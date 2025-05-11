import pandas as pd
import re

def clean_price(price):
    """Clean price by removing currency symbols and converting to float."""
    if pd.isna(price) or price in ["N/A", "Page 1 of 1"]:
        return None
    try:
        cleaned_price = re.sub(r'[^\d.]', '', str(price))
        return float(cleaned_price) if cleaned_price else None
    except (ValueError, TypeError):
        return None

def clean_reviews(reviews):
    """Clean reviews by removing commas and converting to int."""
    if pd.isna(reviews) or reviews in ["N/A", "Page 1 of 1", "Previous"]:
        return None
    try:
        cleaned_reviews = re.sub(r'[^\d]', '', str(reviews))
        return int(cleaned_reviews) if cleaned_reviews else None
    except (ValueError, TypeError):
        return None

def clean_rating(rating):
    """Clean rating by converting to float."""
    if pd.isna(rating) or rating in ["N/A", "Page 1 of 1", "Previous"]:
        return None
    try:
        return float(rating)
    except (ValueError, TypeError):
        return None

def clean_data(input_file, output_file):
    """Clean and prepare the DataFrame for visualization."""
    print(f"Loading data from {input_file} for cleaning...")
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} rows with columns: {list(df.columns)}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
    print("Starting data cleaning...")
    
    # Standardize column names
    df.columns = ["Title", "Brand", "Rating", "Reviews", "Price", "Image URL", "Product URL", "Is Sponsored"]
    
    # Clean the Brand column: Remove "Visit the" and "Store"
    df["Brand"] = df["Brand"].str.replace("Visit the ", "").str.replace(" Store", "")
    
    # Convert text columns to string type, handling NaN
    text_columns = ['Title', 'Brand', 'Image URL', 'Product URL', 'Is Sponsored']
    for col in text_columns:
        df[col] = df[col].astype(str).replace('nan', '')
    
    # Clean and convert numeric columns
    df['Price'] = df['Price'].apply(clean_price)
    df['Reviews'] = df['Reviews'].apply(clean_reviews)
    df['Rating'] = df['Rating'].apply(clean_rating)
    
    # Standardize text columns (strip whitespace)
    df['Title'] = df['Title'].str.strip()
    df['Brand'] = df['Brand'].str.strip()
    df['Image URL'] = df['Image URL'].str.strip()
    df['Product URL'] = df['Product URL'].str.strip()
    df['Is Sponsored'] = df['Is Sponsored'].str.strip()
    
    # Remove rows with None, "N/A", or empty values in any column
    initial_rows = len(df)
    # First, replace empty strings with None for consistent handling
    df = df.replace('', None)
    # Now remove rows with None or "N/A"
    df = df[~df.isin([None, "N/A"]).any(axis=1)]
    print(f"Removed {initial_rows - len(df)} rows with 'N/A', None, or empty values. {len(df)} rows remain.")
    
    # Verify data types
    print("\nData types after cleaning:")
    print(df.dtypes)
    
    # Summary of missing values
    print("\nMissing values after cleaning:")
    print(df.isna().sum())
    
    # Save the cleaned data
    try:
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file} with {len(df)} rows.")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")
        return None
    
    return output_file