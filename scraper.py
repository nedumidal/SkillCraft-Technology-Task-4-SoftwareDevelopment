# scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import random
import time

def scrape_amazon_laptops(url, output_csv):
    # List of user-agents to rotate
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
    ]
    
    # List of proxies (replace with your own proxies if needed)
    proxies = [
        "http://proxy1.example.com:8888",  # Example proxy
        "http://proxy2.example.com:8888",
        # Add more proxies if you have a proxy service
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),  # Randomly select a user-agent
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # List to store product data
    product_data = []

    # Page number for pagination
    page_number = 1

    while True:
        # Modify URL to include pagination (page=1, page=2, etc.)
        page_url = f"{url}&page={page_number}"

        # Select a random proxy
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}

        try:
            # Send GET request with headers and proxy
            response = requests.get(page_url, headers=headers, proxies=proxy_dict, timeout=10)

            # Handle 503 error (Service Unavailable)
            if response.status_code == 503:
                print(f"503 Service Unavailable on page {page_number}. Retrying...")
                time.sleep(random.randint(15, 30))  # Wait for a random time between 15 to 30 seconds
                continue
            elif response.status_code != 200:
                print(f"Failed to fetch the webpage: {response.status_code}")
                break  # Exit the loop if we get a non-200 status code

            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all products on the page
            products = soup.select(".s-main-slot .s-result-item")

            # If no products are found, stop the loop
            if not products:
                print(f"No more products found on page {page_number}. Stopping.")
                break

            # Extract data for each product
            for product in products:
                name_tag = product.select_one("h2 .a-link-normal")
                name = name_tag.get_text(strip=True) if name_tag else None

                price_whole = product.select_one(".a-price-whole")
                price_fraction = product.select_one(".a-price-fraction")
                price = None
                if price_whole:
                    price = f"{price_whole.get_text(strip=True)}.{price_fraction.get_text(strip=True) if price_fraction else '00'}"

                rating_tag = product.select_one(".a-icon-alt")
                rating = rating_tag.get_text(strip=True) if rating_tag else "No rating"

                # Add the product data to the list if the name and price are found
                if name and price:
                    product_data.append({
                        'Name': name,
                        'Price': price,
                        'Rating': rating
                    })

            # Write product data to CSV
            with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Name', 'Price', 'Rating'])
                writer.writeheader()  # Write the header row
                writer.writerows(product_data)  # Write the product rows

            print(f"Data saved to {output_csv} - Page {page_number}")

            # Wait before scraping the next page to avoid being blocked
            time.sleep(random.randint(5, 10))  # Randomized delay between 5 to 10 seconds

        except Exception as e:
            print(f"Error occurred on page {page_number}: {e}")
            break  # Exit if there is an error

        # Increment page number for the next iteration
        page_number += 1
