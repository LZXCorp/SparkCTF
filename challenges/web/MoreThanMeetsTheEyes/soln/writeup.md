# Web Scraping challenge writeup

## Context of challenge:
The python source code generates a website which stores 5000 items. There is a hidden javascript API call in one of the items. Calling this will reveal the flag (with the right parameters). 

## Solution Steps:

To obtain the flag, a web scraper should be used to quickly parse through all of the hidden data. This is as manually sorting through the 5000 pages using inspect element is not efficient. This can be done using python code to load html and make API calls. 

By creating a python script that sends requests to parse through every page, highlighting terms such as `<script>`, `fetch` or `/api`, it is possible to discover the hidden API route. 

To obtain the flag, the discovered api route should be called. The simplest is to do this is via the browser. This reveals that the API format is correct, but the parameter has to be determined. 

Therefore, to automate the process, python can be used again to automatically modify the ID of the API call to reveal the flag. 



## Answers

This is the minimum steps required to reveal the flag

`http://localhost:24680/api/hidden-data?id=4777`\
This reveals is the API call format

`http://localhost:24680/api/hidden-data?id=2119`\
This reveals the flag


Sample python code to generate minimum solution:

```python
import requests, re

BASE = "http://localhost:24680"
MAX_PAGES = 5000
FLAG_PREFIX = "SPARK{"


apiLIST = []



def probe_api(api_path, start=0, end=5000):
    flags = []

    for i in range(start, end):
        url = f"{BASE}{api_path}?id={i}"
        try:
            r = requests.get(url, timeout=5)
            text = r.text.strip()
            print(f"[{i}] {text}")

            if FLAG_PREFIX in text:
                return text

        except Exception as e:
            print(f"[{i}] Error: {e}")



for page in range(0, MAX_PAGES + 1):
    url = f"{BASE}/items?page={page}"
    try:
        r = requests.get(url, timeout=5)
        html = r.text
        print(f"\n--- Page {page} ({len(html)} bytes) ---")

        # Print any discovered API routes
        if 'fetch' in html:
            html = html.split('fetch(\'')[1]
            apiLIST.append(html)
            

        # Highlight possible flag
        if FLAG_PREFIX in html:
            print(f"[FLAG?] {re.search(r'SPARK{.*?}', html).group()}")

        # Stop early if page looks empty
        if len(html.strip()) < 50:
            print("[!] Empty page, stopping.")
            break
        
        
    except Exception as e:
        print(f"[!] Error fetching page {page}: {e}")
        break

print(apiLIST)



for x in apiLIST:
    x = x.split('?')[0]
    print(x)
    print(probe_api(x))
```
