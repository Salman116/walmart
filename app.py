import os

import cv2

import uuid

import time

from selenium import webdriver

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By

from flask import Flask, request, send_file

from selenium.webdriver import ActionChains

from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)


def walmart(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()
    time.sleep(3)
    if "verification" in driver.title.lower():
        times = 0
        while times < 3:
            try:
                element = driver.find_element(By.ID, 'px-captcha')
                action = ActionChains(driver)
                action.click_and_hold(element)
                action.perform()
                time.sleep(10)
                action.release(element)
                action.perform()
                time.sleep(0.2)
                action.release(element)
                break
            except:
                driver.refresh()
                time.sleep(3)
                pass
            times += 1
    else:
        pass
    try:
        driver.save_screenshot("image.jpg")
        path = os.getcwd()
        image = cv2.imread(path + '\\image.jpg')
        image.shape
        x, y = 0, 0
        h, w = image.shape[:-1]
        crop_value = int(0.125 * h)
        cropped_image = image[crop_value:h, x:w]
        driver.quit()
        return cropped_image

    except Exception as e:

        driver.quit()


@app.route('/walmart', methods=['GET'])
def walmart2():
    url = request.args.get('url')
    image = walmart(url)
    cv2.imwrite("cropped.jpg", image)

    return send_file("cropped.jpg", mimetype='image/gif')


if __name__ == "__main__":
    app.run(debug=True)
