import sys
from scraper import scrape_data
from cleaner import clean_data
from analyzer import analyze_and_visualize

def main():
    """Main function to run the entire pipeline: scrape, clean, and analyze."""
    print("Starting the Amazon sponsored products pipeline...\n")
    
    # Step 1: Scrape the data
    # print("=== Running Scraper ===")
    # raw_data_file = "soft_toys.csv"
    # scraped_file = scrape_data(raw_data_file)
    # if not scraped_file:
    #     print("Scraping failed. Exiting pipeline.")
    #     sys.exit(1)
    scraped_file= "soft_toys.csv"

    # Step 2: Clean the data
    print("\n=== Running Cleaner ===")
    cleaned_data_file = "cleaned_soft_toys.csv"
    cleaned_file = clean_data(scraped_file, cleaned_data_file)
    if not cleaned_file:
        print("Cleaning failed. Exiting pipeline.")
        sys.exit(1)
    
    # Step 3: Analyze and visualize the data
    print("\n=== Running Analyzer ===")
    if not analyze_and_visualize(cleaned_file):
        print("Analysis and visualization failed. Exiting pipeline.")
        sys.exit(1)
    
    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    main()