import zipfile
import os

def find_flag(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            try:
                with zip_ref.open(file_info.filename) as file:
                    content = file.read()
                    try:
                        # Try to decode as text
                        text_content = content.decode('utf-8')
                        if 'SIG24{' in text_content:
                            print(f"Found flag in {file_info.filename}:")
                            print(text_content[text_content.find('SIG24{'):text_content.find('}')+1])
                    except UnicodeDecodeError:
                        # If file is binary, search raw bytes
                        if b'SIG24{' in content:
                            print(f"Found flag in binary file {file_info.filename}")
                            start = content.find(b'SIG24{')
                            end = content.find(b'}', start)
                            print(content[start:end+1].decode('utf-8'))
            except:
                print(f"Could not read {file_info.filename}")

if __name__ == "__main__":
    zip_path = "../dist/challenge_files.zip"
    find_flag(zip_path)
