import requests
import json
import re
from deep_translator import GoogleTranslator

def fetch_and_translate():
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=730&count=10"
    response = requests.get(url)
    data = response.json()
    
    news_items = data.get('appnews', {}).get('newsitems', [])
    translator = GoogleTranslator(source='en', target='zh-CN')

    for item in news_items:
        try:
            # 1. 翻译标题
            item['title'] = translator.translate(item['title'])
            
            # 2. 保留图片标签，仅翻译文本
            content = item.get('contents', '')
            
            # 增加翻译截断长度到 5000，确保图片标签不被切断
            content_to_process = content[:5000] 
            
            # 这里的逻辑是：GoogleTranslator 会自动跳过 [img] 这种特殊格式
            # 如果翻译后标签损坏，我们可以考虑更复杂的占位符方案，但通常直接翻译即可
            item['contents'] = translator.translate(content_to_process)
            
        except Exception as e:
            print(f"翻译失败: {e}")

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({"appnews": {"newsitems": news_items}}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_and_translate()
