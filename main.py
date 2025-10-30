#!/usr/bin/env python3
#_*-_ coding: utf-8 _*_


###  Leonel Version
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup  
import json
import os

url =  ['https://scholar.google.com/scholar?q=', 'https://www.acm.org/search#stq=', 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=']
subjet_search = "proximal policy optimization ppo"
encoded_search = urllib.parse.quote_plus(subjet_search)


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
headers = {'User-Agent': user_agent}

logs_json = []
avoid_duplicates = []

file_name = 'results_google_scholar.json'



def fetch_url(url_index):
    """Realiza la consulta HTTP con la URL y User-Agent."""
    
    
    if url_index == 0:  # Google Scholar
        full_url = url[0] + encoded_search
    elif url_index == 1:  # IEE Xplore
        full_url = url[1] + encoded_search 
    elif url_index == 2:  # ACM
        full_url = url[2] + encoded_search
    
    print(f"\n--- Consultando en: {full_url}")
    
    req = urllib.request.Request(full_url, headers=headers)
    
    try:
        consult = urllib.request.urlopen(req)
        consult_bytes = consult.read()
        consult_html = consult_bytes.decode('utf-8')
        print(f"Conexión exitosa con {full_url}.")
        return consult_html
    
    except urllib.error.HTTPError as e:
        print(f"Error HTTP en {full_url}: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"Error de URL en {full_url}: {e.reason}")
    except Exception as e:
        print(f"Error desconocido al consultar {full_url}: {e}")
        
    return None


def google_scholar(): 
        
        file_web = open("schoolargoogle.html", "w+", encoding='utf-8')
    
        consult_html = fetch_url(0)
    
        print("Connection succesful. First 50 characters:")
        print(consult_html[:50])

        file_web.write(str(consult_html))
        file_web.close()

        html= open("schoolargoogle.html", "r+", encoding='utf-8')
        soup = BeautifulSoup(html, 'html.parser')
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
                'source': 'Google Scholar',
                'title': title,
                'link': link,
                'authors': citations
            }

            logs_json.append(log)
        #with open('results_google_scholar.json', 'w', encoding='utf-8') as f:
            #json.dump(logs_json, f, ensure_ascii=False, indent=4)
      
        """
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
            """

def ieee():
    full_url = url[1] + encoded_search
    html_content = fetch_url(1)
    if not html_content:
        return
    

    


def acm():
    full_url = url[2] + encoded_search 
    html_content = fetch_url(2)
    if not html_content:
        return
    file_web = open("acm.html", "w+", encoding='utf-8')
    file_web.write(str(html_content))
    file_web.close()
    html= open("acm.html", "r+", encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    class_searched = 'issue-item__content' 
    result = soup.find_all('div', class_=class_searched)

    for line in result:
        title_tag = line.find('h5', class_='issue-item__title')
        title = title_tag.text.strip() if title_tag else "ACM Title N/A"
        
        link_tag = line.find('a')
        link = "https://dl.acm.org" + link_tag['href'] if link_tag and link_tag.get('href') else "ACM Link N/A"
        
        authors_tag = line.find('div', class_='issue-item__content-authors')
        authors = authors_tag.text.strip() if authors_tag else "ACM Authors N/A"
        
        log = {
            'site': 'ACM',
            'title': title,
            'link': link,
            'authors': authors
        }
        logs_json.append(log)
    print(f"   -> {len(result)} resultados añadidos (ACM).")


if __name__ == '__main__':
    #google_scholar()
    ieee()
    #acm()


resultados_existentes = []
nuevos_a_añadir = []
titulos_existentes = set()
count_duplicados = 0

if os.path.exists(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        try:
            resultados_existentes = json.load(f)
            # 2.1. Crear set de títulos existentes
            titulos_existentes = {item['title'] for item in resultados_existentes}
        except json.JSONDecodeError:
            print("Archivo JSON corrupto o vacío. Reiniciando log.")
            resultados_existentes = []
            
# 2.2. Filtrar logs_json (que contiene los nuevos resultados de todas las funciones)
for article in logs_json:
    if article['title'] not in titulos_existentes:
        nuevos_a_añadir.append(article)
        titulos_existentes.add(article['title']) # Prevenir duplicados en la misma ejecución
    else:
        count_duplicados += 1

# 2.3. Unir y Guardar
resultados_existentes.extend(nuevos_a_añadir)

with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(resultados_existentes, f, ensure_ascii=False, indent=4)

print(f"\n--- RESUMEN FINAL ---")
print(f"Se omitieron {count_duplicados} duplicados.")
print(f"Se añadieron {len(nuevos_a_añadir)} registros nuevos.")
print(f"Total de registros en '{file_name}': {len(resultados_existentes)}")