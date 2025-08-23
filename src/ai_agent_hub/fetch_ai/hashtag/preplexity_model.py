import requests

# API endpoint and your authentication details
API_URL = "https://api.perplexity.ai/chat/completions"  # Replace with the real endpoint
API_KEY = "<Model API Key>"  # Replace with your API key

def get_trending_fashion_hashtags(prompt: str) -> str:
    prompt = "Think yourself as a social media manager, and advice me on the trending social media hastags on tiktok, instagram platform, and catchy words which has a very high virality factor in the "+prompt+" industry."
    #prompt = "Think yourself as a social media marketer, and List the most viral and trending hashtags for food vlogging on Twitter, TikTok and Instagram, and catchy words which has a very high virality factor in the "+prompt+" industry. Include the approximate number of posts or videos associated with each hashtag. Focus on hashtags that drive high engagement"
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
        return hashtags
    else:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")

