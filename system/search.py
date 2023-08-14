import requests
from bs4 import BeautifulSoup

def search_the_web(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            item = {
                "title": title,
                "link": link
            }
            results.append(item)
    results = str(results)
    return results

def inspect(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    page_data = {}
    
    title = soup.title.string if soup.title else None
    page_data["title"] = title
    
    meta_description = soup.find('meta', attrs={'name': 'description'})
    page_data["meta_description"] = meta_description["content"] if meta_description else None
    
    paragraphs = soup.find_all('p')
    page_data["initial_content"] = [p.get_text() for p in paragraphs[:5]] if paragraphs else None
    
    return page_data














