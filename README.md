# YouTube Video Scraper using Selenium

## Overview
This script automates the process of scraping YouTube video details and comments from a specific channel using Selenium and Python. It extracts information such as:
- Video Title
- Views Count
- Posted Time
- Thumbnail URL
- Video URL
- Comments

The extracted data is saved in a CSV file for further analysis.

## Prerequisites
Ensure you have the following installed:
- Python (>=3.x)
- Google Chrome
- Chrome WebDriver (matching your Chrome version)
- Required Python libraries:
  ```sh
  pip install selenium pandas
  ```

## How It Works
1. Opens the specified YouTube channel's videos page.
2. Scrolls down to load more videos.
3. Extracts video details from each visible video.
4. Navigates to each video page to scrape comments.
5. Saves the data into a CSV file (`Video Details.csv`).

## Code Explanation
### Importing Libraries
```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
```
- `selenium`: For web automation.
- `pandas`: For handling and saving extracted data.
- `sleep`: To introduce delays for smooth execution.

### Setting Up WebDriver
```python
driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
```
- Initializes the Chrome WebDriver.
- Sets a page load timeout of 30 seconds.

### Function to Extract Video Details
```python
def get_video_details(video):
    video_details = {}
    try:
        title_element = video.find_element(By.XPATH, './/*[@id="video-title"]')
        video_details['Title'] = title_element.text
    except:
        video_details['Title'] = None
    ...  # Additional extraction logic for views, posted time, thumbnail, and URL
    return video_details
```
- Extracts title, views, posted time, thumbnail, and video URL.
- Uses XPath to locate elements on the page.

### Navigating to the Channel and Scraping Videos
```python
channel_url = 'https://www.youtube.com/@skgameon/videos'
driver.get(channel_url)
driver.maximize_window()
sleep(5)

for i in range(2):
    driver.execute_script("window.scrollBy(0, 700);")
    sleep(2)
```
- Opens the YouTube channel's video section.
- Scrolls down to load more videos dynamically.

### Scraping Comments from Each Video
```python
for video in video_list:
    if video['URL']:
        driver.get(video['URL'])
        sleep(10)
        try:
            for i in range(4):
                driver.execute_script("window.scrollBy(0, 700);")
                sleep(2)
            comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
            comments_text = [comment.text for comment in comments]
            video['Comments'] = comments_text
        except Exception as e:
            video['Comments'] = []
            print(f"Could not retrieve comments for {video['Title']}: {e}")
```
- Opens each video URL and extracts comments.
- Scrolls down to load more comments.

### Saving Data to CSV
```python
df = pd.DataFrame(video_list)
df.to_csv("Video Details.csv", index=False)
```
- Converts the extracted data into a DataFrame.
- Saves it as `Video Details.csv`.

### Closing the WebDriver
```python
driver.close()
```
- Ensures proper closure of the browser instance.

## Running the Script
Run the script using:
```sh
python script.py
```
Ensure Chrome WebDriver is in your system's PATH or specify its location in the script.

## Notes
- This script might need updates if YouTube's HTML structure changes.
- Use appropriate `sleep` intervals to prevent getting blocked.
- Running the script too frequently may result in temporary IP bans from YouTube.

## Example Output
A sample output in `Video Details.csv`:

| Title  | Views  | Posted Time | Thumbnail | URL  | Comments |
|--------|--------|-------------|-----------|------|----------|
| Video 1 | 10K views | 1 week ago | [Link](image_url) | [YouTube Link](video_url) | ["Great video!", "Awesome content!"] |

