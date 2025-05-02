import os
import csv

# Path to the directory with the files
directory = "./webrtc_sample_pcap/firefox"

# Use the name of the directory as the label
label = "webrtc"

# Get all files in the directory (ignores subdirectories)
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Output CSV file
csv_filename = "webrtc_mac_firefox.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Item', 'Label'])  # Header
    for filename in files:
        writer.writerow([filename, label])

print(f"CSV file '{csv_filename}' created with {len(files)} items.")
