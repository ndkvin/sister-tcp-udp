import os
import argparse

def generate_file(file_name, size_kb):
    size_bytes = size_kb * 1024
    if os.path.exists(file_name):
        print(f"Replacing existing file: {file_name}")
    with open(file_name, 'wb') as f:
        f.write(b'.' * size_bytes)
    print(f"File '{file_name}' generated with size {size_kb} KB.")


parser = argparse.ArgumentParser(description='Generate a numeric file of specified size.')
parser.add_argument('filename', type=str, help='The name of the file to generate.')
parser.add_argument('size_kb', type=int, help='The desired size of the file in KB.')
args = parser.parse_args()
generate_file(args.filename, args.size_kb)