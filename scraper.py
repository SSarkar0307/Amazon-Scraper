import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.amazon.in/'
}

visited_urls = set()

def is_valid_product_url(url):
    return url.startswith('https://www.amazon.in/') and '/dp/' in url

def get_product_info(url):
    try:
        if not is_valid_product_url(url):
            print(f"Skipping non-product URL: {url[:100]}...")
            return None

        response = requests.get(url, headers=custom_headers, timeout=10)
        if response.status_code != 200:
            print(f"Error {response.status_code} for {url}")
            return None

        soup = BeautifulSoup(response.text, "lxml")

        title = (soup.select_one("#productTitle") or
                 soup.select_one("#title") or
                 soup.select_one("h1#title"))
        title = title.get_text(strip=True) if title else "N/A"

        brand = (soup.select_one("#bylineInfo") or 
                 soup.select_one("a#bylineInfo"))
        brand = brand.get_text(strip=True) if brand else "N/A"

        rating = soup.select_one("span.a-icon-alt")
        rating = rating.get_text(strip=True).split(" ")[0] if rating else "N/A"

        reviews = soup.select_one("#acrCustomerReviewText")
        reviews = reviews.get_text(strip=True).split(" ")[0].replace(",", "") if reviews else "N/A"

        price_elem = (soup.select_one("span.a-offscreen") or
                      soup.select_one(".a-price .a-offscreen") or
                      soup.select_one("#priceblock_ourprice"))
        price = price_elem.get_text(strip=True) if price_elem else "N/A"

        image_elem = soup.select_one("#landingImage") or soup.select_one("#imgTagWrapperId img")
        image_url = image_elem['src'] if image_elem and 'src' in image_elem.attrs else "N/A"

        return {
            "Title": title,
            "Brand": brand,
            "Rating": rating,
            "Reviews": reviews,
            "Price": price,
            "Image URL": image_url,
            "Product URL": url.split('?')[0],
            "Is Sponsored": "NO"
        }

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def parse_listing(listing_url, max_pages=3):
    global visited_urls

    response = requests.get(listing_url, headers=custom_headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {listing_url}")
        return []

    soup_search = BeautifulSoup(response.text, "lxml")

    product_links = []
    for a in soup_search.select('a.a-link-normal.s-no-outline[href*="/dp/"]'):
        url = urljoin(listing_url, a['href'])
        if is_valid_product_url(url) and url not in visited_urls:
            product_links.append(url)

    page_data = []
    for url in product_links:
        visited_urls.add(url)
        print(f"\nScraping product: {url[:80]}...")
        product_info = get_product_info(url)
        if product_info:
            page_data.append(product_info)
            print(f"Success: {product_info['Title'][:50]}...")

    next_page_el = soup_search.select_one('a.s-pagination-next:not(.s-pagination-disabled)')
    if next_page_el and max_pages > 1:
        next_page_url = urljoin(listing_url, next_page_el['href'])
        if next_page_url not in visited_urls:
            page_data += parse_listing(next_page_url, max_pages - 1)

    return page_data

def scrape_data(output_file="soft_toys.csv"):
    """Run the scraper and save the data to a CSV file."""
    data = []
    search_url = "https://www.amazon.in/s?k=soft+toys&ref=nb_sb_noss"
    data = parse_listing(search_url, max_pages=1)
    
    if data:
        df = pd.DataFrame(data)
        print(f"\nSuccessfully scraped {len(df)} products!")
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
    else:
        print("No valid products were scraped")
    return output_file