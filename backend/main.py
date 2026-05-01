from fastapi import FastAPI, UploadFile, File
from processor import FinanceProcessor
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import shutil
import os
import time


app = FastAPI(
    title="Cognis API",
    description="Backend engine for AI-powered financial tracking",
    version="1.0.0"
)
finance_engine = FinanceProcessor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

# Create folders
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Master file path to be used everywhere
ACTIVE_FILE = os.path.join(DATA_DIR, "active_transactions.csv")

def process_and_categorize(file_path: str, proc: FinanceProcessor):
    try:
        # 1. Load and Categorize New Data
        new_df = pd.read_csv(file_path)
        print(f"--- NEW UPLOAD: {len(new_df)} rows ---")
        
        new_df['category'] = new_df['description'].apply(proc.get_ai_category)

        # 2. Check for Existing Data
        if os.path.exists(ACTIVE_FILE):
            existing_df = pd.read_csv(ACTIVE_FILE)
            print(f"--- FOUND EXISTING: {len(existing_df)} rows ---")
            combined_df = pd.concat([existing_df, new_df], ignore_index=True, sort=False)
            final_df = combined_df.drop_duplicates(subset=['date', 'description', 'amount'])
        else:
            final_df = new_df

        # 3. Final Save
        final_df.to_csv(ACTIVE_FILE, index=False)
        print(f"--- SUCCESS: Data saved to {ACTIVE_FILE} ---")
        return final_df

    except Exception as e:
        print(f"Pipeline Error: {e}")
        return None
        

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    # creating the path to save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Trigger the ai pipeline
    # This turns the raw CSV into a categorized "Active" file
    process_and_categorize(file_path, finance_engine)
    return {
        "status": "success"
    }

@app.get("/transactions")
async def get_transactions():
    if os.path.exists(ACTIVE_FILE):
        try:
            df = pd.read_csv(ACTIVE_FILE)
            if df.empty:
                return {"transactions": []}
            df = df.fillna({"amount": 0, "category": "Uncategorized"})
            return {"transactions": df.to_dict(orient="records")}
        except Exception as e:
            print(f"Read Error: {e}")
            return {"transactions": []}
    return {"transactions": []}
    
@app.delete("/clear-data")
async def clear_data():
    if os.path.exists(ACTIVE_FILE):
        # overwrite the file with empty headers
        df = pd.DataFrame(columns=["date", 'description', 'amount', 'category'])
        df.to_csv(ACTIVE_FILE, index=False)
        return {"message": "Data cleared"}
    return {"message": "Nothing to clear"}