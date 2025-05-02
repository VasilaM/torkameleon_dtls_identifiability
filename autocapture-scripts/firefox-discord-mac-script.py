import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

INTERFACE = "en0"
DISPLAY_FILTER = "dtls"
CAPTURE_DIR = "../discord_pcap/mac/firefox"
GECKO_DRIVER_PATH = "/opt/homebrew/bin/geckodriver"

def automate_capture():
    profile_path = "/Users/vasilamirshamsova/selenium_profiles/iw_test_profile-2"
    os.makedirs(profile_path, exist_ok=True)

    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # options.add_argument("--headless=new")

    service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://discord.com/channels/1361499421379924234/1361499422059397272")
    time.sleep(60)

    try:
        for i in range(63, 151):
            output_file = os.path.join(CAPTURE_DIR, f"full_dtls_{str(i)}.pcap")
            print(f"Starting capture: {output_file}")

            capture_process = subprocess.Popen(
                [
                    "tshark",
                    "-i", INTERFACE,
                    "-w", output_file
                ]
            )
            time.sleep(3)
            # @class=link__2ea32
            voice_channel_link = driver.find_element(By.XPATH, f'//a[@role="button" and @data-list-item-id="channels___1361499422059397273"]')
            voice_channel_link.click()
            time.sleep(2)


            disconnect_button = driver.find_element(By.XPATH, f'//button[@aria-label="Disconnect" and @type="button"]')
            disconnect_button.click()
            time.sleep(1)
            capture_process.terminate()
            print(f"terminated capturing for pcap {i}")
            time.sleep(2)
            filter_file = os.path.join(CAPTURE_DIR, f"mac_discord_firefox_{i}.pcap")
            filter_process = subprocess.Popen(
                    [
                    "tshark",
                    "-r", output_file,
                    "-Y", "dtls.handshake",
                    "-w", filter_file
                ]
            )
            time.sleep(2)
            filter_process.terminate()
            time.sleep(1)
            print(f"pcap {i} filtered and saved")

        # while True:
        #     time.sleep(5)


    except Exception as e:
        print(f"error: {e}")
    finally:
        driver.quit()



# for i in range(1, 4):
#     automate_capture(i)
#     time.sleep(3)
automate_capture()
