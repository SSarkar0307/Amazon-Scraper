import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def truncate_title(title, max_length=30):
    """Truncate long titles to fit in visualizations."""
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title

def analyze_and_visualize(input_file):
    """Perform analysis and visualization on the cleaned data."""
    print(f"Starting analysis and visualization on {input_file}...")
    
    # Create output directory for saving PNG files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load the cleaned data
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} rows for analysis.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return False
    
    # Ensure numeric columns are of the correct type
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    
    # Drop any rows with NaN in these columns (shouldn't be any after cleaning, but just in case)
    df = df.dropna(subset=['Price', 'Rating', 'Reviews'])
    print(f"After ensuring numeric columns, {len(df)} rows remain.")
    
    # === Analysis 1: Brand Performance Analysis ===
    print("\n=== Brand Performance Analysis ===")
    
    # Brand Frequency
    brand_counts = df['Brand'].value_counts()
    top_5_brands = brand_counts.head(5)
    print("Top 5 Brands by Frequency:")
    print(top_5_brands)
    
    # Average Rating by Brand
    avg_rating_by_brand = df.groupby('Brand')['Rating'].mean().sort_values(ascending=False)
    print("\nTop 5 Brands by Average Rating:")
    print(avg_rating_by_brand.head(5))
    
    # Visualization 1: Bar Chart - Top 5 Brands by Frequency
    plt.figure(figsize=(10, 6))
    top_5_brands.plot(kind='bar', color='skyblue')
    plt.title('Top 5 Brands by Frequency')
    plt.xlabel('Brand')
    plt.ylabel('Number of Products')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_5_brands_frequency.png'))
    plt.close()
    print(f"Saved bar chart: {os.path.join(output_dir, 'top_5_brands_frequency.png')}")
    
    # Visualization 2: Pie Chart - Percentage Share of Top Brands
    plt.figure(figsize=(8, 8))
    top_5_brands.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#ff99cc'])
    plt.title('Percentage Share of Top 5 Brands')
    plt.ylabel('')  # Remove y-label for pie chart
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_5_brands_share.png'))
    plt.close()
    print(f"Saved pie chart: {os.path.join(output_dir, 'top_5_brands_share.png')}")
    
    # === Analysis 2: Price vs. Rating Analysis ===
    print("\n=== Price vs. Rating Analysis ===")
    
    # Define rating ranges
    bins = [0, 2, 3, 4, 4.5, 5]
    labels = ['0-2', '2-3', '3-4', '4-4.5', '4.5-5']
    df['Rating Range'] = pd.cut(df['Rating'], bins=bins, labels=labels, include_lowest=True)
    
    # Average Price by Rating Range
    avg_price_by_rating = df.groupby('Rating Range')['Price'].mean()
    print("Average Price by Rating Range:")
    print(avg_price_by_rating)
    
    # Identify Price-Performance Outliers (affordable, high-rated products)
    affordable_high_rated = df[(df['Price'] < df['Price'].quantile(0.25)) & (df['Rating'] >= 4.5)]
    print("\nAffordable High-Rated Products (Price < 25th percentile, Rating >= 4.5):")
    if not affordable_high_rated.empty:
        print(affordable_high_rated[['Title', 'Brand', 'Price', 'Rating']].head())
    else:
        print("No affordable high-rated products found.")
    
    # Visualization 3: Scatter Plot - Price vs. Rating
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Price'], df['Rating'], alpha=0.5, color='purple')
    plt.title('Price vs. Rating')
    plt.xlabel('Price ($)')
    plt.ylabel('Rating')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_vs_rating.png'))
    plt.close()
    print(f"Saved scatter plot: {os.path.join(output_dir, 'price_vs_rating.png')}")
    
    # Visualization 4: Bar Chart - Average Price by Rating Range
    plt.figure(figsize=(10, 6))
    avg_price_by_rating.plot(kind='bar', color='lightcoral')
    plt.title('Average Price by Rating Range')
    plt.xlabel('Rating Range')
    plt.ylabel('Average Price ($)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'avg_price_by_rating.png'))
    plt.close()
    print(f"Saved bar chart: {os.path.join(output_dir, 'avg_price_by_rating.png')}")
    
    # === Analysis 3: Review & Rating Distribution ===
    print("\n=== Review & Rating Distribution ===")
    
    # Top 5 Products by Reviews
    top_reviews = df.nlargest(5, 'Reviews')[['Title', 'Brand', 'Reviews', 'Rating']]
    top_reviews['Title'] = top_reviews['Title'].apply(truncate_title)  # Truncate long titles
    print("Top 5 Products by Number of Reviews:")
    print(top_reviews)
    
    # Top 5 Products by Rating
    top_rated = df.nlargest(5, 'Rating')[['Title', 'Brand', 'Rating', 'Reviews']]
    top_rated['Title'] = top_rated['Title'].apply(truncate_title)  # Truncate long titles
    print("\nTop 5 Products by Rating:")
    print(top_rated)
    
    # Visualization 5: Bar Chart - Top 5 Most-Reviewed Products
    plt.figure(figsize=(12, 8))  # Increased figure size for better readability
    plt.barh(top_reviews['Title'], top_reviews['Reviews'], color='gold')
    plt.title('Top 5 Most-Reviewed Products')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Product Title')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_5_reviews.png'))
    plt.close()
    print(f"Saved bar chart: {os.path.join(output_dir, 'top_5_reviews.png')}")
    
    # Visualization 6: Bar Chart - Top 5 Highest-Rated Products
    plt.figure(figsize=(12, 8))  # Increased figure size for better readability
    plt.barh(top_rated['Title'], top_rated['Rating'], color='lightgreen')
    plt.title('Top 5 Highest-Rated Products')
    plt.xlabel('Rating')
    plt.ylabel('Product Title')
    plt.xlim(0, 5)  # Ratings are out of 5
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_5_rated.png'))
    plt.close()
    print(f"Saved bar chart: {os.path.join(output_dir, 'top_5_rated.png')}")
    
    print("\nAnalysis and visualization completed successfully!")
    return True