import os
import time
import subprocess

DISPLAY_FILTER = "dtls.handshake"
CAPTURE_DIR = "../zoom_pcap/ubuntu/firefox"

def get_handshakes(iteration):
    filter_file = os.path.join(CAPTURE_DIR, f"ubuntu_zoom_firefox_{iteration}.pcap")
    output_file = os.path.join(CAPTURE_DIR, f"real_ubuntu_zoom_firefox_{iteration}.pcap")
    filter_process = subprocess.Popen(
        [
        "tshark",
        "-r", filter_file,
        "-Y", DISPLAY_FILTER,
        "-w", output_file
    ]
    )
    print("finishing filter process")
    time.sleep(2)
    filter_process.terminate()

for i in range(1, 151):
    get_handshakes(i)