import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

INTERFACE = "en0"
DISPLAY_FILTER = "dtls"
CAPTURE_DIR = "../discord_pcap/mac"
CHROME_DRIVER_PATH = "/opt/homebrew/bin/chromedriver"

def automate_capture(iteration):
    profile_path = "/Users/vasilamirshamsova/selenium_profiles/iw_test_profile"
    os.makedirs(profile_path, exist_ok=True)

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

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
        time.sleep(2)

        driver.get("https://discord.com/channels/1361499421379924234/1361499422059397272")
        time.sleep(5)

        # @class=link__2ea32
        voice_channel_link = driver.find_element(By.XPATH, f'//a[@role="button" and @data-list-item-id="channels___1361499422059397273"]')
        voice_channel_link.click()
        time.sleep(3)


        disconnect_button = driver.find_element(By.XPATH, f'//button[@aria-label="Disconnect" and @type="button"]')
        disconnect_button.click()
        time.sleep(1)

        capture_process.terminate()
        time.sleep(3)
 
        filter_process = subprocess.Popen(
                [
                "tshark",
                "-r", output_file,
                "-Y", "dtls.handshake",
                "-w", f"mac_discord_chrome_{iteration}.pcap"
            ]
        )
        time.sleep(2)
        filter_process.terminate()
        # while True:
        #     time.sleep(5)

    except Exception as e:
        print(f"error during iteration {iteration}: {e}")
    finally:
        driver.quit()


for i in range(101, 151):
    automate_capture(i)
    time.sleep(3)

