import os
import json
import google.generativeai as genai
from datetime import datetime

# Gemini API 설정
API_KEY = ""  # 실제 API 키로 교체하세요
genai.configure(api_key=API_KEY)

def generate_website_content(topic):
    """주제에 대한 웹사이트 콘텐츠를 생성합니다."""
    # Gemini API를 사용하지 않고 직접 HTML 파일들을 생성
    return "DIRECT_GENERATION"
                    
def create_website_files(topic, html_content):
    """웹사이트 파일들을 생성합니다."""
    output_dir = f"web_{topic.replace(' ', '_')}"
    
    # 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "image"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "video"), exist_ok=True)
    
    # 직접 HTML 파일들 생성
    create_direct_html_files(topic, output_dir)
    
    files_created = ["index.html", "image/image.html", "video/video.html"]
    
    # README 파일 생성
    readme_content = f"""# {topic.title()} Website

This website was automatically generated using Python.

## Files
- `index.html` - Main page
- `image/image.html` - Image gallery page  
- `video/video.html` - Video page

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    readme_file = os.path.join(output_dir, "README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ {topic} 웹사이트 생성 완료: {output_dir}/")
    for file in files_created:
        print(f"   - {file}")
    return output_dir

def create_direct_html_files(topic, output_dir):
    """직접 HTML 파일들을 생성합니다."""
    
    # index.html 생성
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic.title()} - Home</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
        }}
        .container {{ 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 40px 20px; 
            text-align: center; 
        }}
        h1 {{ 
            color: white; 
            font-size: 3.5em; 
            margin-bottom: 20px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
            font-weight: 300;
        }}
        p {{ 
            color: white; 
            font-size: 1.3em; 
            margin-bottom: 50px; 
            line-height: 1.6; 
            opacity: 0.9;
        }}
        .buttons {{ 
            display: flex; 
            gap: 30px; 
            justify-content: center; 
            flex-wrap: wrap; 
        }}
        .btn {{ 
            padding: 18px 35px; 
            background: rgba(255,255,255,0.15); 
            color: white; 
            text-decoration: none; 
            border-radius: 30px; 
            font-size: 1.2em; 
            transition: all 0.3s ease; 
            border: 2px solid rgba(255,255,255,0.3); 
            backdrop-filter: blur(10px);
        }}
        .btn:hover {{ 
            background: rgba(255,255,255,0.25); 
            transform: translateY(-3px); 
            box-shadow: 0 8px 25px rgba(0,0,0,0.2); 
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic.title()}</h1>
        <p>Welcome to our amazing {topic} website! Discover fascinating facts, beautiful images, and exciting videos about {topic}.</p>
        <div class="buttons">
            <a href="image/image.html" class="btn">🖼️ View Images</a>
            <a href="video/video.html" class="btn">🎥 View Video</a>
        </div>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # image/image.html 생성
    image_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic.title()} Image Gallery</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
        }}
        h1 {{ 
            color: #333; 
            text-align: center; 
            margin-bottom: 40px; 
            font-size: 2.5em;
            font-weight: 300;
        }}
        .gallery {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 30px; 
            margin-bottom: 40px;
        }}
        .image {{ 
            text-align: center; 
            background: white; 
            padding: 25px; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); 
            transition: transform 0.3s ease;
        }}
        .image:hover {{
            transform: translateY(-5px);
        }}
        .image img {{ 
            max-width: 100%; 
            height: 250px; 
            object-fit: cover; 
            border-radius: 10px; 
            margin-bottom: 15px;
        }}
        .image p {{
            color: #666;
            font-size: 1.1em;
            margin: 0;
        }}
        .back-btn {{ 
            display: inline-block; 
            margin-top: 30px; 
            padding: 15px 30px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            text-decoration: none; 
            border-radius: 25px; 
            font-size: 1.1em;
            transition: all 0.3s ease;
        }}
        .back-btn:hover {{ 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic.title()} Image Gallery</h1>
        <div class="gallery">
            <div class="image">
                <img src="https://picsum.photos/400/300?random=1" alt="Beautiful {topic}">
                <p>Amazing {topic} in nature</p>
            </div>
            <div class="image">
                <img src="https://picsum.photos/400/300?random=2" alt="Cute {topic}">
                <p>Adorable {topic} close-up</p>
            </div>
            <div class="image">
                <img src="https://picsum.photos/400/300?random=3" alt="Wild {topic}">
                <p>Wild {topic} in action</p>
            </div>
        </div>
        <div style="text-align: center;">
            <a href="../index.html" class="back-btn">← Back to Home</a>
        </div>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, "image", "image.html"), 'w', encoding='utf-8') as f:
        f.write(image_html)
    
    # video/video.html 생성
    video_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic.title()} Video</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 900px; 
            margin: 0 auto; 
        }}
        h1 {{ 
            color: #333; 
            text-align: center; 
            margin-bottom: 40px; 
            font-size: 2.5em;
            font-weight: 300;
        }}
        .video-container {{ 
            text-align: center; 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); 
            margin-bottom: 30px;
        }}
        video {{ 
            max-width: 100%; 
            height: auto; 
            border-radius: 10px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .video-container p {{
            color: #666;
            font-size: 1.2em;
            margin-top: 20px;
        }}
        .back-btn {{ 
            display: inline-block; 
            margin-top: 30px; 
            padding: 15px 30px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            text-decoration: none; 
            border-radius: 25px; 
            font-size: 1.1em;
            transition: all 0.3s ease;
        }}
        .back-btn:hover {{ 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic.title()} Video</h1>
        <div class="video-container">
            <video controls>
                <source src="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <p>Watch this amazing video about {topic}!</p>
        </div>
        <div style="text-align: center;">
            <a href="../index.html" class="back-btn">← Back to Home</a>
        </div>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, "video", "video.html"), 'w', encoding='utf-8') as f:
        f.write(video_html)

def create_website_files(topic, html_content):
    """웹사이트 파일들을 생성합니다."""
    output_dir = f"web_{topic.replace(' ', '_')}"
    
    # 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "image"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "video"), exist_ok=True)
    
    # Gemini 응답에서 HTML 파일들을 분리
    files_created = []
    
    # FILE 1, FILE 2, FILE 3으로 분리
    if "FILE 1 - index.html:" in html_content:
        # index.html 추출
        start = html_content.find("FILE 1 - index.html:")
        end = html_content.find("FILE 2 - image/image.html:")
        if end == -1:
            end = len(html_content)
        
        index_content = html_content[start:end].replace("FILE 1 - index.html:", "").strip()
        index_file = os.path.join(output_dir, "index.html")
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        files_created.append("index.html")
    
    if "FILE 2 - image/image.html:" in html_content:
        # image.html 추출
        start = html_content.find("FILE 2 - image/image.html:")
        end = html_content.find("FILE 3 - video/video.html:")
        if end == -1:
            end = len(html_content)
        
        image_content = html_content[start:end].replace("FILE 2 - image/image.html:", "").strip()
        image_file = os.path.join(output_dir, "image", "image.html")
        with open(image_file, 'w', encoding='utf-8') as f:
            f.write(image_content)
        files_created.append("image/image.html")
    
    if "FILE 3 - video/video.html:" in html_content:
        # video.html 추출
        start = html_content.find("FILE 3 - video/video.html:")
        video_content = html_content[start:].replace("FILE 3 - video/video.html:", "").strip()
        video_file = os.path.join(output_dir, "video", "video.html")
        with open(video_file, 'w', encoding='utf-8') as f:
            f.write(video_content)
        files_created.append("video/video.html")
    
    # 만약 Gemini가 제대로 분리하지 못했다면 기본 파일들 생성
    if len(files_created) == 0:
        create_default_files(topic, output_dir)
        files_created = ["index.html", "image/image.html", "video/video.html"]
    
    # README 파일 생성
    readme_content = f"""# {topic.title()} Website

This website was automatically generated using Google Gemini AI.

## Files
- `index.html` - Main page
- `image/image.html` - Image gallery page  
- `video/video.html` - Video page

## Generated on
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    readme_file = os.path.join(output_dir, "README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ {topic} 웹사이트 생성 완료: {output_dir}/")
    for file in files_created:
        print(f"   - {file}")
    return output_dir

def create_default_files(topic, output_dir):
    """기본 HTML 파일들을 생성합니다."""
    # image/image.html
    image_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic.title()} Image Gallery</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #333; text-align: center; }}
        .image-gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .image {{ text-align: center; }}
        .image img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .back-btn {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        .back-btn:hover {{ background: #0056b3; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic.title()} Image Gallery</h1>
        <div class="image-gallery">
            <div class="image">
                <img src="https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text={topic.title()}+Image+1" alt="{topic.title()} Image 1">
            </div>
            <div class="image">
                <img src="https://via.placeholder.com/300x200/4ECDC4/FFFFFF?text={topic.title()}+Image+2" alt="{topic.title()} Image 2">
            </div>
            <div class="image">
                <img src="https://via.placeholder.com/300x200/45B7D1/FFFFFF?text={topic.title()}+Image+3" alt="{topic.title()} Image 3">
            </div>
        </div>
        <a href="../index.html" class="back-btn">Back to Home</a>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, "image", "image.html"), 'w', encoding='utf-8') as f:
        f.write(image_html)
    
    # video/video.html
    video_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic.title()} Video</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #333; text-align: center; }}
        .video-container {{ text-align: center; margin: 20px 0; }}
        video {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .back-btn {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        .back-btn:hover {{ background: #0056b3; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{topic.title()} Video</h1>
        <div class="video-container">
            <video controls>
                <source src="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <a href="../index.html" class="back-btn">Back to Home</a>
    </div>
</body>
</html>"""
    
    with open(os.path.join(output_dir, "video", "video.html"), 'w', encoding='utf-8') as f:
        f.write(video_html)

def main():
    topics = ["cats"]#, "dogs", "birds", "fish", "rabbits", "tigers", "lions", "elephants", "whales", "frogs"]
    
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