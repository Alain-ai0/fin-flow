from fastapi import FastAPI, UploadFile, File
from processor import FinanceProcessor
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import shutil
import os
import time


app = FastAPI()
finance_engine = FinanceProcessor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
UPLOAD_DIR = "../data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_and_categorize(file_path: str, proc: FinanceProcessor):
    try:
        # Load the raw uploaded data
        df = pd.read_csv(file_path)
        print(f"Starting AI categorization for {len(df)} transactions...")

        categories = []
        for desc in df['description']:
            cat = proc.get_ai_category(desc)
            categories.append(cat)
            print(f"Categorized: {desc} -> {cat}")
            time.sleep(1)

        df['category'] = df['description'].apply(proc.get_ai_category)

        # Save to the 'active' file for the dashboard to read
        active_path = os.path.join(DATA_DIR, "active_transactions.csv")
        df.to_csv(active_path, index=False)
        print("Categorization successful!")
        return df

    except Exception as e:
        print(f"Error during AI pipeline: {e}")
        # If it fails, we still want a file to exist so the frontend doesn't break
        return None
        

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    # creating the path to save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Triger the ai pipeline
    # This turns the raw CSV into a categorized "Active" file
    process_and_categorize(file_path, finance_engine)
    return {
        "message": "AI Categorization Complete",
        "filename": file.filename,
        "status": "success"
    }


@app.get("/transactions")
async def get_transactions():
    # Always read from the 'active' file created by the pipeline
    active_path = os.path.join(DATA_DIR, "active_transactions.csv")
    if os.path.exists(active_path):
        df = pd.read_csv(active_path)
        # Handle empty amounts or NaNs just in case
        df = df.fillna({"amount": 0, "category": "Uncategorized"})
        return {"transactions": df.to_dict(orient="records")}
    return {"transactions": []}