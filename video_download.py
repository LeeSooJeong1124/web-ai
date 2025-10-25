import requests

url = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
output_path = "SampleVideo_1280x720_1mb.mp4"

response = requests.get(url)
with open(output_path, "wb") as f:
    f.write(response.content)

print("✅ 다운로드 완료:", output_path)