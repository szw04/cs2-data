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
            # 1. 保留原始英文标题和内容
            item['title_en'] = item.get('title', '')
            item['contents_en'] = item.get('contents', '')
            
            # 2. 翻译并存入中文专用字段
            item['title_cn'] = translator.translate(item['title_en'])
            
            # 限制长度以保证翻译质量，同时保留 [img] 标签
            content_to_process = item['contents_en'][:4000] 
            item['contents_cn'] = translator.translate(content_to_process)
            
        except Exception as e:
            print(f"翻译失败: {e}")
            # 如果翻译失败，确保字段存在以防小程序报错
            item['title_cn'] = item.get('title', '')
            item['contents_cn'] = item.get('contents', '')

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({"appnews": {"newsitems": news_items}}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_and_translate()
