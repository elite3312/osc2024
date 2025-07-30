import os
import os.path
import argparse
import time

parser = argparse.ArgumentParser(description='Send a file over serial connection.')
parser.add_argument('-s', '--serial_path', default='/dev/ttyUSB0', help='The path to the serial device (default: /dev/ttyUSB0)')
parser.add_argument('-f', '--file_path', default='kernel8.img', help='The file to send (default: kernel8.img)')
args = parser.parse_args()

if not os.path.exists(args.file_path):
    print(f"File {args.file_path} not found.")
    exit(1)

size = os.stat(args.file_path).st_size
size_bytes = size.to_bytes(4, "little")

with open(args.serial_path, "wb", buffering=0) as tty:
    print(f"Sending size: {size} bytes")
    tty.write(size_bytes)
    time.sleep(1)  # Increased delay
    
    print("Sending kernel...")
    with open(args.file_path, "rb") as f:
        data = f.read()
        # Send in smaller chunks
        chunk_size = 256
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            tty.write(chunk)
            time.sleep(0.01)  # Small delay between chunks
    
    print("Transfer complete")