import os
import os.path
import argparse
import time
import socket

parser = argparse.ArgumentParser(description='Send a file over TCP connection.')
parser.add_argument('--host', default='localhost', help='The host to connect to (default: localhost)')
parser.add_argument('-p', '--port', type=int, default=1234, help='The port to connect to (default: 1234)')
parser.add_argument('-f', '--file_path', default='kernel8.img', help='The file to send (default: kernel8.img)')
args = parser.parse_args()

if not os.path.exists(args.file_path):
    print(f"File {args.file_path} not found.")
    exit(1)

size = os.stat(args.file_path).st_size
size_bytes = size.to_bytes(4, "little")

try:
    # Create TCP socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))
    
    print(f"Connected to {args.host}:{args.port}")
    print(f"Sending size: {size} bytes")
    
    # Send size first
    sock.send(size_bytes)
    time.sleep(1)  # Delay after sending size
    
    print("Sending kernel...")
    with open(args.file_path, "rb") as f:
        data = f.read()
        # Send in smaller chunks
        chunk_size = 256
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i+chunk_size]
            sock.send(chunk)
            time.sleep(0.01)  # Small delay between chunks
    
    print("Transfer complete")
    
except ConnectionRefusedError:
    print(f"Could not connect to {args.host}:{args.port}")
    print("Make sure QEMU is running with -serial tcp::1234,server,nowait")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()