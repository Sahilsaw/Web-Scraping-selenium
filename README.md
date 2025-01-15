
# Twitter Scraping Project

This project is designed to scrape the top 5 trending topics from Twitter's homepage using Selenium, ProxyMesh for rotating IPs, and store the results in MongoDB.

## Steps to Run the Project

1. Start MongoDB server on port 27017
2. Switch to the `TwitterScraping` database:
   ```bash
   use TwitterScraping
   ```
3. Create the `trends` collection:
   ```bash
   db.createCollection("trends")
   ```

4. Run the following commands in your terminal, making sure you are in the project directory:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

5. Change the username and password in the script to your Twitter credentials.

## Technologies Used
- Python
- Selenium
- MongoDB
- ProxyMesh
