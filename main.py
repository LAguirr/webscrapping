#!/usr/bin/env python3
#_*-_ coding: utf-8 _*_


###  Leonel Version
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup  
import json
import os

url =  'https://scholar.google.com/scholar?q='
subjet_search = "proximal policy optimization ppo"
encoded_search = urllib.parse.quote_plus(subjet_search)
full_url = url + encoded_search
print(full_url)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
headers = {'User-Agent': user_agent}

logs_json = []
avoid_duplicates = []

file_name = 'results_google_scholar.json'
def main():

        file_web = open("schoolargoogle.html", "w+", encoding='utf-8')
        req = urllib.request.Request(full_url, headers={'User-Agent': user_agent})
        consult = urllib.request.urlopen(req)
        consult_bytes = consult.read()
    
        consult_html = consult_bytes.decode('utf-8')
    
        print("Connection succesful. First 50 characters:")
        print(consult_html[:50])

        file_web.write(str(consult_bytes.decode('utf-8')))
        file_web.close()

        html= open("schoolargoogle.html", "r+")
        soup = BeautifulSoup(consult_html, 'html.parser')
        class_searched = 'gs_r gs_or gs_scl'
        result = soup.find_all('div', class_=class_searched)
    
        for i, line in enumerate(result):
            
            title_tag = line.find('h3', class_='gs_rt')
            title = title_tag.text if title_tag else "N/A"
            
            link_tag = line.find('a')
            link = link_tag['href'] if link_tag else "N/A"

            citations_tag = line.find('div', class_='gs_a')
            citations = citations_tag.text if citations_tag else "N/A"
            
            print(f"\n--- Result {i+1} ---")
            print(f"Title: {title}")
            print(f"Link: {link}")
            print(f"Authors: {citations}")

            log = {
                'title': title,
                'link': link,
                'authors': citations
            }

            logs_json.append(log)
        #with open('results_google_scholar.json', 'w', encoding='utf-8') as f:
            #json.dump(logs_json, f, ensure_ascii=False, indent=4)
      

        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                try:
                    file = json.load(f)

                    # Avoid duplicates based on title
                    titles = {item['title'] for item in file}

                except json.JSONDecodeError:
                    file = []
        else: 
            with open(file_name, 'w', encoding='utf-8') as f:
                file = []
                json.dump(file, f, ensure_ascii=False, indent=4)
            titles = set()


        for article in logs_json:
            if article['title'] not in titles:
                avoid_duplicates.append(article)
                titles.add(article['title'])

        file.extend(avoid_duplicates)

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(file, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()

