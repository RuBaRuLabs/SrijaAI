import requests
from uagents import Context, Protocol

# API endpoint and your authentication details
API_URL = "https://api.perplexity.ai/chat/completions"  # Replace with the real endpoint
API_KEY = "<Model API Key>"  # Replace with your API key

def get_trending_fashion_hashtags(ctx: Context, prompt: str) -> str:
    #prompt = "Think yourself as a social media manager, and advice me on the trending social media hastags on tiktok, instagram platform, and catchy words which has a very high virality factor in the "+prompt+" industry."
    #prompt = "Think yourself as a social media marketer, and List the most viral and trending hashtags for food vlogging on Twitter, TikTok and Instagram, and catchy words which has a very high virality factor in the "+prompt+" industry. Include the approximate number of posts or videos associated with each hashtag. Focus on hashtags that drive high engagement"
    prompt = f"""
    You are an expert social media trend analyst with access to real-time data and deep platform expertise. 
    Your task is to identify and analyze the most current trending hashtags in the {prompt} industry/niche.

    INSTRUCTIONS:
    1. Use ONLY the 'searchTheWeb' tool to identify real-time trending topics.
    2. Focus strictly on posts trending RIGHT NOW (ignore historical data).
    3. For each major platform (Twitter/X, Instagram, TikTok):
       - Suggest platform-optimized hashtags only.
       - Score each hashtag set for viral potential out of 10 without any reasoning.
    4. Ignore sending result if you cannot find the results.

    OUTPUT FORMAT (MANDATORY):
    Return results ONLY in this exact format:

    Twitter/X:
    #hashtag1 (score/10)
    #hashtag2 (score/10)
    #hashtag3 (score/10)

    Instagram:
    #hashtag1 (score/10)
    #hashtag2 (score/10)
    #hashtag3 (score/10)

    TikTok:
    #hashtag1 (score/10)
    #hashtag2 (score/10)
    #hashtag3 (score/10)

    Do not deviate from this structure.
    """
    ctx.logger.info(f"Final prompt is: {prompt}")
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

