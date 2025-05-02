import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

INTERFACE = "en0"
DISPLAY_FILTER = "dtls.handshake"
CAPTURE_DIR = "../zoom_pcap/mac"
CHROME_DRIVER_PATH = "/opt/homebrew/bin/chromedriver"

def automate_capture(iteration):
    profile_path = "/Users/vasilamirshamsova/selenium_profiles/iw_test_profile"
    os.makedirs(profile_path, exist_ok=True)

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless=new")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        output_file = os.path.join(CAPTURE_DIR, f"full_dtls_{str(iteration)}.pcap")
        print(f"Starting capture: {output_file}")

        capture_process = subprocess.Popen(
            [
                "tshark",
                "-i", INTERFACE,
                "-w", output_file
            ]
        )
        time.sleep(1)

        driver.get("https://princeton.zoom.us/j/99262750566#success")
        time.sleep(1)

        download_now_link = driver.find_element(By.XPATH, f'//*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3/a')
        download_now_link.click()
        time.sleep(2)

        join_web_link = driver.find_element(By.XPATH, f'//*[@id="zoom-ui-frame"]/div[2]/div[2]/div[2]/h3[2]/span/a')
        join_web_link.click()
        time.sleep(2)
        driver.close()
        capture_process.terminate()
        filter_file = os.path.join(CAPTURE_DIR, f"mac_zoom_chrome_{iteration}.pcap")
        filter_process = subprocess.Popen(
                [
                "tshark",
                "-r", output_file,
                "-Y", DISPLAY_FILTER,
                "-w", filter_file
            ]
        )
        time.sleep(2)
        filter_process.terminate()

    except Exception as e:
        print(f"error during iteration {iteration}: {e}")
    finally:
        driver.quit()


for i in range(101, 151):
    automate_capture(i)
    time.sleep(2)

