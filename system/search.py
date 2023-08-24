import requests
from bs4 import BeautifulSoup
from model.user import get_user
from model.search_history import add_search_history, get_search_history

def search_the_web(query):
    user = get_user()

    if (user['collect_data']):
        add_search_history(user['user_id'], query)
    
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

def indepth_inspect(link):
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

    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    page_data["meta_keywords"] = meta_keywords["content"].split(",") if meta_keywords else None
    
    headers = {}
    for h in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        headers[h] = [header.get_text() for header in soup.find_all(h)]
    page_data["headers"] = headers
    
    images = [{"src": img["src"], "alt": img.get("alt", "")} for img in soup.find_all('img') if img.has_attr("src")]
    page_data["images"] = images
    
    internal_links = []
    external_links = []
    for a in soup.find_all('a', href=True):
        if 'http' in a['href']:
            external_links.append(a['href'])
        else:
            internal_links.append(a['href'])
    page_data["internal_links"] = internal_links
    page_data["external_links"] = external_links
    
    scripts = [script["src"] for script in soup.find_all('script') if script.has_attr("src")]
    page_data["scripts"] = scripts
    
    stylesheets = [link["href"] for link in soup.find_all('link') if link.has_attr("rel") and "stylesheet" in link["rel"]]
    page_data["stylesheets"] = stylesheets

    paragraphs = soup.find_all('p')
    page_data["content"] = [p.get_text() for p in paragraphs] if paragraphs else None
    
    return page_data

def reddit_search(query):
    user = get_user()

    if (user['collect_data']):
        add_search_history(user['user_id'], query)
    
    url = f"https://www.reddit.com/search/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for g in soup.find_all('div'):
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














