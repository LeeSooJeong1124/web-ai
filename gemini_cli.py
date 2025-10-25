import os
import json
import google.generativeai as genai
from datetime import datetime

# Gemini API 설정
API_KEY = "AIzaSyBuwKbtI-_3z2_wJzTPQm5cygukByaXmK8"  # 실제 API 키로 교체하세요
genai.configure(api_key=API_KEY)

def generate_website_content(topic):
    """주제에 대한 웹사이트 콘텐츠를 생성합니다."""
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    prompt = f"""Create a simple HTML website about {topic}.
                The website should have the following structure and behavior:
                    •	The site has three HTML files:
                    •	index.html: main page
                    •	image/image.html: image gallery page
                    •	video/video.html: video page
                    •	index.html should include:
                    •	Proper HTML5 structure with <!DOCTYPE html>
                    •	<head> section with a title
                    •	A main heading (<h1>) showing the topic name
                    •	A short description paragraph about the topic
                    •	Two buttons:
                    •	“View Images” → navigates to image/image.html
                    •	“View Video” → navigates to video/video.html
                    •	Basic CSS styling (centered layout, soft background, hover effects)
                    •	Responsive design
                    •	image/image.html should include:
                    •	Proper HTML5 structure
                    •	A heading like “{topic} Image Gallery”
                    •	Three <img> elements that load local images from the image/ folder
                (e.g., image1.jpg, image2.png, image3.jpg)
                    •	Each image must have appropriate alt text
                    •	A “Back to Home” button that returns to ../index.html
                    •	video/video.html should include:
                    •	Proper HTML5 structure
                    •	A heading like “{topic} Video”
                    •	An embedded <video> tag that loads a local .mp4 file from the video/ folder (e.g., video.mp4)
                with controls enabled
                    •	A “Back to Home” button that returns to ../index.html
                    •	Include consistent and simple CSS styling across all pages
                    •	Return only the complete HTML code for all three files (index.html, image/image.html, and video/video.html) without any explanations or markdown formatting.
                """
                    
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
    topics = ["cats", "dogs", "birds", "fish"]#, "rabbits", "tigers", "lions", "elephants", "whales", "frogs"]
    
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