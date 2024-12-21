import os
import re
import zipfile
from collections import Counter
from contextlib import contextmanager

class FlagCounter:
    def __init__(self, flag_pattern=r"SIG24\{[a-zA-Z0-9_]+\}"):
        self.flag_pattern = re.compile(flag_pattern)
        
    @contextmanager
    def temp_extract_dir(self, path="./extracted_content"):
        os.makedirs(path, exist_ok=True)
        try:
            yield path
        finally:
            self._cleanup_dir(path)
    
    def _cleanup_dir(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(path)
    
    def find_least_common_flag(self, dir_path):
        flag_counts = Counter()
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        flags = self.flag_pattern.findall(f.read())
                        flag_counts.update(flags)
                except (IOError, UnicodeDecodeError):
                    continue
                    
        return min(flag_counts.items(), key=lambda x: x[1]) if flag_counts else (None, 0)

    def count_specific_flag(self, dir_path, target_flag):
        flag_counts = Counter()
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        flags = self.flag_pattern.findall(f.read())
                        flag_counts.update(flags)
                except (IOError, UnicodeDecodeError):
                    continue
                    
        return flag_counts[target_flag]

def solve_zip(zip_path, specific_flag=None):
    counter = FlagCounter()
    
    try:
        with counter.temp_extract_dir() as extract_path:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            if specific_flag:
                count = counter.count_specific_flag(extract_path, specific_flag)
                return specific_flag, count
            return counter.find_least_common_flag(extract_path)
    except zipfile.BadZipFile:
        return None, 0

if __name__ == "__main__":
    zip_path = '../dist/countingflags.zip'
    user_flag = input("Enter a specific flag to count (press Enter to find least common): ").strip()
    
    if user_flag:
        flag, count = solve_zip(zip_path, user_flag)
        print(f"Count for flag {flag}: {count}")
    else:
        flag, count = solve_zip(zip_path)
        print(f"Least common flag: {flag}, Count: {count}")