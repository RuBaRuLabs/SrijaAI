import requests

API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "<Model API Key>"  # Replace with your actual API key

def test_api_key():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        print("API key is valid and works.")
        print("Response snippet:", response.json())
    elif response.status_code == 401:
        print("Unauthorized! API key is invalid or inactive.")
    elif response.status_code == 403:
        print("Forbidden! API key does not have permissions for this endpoint.")
    else:
        print(f"Unexpected status code: {response.status_code}")
        print(response.text)


def get_trending_fashion_hashtags(prompt: str) -> str:
    prompt = "Think yourself as a social media manager, and advice me on the tranding social media hastag in tiktok platform, and catchy words which has a very high virality factor in the"+prompt+"industry."
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar",  # Or your specific model identifier
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 128
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        hashtags = response.json()["choices"][0]["message"]["content"].split()
        print(hashtags)
    else:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")


if __name__ == "__main__":
    get_trending_fashion_hashtags("memes")
