# run_scraper.py
from scraper import scrape_amazon_laptops

# Define the URL to scrape
url = "https://www.amazon.com/s?k=laptops&crid=657673YVM6LR&sprefix=%2Caps%2C349&ref=nb_sb_ss_recent_1_0_recent"

# Define the output CSV file name
output_csv = "amazon_laptops.csv"

# Call the function to scrape Amazon laptops and save the data
scrape_amazon_laptops(url, output_csv)
