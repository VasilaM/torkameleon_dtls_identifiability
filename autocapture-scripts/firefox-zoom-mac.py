import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

INTERFACE = "en0"
DISPLAY_FILTER = "dtls.handshake"
CAPTURE_DIR = "../zoom_pcap/mac/firefox"
GECKO_DRIVER_PATH = "/opt/homebrew/bin/geckodriver"

def automate_capture():
    profile_path = "/Users/vasilamirshamsova/selenium_profiles/iw_test_profile-2"
    os.makedirs(profile_path, exist_ok=True)
    options = Options()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Disable download prompts and block known Zoom pkg MIME types
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", "/dev/null")  # Use a junk folder
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-apple-diskimage, application/octet-stream")
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("pdfjs.disabled", True)
    options.set_preference("browser.download.forbid_open_with", True)

    # (optional) Block all automatic downloads
    options.set_preference("browser.download.useDownloadDir", False)
    # options.add_argument("--headless=new")

    service = Service(GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://zoom.us/j/96108872847?pwd=Ge4xu57q6avAaCweifEG0hPzbrvRuI.1#success")
    time.sleep(6)

    download_now_link = driver.find_element(By.XPATH, f'//*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3/a')
    download_now_link.click()
    time.sleep(3)
    try:
        for iteration in range(51, 151):
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

            join_web_link = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div/div[2]/h3[2]/span/a')
            join_web_link.click()
            time.sleep(2)
            capture_process.terminate()
            print(f"terminated capture: {output_file}, writing to mac_zoom_firefox_{iteration}.pcap ")
            filter_file = os.path.join(CAPTURE_DIR, f"mac_zoom_firefox_{iteration}.pcap")
            filter_process = subprocess.Popen(
                    [
                    "tshark",
                    "-r", output_file,
                    "-Y", DISPLAY_FILTER,
                    "-w", filter_file
                ]
            )
            print("finishing filter process")
            time.sleep(2)
            filter_process.terminate()
            driver.back()
        # while True:
        #     time.sleep(5)


    except Exception as e:
        print(f"error: {e}")
    finally:
        driver.quit()




automate_capture()
# automate_capture()
