import requests
import json
import re
from deep_translator import GoogleTranslator

def clean_bbcode(text):
    # 预处理：删除 [img]...[/img] 标签，因为它们包含长链接且不需要翻译
    text = re.sub(r'\[img\].*?\[/img\]', '', text)
    # 删除视频标签
    text = re.sub(r'\[video.*?\][\s\S]*?\[\/video\]', '', text)
    return text

def fetch_and_translate():
    url = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=730&count=10"
    response = requests.get(url)
    data = response.json()
    
    news_items = data.get('appnews', {}).get('newsitems', [])
    translator = GoogleTranslator(source='en', target='zh-CN')

    for item in news_items:
        try:
            # 翻译标题
            item['title'] = translator.translate(item['title'])
            
            # 核心优化：先清洗掉干扰标签再翻译
            original_content = item.get('contents', '')
            cleaned_content = clean_bbcode(original_content)
            
            # 放宽限制到 2500 字符，确保内容完整性
            content_to_translate = cleaned_content[:2500] 
            
            item['contents'] = translator.translate(content_to_translate)
        except Exception as e:
            print(f"翻译失败: {e}")

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump({"appnews": {"newsitems": news_items}}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_and_translate()
