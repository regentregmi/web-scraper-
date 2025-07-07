import requests
from bs4 import BeautifulSoup
import json

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises http Error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = {}

    # Extract headings
    
    headings = []
    for tag in ['h1', 'h2', 'h3']:
        for heading in soup.find_all(tag):
            headings.append(heading.get_text(strip=True))
    data['headings'] = headings

    # Extract links
    
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append({'text': a_tag.get_text(strip=True), 'url': a_tag['href']})
    data['links'] = links

    # Extract paragraphs
    
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    data['paragraphs'] = paragraphs
    return data

def save_to_json(data, filename='scraped_data.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error saving data: {e}")

def main():
    url = input("Enter the URL to scrape (or press Enter for default): ").strip()
    if not url:
        url = ''  
        # default URL for testing

    print(f"Fetching: {url}")
    html = fetch_html(url)
    if html:
        scraped_data = parse_html(html)
        save_to_json(scraped_data)

if __name__ == '__main__':
    main()
