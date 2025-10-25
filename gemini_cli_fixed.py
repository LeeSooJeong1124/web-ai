import os
import json
import google.generativeai as genai
from datetime import datetime
import requests
import time

# API 키 설정
GEMINI_API_KEY = ""  # Gemini API 키
UNSPLASH_ACCESS_KEY = ""  # Unsplash API 키 (https://unsplash.com/developers)
PIXABAY_API_KEY = ""  # Pixabay API 키 (https://pixabay.com/api/docs/)

# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)

# 기존 LLM topic 생성 함수 (주석처리)
# def generate_topics_with_llm(num_topics=100):
#     """LLM을 사용해서 다양한 topic들을 자동 생성합니다."""
#     model = genai.GenerativeModel('gemini-2.0-flash')
#     
#     prompt = f"""You must respond with ONLY a valid JSON array containing exactly {num_topics} topics.
#
#     Generate {num_topics} diverse and interesting topics for creating websites. 
#
#     Requirements:
#     - Each topic should be a single word or short phrase (1-3 words)
#     - Topics should be interesting and engaging for general audiences
#     - Suitable for creating image galleries and video content
#     - Include diverse categories: animals, nature, technology, food, sports, art, music, travel, science, etc.
#     - Avoid topics that might be inappropriate or controversial
#     - Make topics specific enough to find good images and videos
#
#     Examples of good topics: "cats", "mountains", "robots", "pizza", "soccer", "sunset", "coffee", "books", "flowers", "cars"
#
#     CRITICAL: You must respond with ONLY a JSON array. No explanations, no markdown, no additional text.
#     Format: ["topic1", "topic2", "topic3", ...]
#     
#     Generate exactly {num_topics} topics."""
#     
#     try:
#         response = model.generate_content(prompt)
#         topics_text = response.text.strip()
#         
#         # JSON 파싱 (마크다운 코드 블록 제거)
#         if topics_text.startswith('```json'):
#             # 마크다운 코드 블록에서 JSON 추출
#             topics_text = topics_text.replace('```json', '').replace('```', '').strip()
#         
#         if topics_text.startswith('[') and topics_text.endswith(']'):
#             topics = json.loads(topics_text)
#             print(f"✅ LLM이 {len(topics)}개의 topic을 생성했습니다.")
#             return topics
#         else:
#             print("❌ LLM 응답이 JSON 형식이 아닙니다. 기본 topic을 사용합니다.")
#             print(f"실제 응답: {topics_text[:100]}...")
#             return ["cats", "dogs", "birds", "fish", "mountains", "ocean", "space", "robots", "pizza", "soccer"]
#             
#     except Exception as e:
#         print(f"❌ LLM topic 생성 실패: {e}")
#         return ["cats", "dogs", "birds", "fish", "mountains", "ocean", "space", "robots", "pizza", "soccer"]

def load_fixed_topics():
    """고정된 topic 리스트를 로드합니다."""
    try:
        with open('generated_topics.json', 'r') as f:
            topics = json.load(f)
        print(f"✅ 고정된 {len(topics)}개의 topic을 로드했습니다.")
        return topics
    except FileNotFoundError:
        print("❌ generated_topics.json 파일을 찾을 수 없습니다. 기본 topic을 사용합니다.")
        return ["cats", "dogs", "birds", "fish", "mountains", "ocean", "space", "robots", "pizza", "soccer"]
    except Exception as e:
        print(f"❌ topic 로드 실패: {e}")
        return ["cats", "dogs", "birds", "fish", "mountains", "ocean", "space", "robots", "pizza", "soccer"]

def search_images_for_topic(topic):
    """특정 topic에 대한 이미지 URL을 검색합니다."""
    try:
        # Unsplash API 키 확인
        if not UNSPLASH_ACCESS_KEY or UNSPLASH_ACCESS_KEY == "":
            print("⚠️ Unsplash API 키가 설정되지 않았습니다. fallback 이미지를 사용합니다.")
            return get_fallback_images(topic)
        
        # Unsplash API를 사용하여 이미지 검색
        url = f"https://api.unsplash.com/search/photos"
        params = {
            'query': topic,
            'per_page': 3,
            'orientation': 'landscape'
        }
        headers = {
            'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            images = []
            for photo in data['results'][:3]:
                images.append(photo['urls']['regular'])
            return images
        else:
            print(f"⚠️ Unsplash API 오류: {response.status_code}")
            return get_fallback_images(topic)
            
    except Exception as e:
        print(f"⚠️ 이미지 검색 실패: {e}")
        return get_fallback_images(topic)

def get_fallback_images(topic):
    """API 실패 시 사용할 기본 이미지들"""
    fallback_images = {
        "cats": [
            "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"
        ],
        "dogs": [
            "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1547407139-3c921a71905c?w=400&h=300&fit=crop"
        ],
        "birds": [
            "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=300&fit=crop"
        ],
        "fish": [
            "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=300&fit=crop"
        ],
        "mountains": [
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1464822759844-d150baecf5b1?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop"
        ],
        "ocean": [
            "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=300&fit=crop"
        ],
        "space": [
            "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=400&h=300&fit=crop"
        ],
        "robots": [
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=300&fit=crop"
        ],
        "pizza": [
            "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop"
        ],
        "soccer": [
            "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=300&fit=crop",
            "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=400&h=300&fit=crop"
        ]
    }
    
    # 기본 이미지들 (범용)
    default_images = [
        "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&h=300&fit=crop",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop",
        "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=300&fit=crop"
    ]
    
    return fallback_images.get(topic.lower(), default_images)

def search_video_for_topic(topic):
    """특정 topic에 대한 비디오 URL을 검색합니다."""
    try:
        # Pixabay API 키 확인
        if not PIXABAY_API_KEY or PIXABAY_API_KEY == "":
            print("⚠️ Pixabay API 키가 설정되지 않았습니다. fallback 비디오를 사용합니다.")
            return get_fallback_video(topic)
        
        # Pixabay API를 사용하여 비디오 검색
        url = "https://pixabay.com/api/videos/"
        params = {
            'key': PIXABAY_API_KEY,
            'q': topic,
            'per_page': 1,
            'min_duration': 10,
            'max_duration': 60
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['hits']:
                video_url = data['hits'][0]['videos']['medium']['url']
                return video_url
            else:
                return get_fallback_video(topic)
        else:
            print(f"⚠️ Pixabay API 오류: {response.status_code}")
            return get_fallback_video(topic)
            
    except Exception as e:
        print(f"⚠️ 비디오 검색 실패: {e}")
        return get_fallback_video(topic)

def get_fallback_video(topic):
    """API 실패 시 사용할 기본 비디오들"""
    fallback_videos = {
        "cats": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "dogs": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "birds": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "fish": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "mountains": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "ocean": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
        "space": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
        "robots": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "pizza": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "soccer": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
    }
    
    return fallback_videos.get(topic.lower(), "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

def create_website_files(topic):
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

def get_topic_media_urls(topic):
    """주제에 맞는 이미지와 비디오 URL을 자동으로 검색합니다."""
    print(f"🔍 {topic}에 대한 미디어 검색 중...")
    
    # 이미지 검색
    images = search_images_for_topic(topic)
    
    # 비디오 검색
    video = search_video_for_topic(topic)
    
    return {
        "images": images,
        "video": video
    }

def create_direct_html_files(topic, output_dir):
    """직접 HTML 파일들을 생성합니다."""
    
    # 주제에 맞는 미디어 URL 가져오기
    media_urls = get_topic_media_urls(topic)
    
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
                <img src="{media_urls['images'][0]}" alt="Beautiful {topic}">
                <p>Amazing {topic} in nature</p>
            </div>
            <div class="image">
                <img src="{media_urls['images'][1]}" alt="Cute {topic}">
                <p>Adorable {topic} close-up</p>
            </div>
            <div class="image">
                <img src="{media_urls['images'][2]}" alt="Wild {topic}">
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
                <source src="{media_urls['video']}" type="video/mp4">
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

def main():
    print("🤖 고정 Topic 기반 자동 웹사이트 생성기")
    print("=" * 50)
    
    # 고정된 topic 로드
    print("📂 고정된 topic을 로드 중...")
    topics = load_fixed_topics()[:50]
    
    print(f"📝 총 {len(topics)}개의 주제를 처리합니다.")
    print(f"처리할 topics: {topics[:5]}...")  # 처음 5개만 표시
    
    # API 키 상태 확인
    print("\n🔑 API 키 상태:")
    if UNSPLASH_ACCESS_KEY and UNSPLASH_ACCESS_KEY != "":
        print("✅ Unsplash API 키: 설정됨")
    else:
        print("⚠️ Unsplash API 키: 미설정 (fallback 이미지 사용)")
    
    if PIXABAY_API_KEY and PIXABAY_API_KEY != "":
        print("✅ Pixabay API 키: 설정됨")
    else:
        print("⚠️ Pixabay API 키: 미설정 (fallback 비디오 사용)")
    
    print("\n💡 API 키를 설정하려면:")
    print("   - Unsplash: https://unsplash.com/developers")
    print("   - Pixabay: https://pixabay.com/api/docs/")
    print("   - 코드 상단의 UNSPLASH_ACCESS_KEY, PIXABAY_API_KEY 변수에 키를 입력하세요.")
    
    successful_sites = []
    failed_topics = []
    
    for i, topic in enumerate(topics, 1):
        print(f"\n📄 [{i}/{len(topics)}] {topic} 웹사이트 생성 중...")
        
        try:
            # 파일 생성
            output_dir = create_website_files(topic)
            successful_sites.append(output_dir)
            
            # API 호출 제한을 위한 대기
            if i % 5 == 0:
                print("⏳ API 호출 제한을 위한 2초 대기...")
                time.sleep(2)
                
        except Exception as e:
            failed_topics.append(topic)
            print(f"❌ {topic} 처리 실패: {e}")
    
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
    
    # 생성된 topics를 파일로 저장
    with open("generated_topics.json", "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print(f"\n💾 생성된 topics가 generated_topics.json에 저장되었습니다.")

if __name__ == "__main__":
    main()
