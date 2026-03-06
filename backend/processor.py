import pandas as pd
from pydantic import BaseModel
from typing import List
import os

# 1. Define what a "Categorized Transaction" looks like
class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: str  # The AI will fill this in

class FinanceProcessor:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        """Load the CSV using Pandas"""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f" File not found at: {os.path.abspath(self.csv_path)}")
        self.df = pd.read_csv(self.csv_path, sep=",")
        print(f" Loaded {len(self.df)} transactions.")

    def run_simple_logic(self):

        if self.df is None:
            raise ValueError("Data is not loaded. Call load_data() first.")

        # For every row in 'description', run my function and put the result in the 'category' column.
        self.df['category'] = self.df['description'].apply(self.get_ai_category)
        return self.df

    def get_total_spending(self):
        """Return the total value in the `amount` column."""
        if self.df is None:
            raise ValueError("Data is not loaded. Call load_data() first.")
        if "amount" not in self.df.columns:
            raise KeyError("Missing required column: amount")
        return self.df["amount"].sum()

    def get_expensive_transactions(self, limit: float):
        expensive_items = self.df[self.df['amount'] > limit]
        """Return transactions where amount is greater than `limit`."""
        if self.df is None:
            raise ValueError("Data is not loaded. Call load_data() first.")
        if "amount" not in self.df.columns:
            raise KeyError("Missing required column: amount")
        return self.df[self.df["amount"] > limit]

    def get_ai_category(self, description: str):

    # Define a map
        mapping = {
            "Starbucks": "Food & Drink",
            "Netflix": "Subscriptions",
            "Shell": "Transport",
            "Whole Foods": "Groceries",
            "Steam": "Entertainment"
        }

        # 'desc_lower' makes it case-insensitive
        desc_lower = description.lower()

        for keyword, category in mapping.items():
            if keyword.lower() in desc_lower:
                return category

        # The Fallback
        return "Miscellaneous"

# --- Execution Block ---
if __name__ == "__main__":
    PATH_TO_CSV = "../data/transactions.csv"
    processor = FinanceProcessor(PATH_TO_CSV)

    processor.load_data()

    #1. Run the 'Brain' (The Dictionary mapping)
    processed_df = processor.run_simple_logic()

    #2. Check a big spender
    big_stuff = processor.get_expensive_transactions(20.0)

    print("--- CATEGORIZED DATA ---")
    print(processed_df[['description', 'category']]) # Show only these two columns

    print("\n--- BIG SPENDERS ---")
    print(big_stuff)