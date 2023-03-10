import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from heapq import nlargest

def get_news_summaries(sources):
    news_summaries = []
    for source in sources:
        url = f"https://news.google.com/rss/search?q={source}&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll('item')
        
        for item in items:
            news = {}
            news['source'] = source
            news['link'] = item.link.text
            news['title'] = item.title.text
            news['pubDate'] = item.pubDate.text
            news['description'] = item.description.text

            print(news)

            # Summarize the article
            article_response = requests.get(news['link'])
            article_soup = BeautifulSoup(article_response.content, features="html.parser")
            article_text = ' '.join(map(lambda p: p.text, article_soup.find_all('p')))
            article_sentences = sent_tokenize(article_text)
            stop_words = set(stopwords.words('english'))
            sentence_scores = {}
            for sentence in article_sentences:
                for word in sentence.lower().split():
                    if word in stop_words:
                        continue
                    if sentence in sentence_scores:
                        sentence_scores[sentence] += 1
                    else:
                        sentence_scores[sentence] = 1
            summary_sentences = nlargest(3, sentence_scores, key=sentence_scores.get)
            news['summary'] = ' '.join(summary_sentences)

            news_summaries.append(news)
    return news_summaries