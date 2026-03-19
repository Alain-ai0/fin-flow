from fastapi import FastAPI
from processor import FinanceProcessor
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "fin-flow Backend is running"}

# CHECK THIS LINE FOR TYPOS:
@app.get("/transactions")
def get_transactions():
    try:
        # Make sure this path actually exists on your computer!
        file_path = "../data/processed_transactions.csv"
        df = pd.read_csv(file_path)
        
        # Convert to a list of dictionaries for JSON
        data = df.to_dict(orient="records")
        return {"transactions": data}
    except Exception as e:
        return {"error": str(e)}