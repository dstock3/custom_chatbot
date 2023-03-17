import requests
from system import config
import json

def get_news():
    url = "https://google-news-api1.p.rapidapi.com/search"
    querystring = {"language": "en"}
    headers = {
        "X-RapidAPI-Key": config.NEWS_API_KEY,
        "X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    news_data = json.loads(response.text)
    result = []

    if news_data.get('success') and news_data.get('news'):
        news_items = news_data['news'].get('news')
        if news_items:
            for idx, news_item in enumerate(news_items):
                if idx < 5:
                    result.append({
                        'title': news_item['title'],
                        'description': news_item['description']
                    })
                else:
                    break
        else:
            print("No news found.")
    else:
        print("No news found.")
    print(result)
    return result



