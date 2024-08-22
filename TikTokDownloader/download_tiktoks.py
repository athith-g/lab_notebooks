from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import os
import json
from convert_txt import convert_text, create_text


def check_login_modal():
    try:
        driver.find_element(By.ID, "login-modal-title").click()
        input("Quit login on browser and press 'Enter' key here: ")
        print("Login window removed successfully")
    except:
        print("No login detected")


def right_click_vid():
    try:
        vid = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div/video')
        actionChains.context_click(vid).perform()
        sleep(0.5)
    except:
        print("Couldn't download")


def captcha_check():
    sleep(1)
    try:
        driver.find_element(By.CLASS_NAME,'captcha_verify_bar--title').click()
        input("Complete captcha (and log in) and press 'Enter' key here: ")
        print("Completed captcha successfully.")
    except:
        print("No Captcha")


def download_video(i, links, url):
    try:
        if driver.find_element(By.XPATH, '/html/body/div[1]/ul/li[1]/span').text == "Download video":
            driver.find_element(By.XPATH, '/html/body/div[1]/ul/li[1]').click()
            sleep(3)
            os.rename("/Users/athith_g/Downloads/Download.mp4", f"/Users/athith_g/Downloads/{i + 1}.mp4")
            links[url] = 'downloaded'
        else:
            links[url] = 'not_permitted'
            print("Download button not present")
        return True
    except:
        links[url] = 'error'
        print("Error")
        return False


def create_driver():
    options = Options()
    options.binary_location = "/Users/athith_g/Programming/chrome-test.app/Contents/MacOS/Google Chrome for Testing"
    return webdriver.Chrome(options=options)


# CHANGE CATEGORY BASED ON WHAT SHEET YOU'RE USING (E.G., category = wine when using wine.xlsx)
category = 'wine'

# CHANGE SPREADSHEET TO APPROPRIATE SHEET
create_text('spreadsheets/wine.xlsx', category)
convert_text(category)


with open(f"links_{category}.json") as file:
    links = json.load(file)

driver = create_driver()
vid_count = 0

# Sometimes the bot moves too quickly and doesn't download a video that is downloadable
# Set revision to True if you're making a second pass over the spreadsheet to try downloading the videos that couldn't be downloaded
revision = False
for i, url in enumerate(links):
    if revision:
        if links[url] != "error":
            continue
        if links[url] == "unvisited":
            break
    if i == 100:
        break

    actionChains = ActionChains(driver)
    driver.get(url)
    sleep(1)

    check_login_modal()
    captcha_check()
    right_click_vid()

    if download_video(i, links, url):
        vid_count += 1

    print(f"On video {i}")

with open(f'links_{category}.json', 'w') as file:
    file.write(json.dumps(links))



