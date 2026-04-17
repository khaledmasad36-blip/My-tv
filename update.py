import requests

def get_link():
    url = "http://ugeen.live"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open("playlist.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Done!")
    except:
        print("Error")

if __name__ == "__main__":
    get_link()
