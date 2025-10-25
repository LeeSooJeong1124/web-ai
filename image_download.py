import requests

url = "https://fastly.picsum.photos/id/256/400/300.jpg?hmac=eDLZM9o1U1oO0vtsVt6V4bWlrKbK0J4uBmENDh6ExIk"
filename = "image.jpg"

response = requests.get(url)

# 성공적으로 요청되었는지 확인
if response.status_code == 200:
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✅ Saved as {filename}")
else:
    print("❌ Failed to download:", response.status_code)

# wget -O image.jpg "https://fastly.picsum.photos/id/256/400/300.jpg?hmac=eDLZM9o1U1oO0vtsVt6V4bWlrKbK0J4uBmENDh6ExIk"
# curl -L "https://fastly.picsum.photos/id/256/400/300.jpg?hmac=eDLZM9o1U1oO0vtsVt6V4bWlrKbK0J4uBmENDh6ExIk" -o image.jpg

# 여러 이미지를 한꺼번에 받고 싶다면, URL들을 urls.txt에 저장해두고,
# wget -i urls.txt
# 또는
# while read url; do curl -O "$url"; done < urls.txt