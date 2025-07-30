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
    
    # Send "boot" command first
    sock.send(b"boot\n")
    time.sleep(0.5)
    
    print(f"Sending size: {size} bytes")
    
    # Send size (4 bytes, one by one to match UART byte-by-byte reading)
    for byte in size_bytes:
        sock.send(bytes([byte]))
        time.sleep(0.01)  # Small delay between bytes
    
    print("Sending kernel...")
    with open(args.file_path, "rb") as f:
        data = f.read()
        # Send byte by byte to match UART reading pattern
        for byte in data:
            sock.send(bytes([byte]))
            time.sleep(0.001)  # Very small delay between bytes
    
    print("Transfer complete")
    
except ConnectionRefusedError:
    print(f"Could not connect to {args.host}:{args.port}")
    print("Make sure QEMU is running with -serial tcp::1234,server,nowait")
except Exception as e:
    print(f"Error: {e}")
finally:
    sock.close()