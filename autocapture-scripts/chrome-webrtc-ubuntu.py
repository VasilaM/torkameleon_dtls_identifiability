import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

INTERFACE = "lo"
DISPLAY_FILTER = "dtls.handshake"
CAPTURE_DIR = "../webrtc_sample_pcap/ubuntu"
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"

def automate_capture(iteration):
    profile_path = "/home/vasila/selenium_profiles/iw_test_profile"
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

        driver.get("https://webrtc.github.io/samples/src/content/peerconnection/pc1/")
        time.sleep(2)

        start = driver.find_element(By.XPATH, f'/html/body/div[1]/div/button[1]')
        start.click()
        time.sleep(1)
        call = driver.find_element(By.XPATH, f'/html/body/div[1]/div/button[2]')
        call.click()
        time.sleep(2)
        driver.close()
        capture_process.terminate()
        driver.close()
        capture_process.terminate()
        filter_file = os.path.join(CAPTURE_DIR, f"ubuntu_webrtc_chrome_{iteration}.pcap")
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


for i in range(1, 151):
    automate_capture(i)
    time.sleep(1)

