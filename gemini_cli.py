import os
import json
import google.generativeai as genai
from datetime import datetime

# Gemini API 설정
API_KEY = "AIzaSyBuwKbtI-_3z2_wJzTPQm5cygukByaXmK8"  # 실제 API 키로 교체하세요
genai.configure(api_key=API_KEY)

def generate_website_content(topic):
    """주제에 대한 웹사이트 콘텐츠를 생성합니다."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""Create a simple HTML website about {topic}. The HTML should include:
    - A proper HTML5 structure with <!DOCTYPE html>
    - A title in the <head> section
    - A main heading (h1) with the topic name
    - A description paragraph about the topic
    - 3 placeholder images with alt text (use placeholder.com or similar)
    - 1 embedded video (use a placeholder video service)
    - Basic CSS styling to make it look good
    - Responsive design
    
    Return only the complete HTML code without any explanations or markdown formatting."""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ {topic}에 대한 콘텐츠 생성 실패: {e}")
        return None

def create_website_files(topic, html_content):
    """웹사이트 파일들을 생성합니다."""
    output_dir = f"web_{topic.replace(' ', '_')}"
    
    # 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # HTML 파일 생성
    html_file = os.path.join(output_dir, "index.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # README 파일 생성
    readme_content = f"""# {topic.title()} Website

This website was automatically generated using Google Gemini AI.

## Files
- `index.html` - Main HTML file

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    readme_file = os.path.join(output_dir, "README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ {topic} 웹사이트 생성 완료: {output_dir}/")
    return output_dir

def main():
    topics = ["cats", "dogs", "birds", "fish", "rabbits", "tigers", "lions", "elephants", "whales", "frogs"]
    
    print("🚀 웹사이트 생성 시작...")
    print(f"📝 총 {len(topics)}개의 주제를 처리합니다.")
    
    successful_sites = []
    failed_topics = []
    
    for i, topic in enumerate(topics, 1):
        print(f"\n📄 [{i}/{len(topics)}] {topic} 웹사이트 생성 중...")
        
        # 콘텐츠 생성
        html_content = generate_website_content(topic)
        
        if html_content:
            # 파일 생성
            output_dir = create_website_files(topic, html_content)
            successful_sites.append(output_dir)
        else:
            failed_topics.append(topic)
            print(f"❌ {topic} 처리 실패")
    
    # 결과 요약
    print(f"\n🎉 웹사이트 생성 완료!")
    print(f"✅ 성공: {len(successful_sites)}개")
    print(f"❌ 실패: {len(failed_topics)}개")
    
    if successful_sites:
        print(f"\n📁 생성된 웹사이트:")
        for site in successful_sites:
            print(f"  - {site}")
    
    if failed_topics:
        print(f"\n⚠️ 실패한 주제:")
        for topic in failed_topics:
            print(f"  - {topic}")

if __name__ == "__main__":
    main()