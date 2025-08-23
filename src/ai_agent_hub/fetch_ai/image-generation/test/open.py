from openai import OpenAI
client = OpenAI(api_key="")

available = [m.id for m in client.models.list().data if "image" in m.id]
print("Image models available:", available)