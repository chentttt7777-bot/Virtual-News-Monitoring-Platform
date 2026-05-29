import requests
from bs4 import BeautifulSoup
from .text_detection import process_text

def get_news_content(url):
    try:
        response = requests.get(url)
        # 设置正确的编码，避免乱码
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 假设新闻正文在 <p> 标签内，根据实际网页结构调整
            paragraphs = soup.find_all('p')
            news_content = []
            for p in paragraphs:
                if p.get_text().strip():
                    news_content.append(p.get_text().strip())
            news_text = '\n'.join(news_content)
            return news_text
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"请求过程中出现错误: {e}")


