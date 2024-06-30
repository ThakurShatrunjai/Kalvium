import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

def save_to_csv(headers, rows, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)
    print(f"Data saved to {filename}")


def scrape_website_requests(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Update this selector to match the actual HTML structure of the page
        table = soup.find('table')  # Adjust the selector as necessary

        if table is None:
            return None, None

        headers = [header.text.strip() for header in table.find_all('th')]
        rows = [
            [cell.text.strip() for cell in row.find_all('td')]
            for row in table.find_all('tr')[1:]
        ]

        return headers, rows
    except Exception as err:
        print(f'Error occurred: {err}')
        return None, None

def scrape_website_selenium(url):
    try:
        driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Update this selector to match the actual HTML structure of the page
        table = soup.find('table')  # Adjust the selector as necessary

        if table is None:
            return None, None

        headers = [header.text.strip() for header in table.find_all('th')]
        rows = [
            [cell.text.strip() for cell in row.find_all('td')]
            for row in table.find_all('tr')[1:]
        ]

        return headers, rows
    except Exception as err:
        print(f'Error occurred: {err}')
        return None, None

# URL of the website to scrape
url = 'https://results.eci.gov.in/PcResultGenJune2024/index.htm'

# Attempt to scrape using requests and BeautifulSoup
headers, scraped_data = scrape_website_requests(url)

# If no data is found, attempt to scrape using Selenium
if not headers or not scraped_data:
    print("No data found using requests. Trying with Selenium...")
    headers, scraped_data = scrape_website_selenium(url)

# Printing headers and rows
if headers and scraped_data:
    print("Headers:")
    print(headers)

    print("\nRows:")
    for i, row in enumerate(scraped_data, start=1):
        print(f'{i}: {row}')
else:
    print("No data found.")
    
if headers and scraped_data:
    filename = 'election_results.csv'
    save_to_csv(headers, scraped_data, filename)
else:
    print("No data found.")
