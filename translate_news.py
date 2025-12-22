import requests
import json
from deep_translator import GoogleTranslator

def fetch_and_translate():
    # 1. 获取原始英文数据
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=730&count=10"
    response = requests.get(url)
    data = response.json()
    
    news_items = data.get('appnews', {}).get('newsitems', [])
    translator = GoogleTranslator(source='en', target='zh-CN')

    for item in news_items:
        try:
            # 翻译标题
            item['title'] = translator.translate(item['title'])
            # 翻译正文（仅翻译前 1000 字符，防止过长导致翻译失败）
            content_snippet = item['contents'][:1000]
            item['contents'] = translator.translate(content_snippet) + "..."
        except Exception as e:
            print(f"翻译失败: {e}")

    # 2. 保存为 news.json
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({"appnews": {"newsitems": news_items}}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_and_translate()
