
# Web-Scraping-Selenium

This project scrapes trending topics from Twitter's homepage using Selenium, stores them in MongoDB, and displays the results on a webpage.

## Steps to Run the Project

1. Start the MongoDB server on port 27017.
2. In the terminal, navigate to the project directory and run the following commands:

```bash
pip install -r requirements.txt
python app.py
```

3. Change the username and password in the script to your Twitter username and password.

## Requirements

- MongoDB
- Python 3.x
- Selenium
- Flask
- ProxyMesh (for IP rotation)

## Usage

Once the server is running, you can trigger the scraping task by clicking the button on the webpage. The results will display the trending topics along with the IP address used for scraping and a JSON extract from MongoDB.

## License

This project is licensed under the MIT License.
