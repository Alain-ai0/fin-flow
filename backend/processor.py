import pandas as pd
from pydantic import BaseModel
from typing import List
import os
import ollama

# 1. Defines the structure of a single transaction for validation
class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: str  # The AI will fill this in

class FinanceProcessor:
    def __init__(self, csv_path=None):
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
        """
        Assigns a category using a fast local lookup, falling back to a local LLM (Ollama) for complex descriptions.
        """
    
        # Define a map
        # Priority 1: Instant lookup for common/known vendors
        mapping = {
            "Starbucks": "Food & Drink",
            "Netflix": "Subscriptions",
            "Shell": "Transport",
            "Whole Foods": "Groceries",
            "Steam": "Entertainment"
        }

        # 'desc_lower' makes it case-insensitive
        desc_lower = description.lower()

        # ... (dictionary loop code)
        for keyword, category in mapping.items():
            if keyword.lower() in desc_lower:
                return category
            
        # Priority 2: Use Llama3 to 'guess' categories for unknown stores
        categories = "Housing, Transportation, Food & Drink, Utilities, Subscriptions, Entertainment, Shopping, Health, Miscellaneous"
        
        # System role defines the 'Rules'; User role provides the 'Data
        messages = [
            {
                "role": "system",
                "content": f"You are a professional accountant. Your job is to categorize bank transactions into exactly one of these categories: [{categories}]. Respond with ONLY the category name."
            },
            {
                "role": "user",
                "content": f"Categorize this transaction: '{description}'"
            }
        ]

        try:
            # Synchronous call to local Ollama server
            response = ollama.chat(model='llama3', messages=messages)
            return response['message']['content'].strip()
        except Exception as e:
            # Fallback to prevent the entire pipeline from crashing
            print(f"AI Error: {e}")
            return "Miscellaneous"
        
    def save_data(self, output_path: str):
        """Save the processed DataFrame to a new CSV."""
        if self.df is None:
            raise ValueError("Data is not loaded. Call load_data() first.")
        self.df.to_csv(output_path, index=False)
        print(f"Processed data saved to: {output_path}")

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

    output_file = "../data/processed_transactions.csv"
    processor.save_data(output_file)