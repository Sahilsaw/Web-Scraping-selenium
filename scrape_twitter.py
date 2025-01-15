import random  # Import random to choose a random proxy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bson import ObjectId  # To handle ObjectId serialization
import time

def load_proxies():
    with open('valid_proxies.txt', 'r') as f:
        proxies = f.readlines()
    proxies = [proxy.strip() for proxy in proxies]  # Clean up extra spaces/newlines
    return proxies

def scrape_twitter():
    proxies = load_proxies()  # Load the list of proxies
    # Randomly select a proxy for this scraping attempt
    proxy = random.choice(proxies)  # Choose a random proxy

    # Set up Chrome options with the selected proxy
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={proxy}")  # Use the selected proxy
    chrome_options.add_argument("--start-maximized")  # Optional: starts Chrome maximized

    service = Service("./drivers/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to Twitter login page
        print("Opening Twitter login page...")
        driver.get("https://x.com/login")

        # Wait for the username field to load explicitly
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        print("Username field is visible, entering username...")

        # Find the username input field using XPath
        username = driver.find_element(By.XPATH, "//input[@name='text']")
        username.send_keys("@Bhuvankuma17741")

        # Find the "Next" button and click it automatically
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        print("Clicking the 'Next' button...")
        next_button.click()

        # Find the password input field using the name attribute or XPath
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        print("Password field is visible, entering password...")

        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys("Saktimanisnoob1!")

        # Submit the login form (press Enter)
        print("Submitting login form...")
        password.send_keys(Keys.RETURN)

        # Navigate to the Explore > Trending page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/explore']")))
        print("Navigating to the Explore page...")
        driver.get("https://twitter.com/explore/tabs/trending")

        # Wait for the trending topics section to load
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='trend']")))
        print("Trending topics section is visible, fetching topics...")

        time.sleep(3)
        
        # Fetch trending topics
        trending_items = driver.find_elements(By.XPATH, "//div[@data-testid='trend']")
        trending_data = []
        for item in trending_items:
            try:
                # Extract topic name (e.g., '#Tabu', 'Bhagat Singh')
                topic_name = item.find_element(By.XPATH, ".//span[@dir='ltr' and @class='css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3']").text

                # Extract category (e.g., Entertainment, Politics)
                category = item.find_element(By.XPATH, ".//div[@dir='ltr' and contains(@class, 'css-146c3p1') and not(@aria-hidden)]//span").text
        
                # Extract the number of posts related to the trend
                post_count = item.find_element(By.XPATH, ".//div[@dir='ltr' and contains(@class, 'css-146c3p1')]//span[contains(text(), 'posts')]").text

                trending_data.append({
                    'topic_name': topic_name,
                    'category_name': category,
                    'Post_count': post_count
                })
                
            except Exception as e:
                print(f"Error parsing topic: {e}")

        # MongoDB setup
        client = MongoClient("mongodb://localhost:27017/")
        db = client["TwitterScraping"]
        collection = db["trends"]

        # Store results in MongoDB
        result = {
            "unique_id": str(datetime.now().timestamp()),
            "trends": trending_data,
            "date_time": datetime.now().isoformat(),
            "proxy": proxy,  # Include the proxy used
        }
        inserted_id = collection.insert_one(result).inserted_id

        # Add the inserted ID to the result for JSON extract
        result["_id"] = str(inserted_id)

        # Output result to console for debugging
        print("Trending Topics:")
        for idx, trend in enumerate(trending_data, start=1):
            print(f"{idx}) {trend['topic_name']}")

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()
