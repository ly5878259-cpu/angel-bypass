from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

def run_bot(url):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    time.sleep(5)

    words = [
        "Accept Notifications",
        "Register Now & Place Your Bet!",
        "Complete And Get Rewarded",
        "Discover the Best App",
        "?",
        "New App For Your Desktop",
        "Unlock Content"
    ]

    main_tab = driver.current_window_handle

    while True:

        clicked = False

        for word in words:

            elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{word}')]")

            for el in elements:
                try:
                    el.click()
                    clicked = True
                    time.sleep(2)

                    tabs = driver.window_handles

                    if len(tabs) > 1:
                        for tab in tabs:
                            if tab != main_tab:
                                driver.switch_to.window(tab)
                                driver.close()
                                driver.switch_to.window(main_tab)

                except:
                    pass

        if not clicked:
            break

    try:
        yo = driver.find_element(By.XPATH, "//*[contains(text(),'YO')]")
        yo.click()
    except:
        pass

    final_url = driver.current_url

    driver.quit()

    return final_url


@app.route("/bypass")
def bypass():

    url = request.args.get("url")

    if not url:
        return {"error": "Missing URL"}

    result = run_bot(url)

    return jsonify({
        "success": True,
        "result": result
    })


@app.route("/")
def home():
    return "Angel Selenium API Running"
