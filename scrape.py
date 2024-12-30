from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
print("SBR_WEBDRIVER:", SBR_WEBDRIVER)  # Check if the WebDriver URL is loaded

def scrape_website(website):
    if not SBR_WEBDRIVER:
        print("Error: WebDriver URL is not set. Check .env file.")
        return None

    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)

        # Get the HTML source
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove scripts, styles, and other non-content elements
    for script_or_style in soup(["script", "style", "header", "footer", "aside"]):
        script_or_style.extract()

    # Get clean text content
    cleaned_content = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

def split_dom_content(dom_content, max_length=10000):  # Increased max_length
    return [dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)]
