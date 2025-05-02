import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

INTERFACE = "lo"
DISPLAY_FILTER = "dtls.handshake"
CAPTURE_DIR = "../webrtc_sample_pcap/firefox"
GECKO_DRIVER_PATH = "/snap/bin/geckodriver"

def automate_capture(iteration):
    profile_path = "/hoem/vasila/selenium_profiles/iw_test_profile-2"
    os.makedirs(profile_path, exist_ok=True)
    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")
    options.set_preference("permissions.default.microphone", 1)
    options.set_preference("permissions.default.camera", 1)

    service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
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
        time.sleep(2)
        call = driver.find_element(By.XPATH, f'/html/body/div[1]/div/button[2]')
        call.click()
        time.sleep(2)
        driver.close()
        capture_process.terminate()
        filter_file = os.path.join(CAPTURE_DIR, f"mac_webrtc_chrome_{iteration}.pcap")
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
        # while True:
        #     time.sleep(5)


    except Exception as e:
        print(f"error: {e}")
    finally:
        driver.quit()



for iteration in range(4, 251):
    automate_capture(iteration)
    time.sleep(1)
# automate_capture()
