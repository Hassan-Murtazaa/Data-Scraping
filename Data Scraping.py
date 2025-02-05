from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd

driver = webdriver.Chrome()
driver.set_page_load_timeout(30)

def get_video_details(video):
    video_details = {}
    
    try:
        title_element = video.find_element(By.XPATH, './/*[@id="video-title"]')
        video_details['Title'] = title_element.text
    except:
        video_details['Title'] = None
    
    try:
        views_element = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]')
        video_details['Views'] = views_element.text
    except:
        video_details['Views'] = None

    try:
        posted_time_element = video.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]')
        video_details['Posted Time'] = posted_time_element.text
    except:
        video_details['Posted Time'] = None

    try:
        thumbnail_element = video.find_element(By.XPATH, './/*[@id="thumbnail"]/yt-image/img')
        video_details['Thumbnail'] = thumbnail_element.get_attribute('src')
    except:
        video_details['Thumbnail'] = None

    try:
        URL_element = video.find_element(By.XPATH, './/a[@id="thumbnail"]')
        video_details['URL'] = URL_element.get_attribute('href')
    except:
        video_details['URL'] = None

    return video_details

channel_url = 'https://www.youtube.com/@skgameon/videos'
driver.get(channel_url)
driver.maximize_window()
sleep(5)

for i in range(2):
    driver.execute_script("window.scrollBy(0, 700);")
    sleep(2)

videos = driver.find_elements(By.XPATH, '//*[@id="dismissible"]')

video_list = []

for video in videos:
    details = get_video_details(video)
    video_list.append(details)

# Extract comments for each video
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

        sleep(5)

df = pd.DataFrame(video_list)
df.to_csv("Video Details.csv", index=False)

driver.close()