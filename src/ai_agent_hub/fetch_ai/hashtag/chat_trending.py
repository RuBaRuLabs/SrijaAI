import base64
import os
import requests
from uuid import uuid4
from datetime import datetime
from pydantic.v1 import UUID4

from uagents import Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    Resource,
    ResourceContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from uagents_core.storage import ExternalStorage
from preplexity_model import get_trending_fashion_hashtags

#AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY")
#STORAGE_URL = os.getenv("AGENTVERSE_URL", "https://agentverse.ai") + "/v1/storage"



#if AGENTVERSE_API_KEY is None:
#    raise ValueError("You need to provide an API_TOKEN.")

#external_storage = ExternalStorage(api_token=AGENTVERSE_API_KEY, storage_url=STORAGE_URL)


def create_text_chat(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text=text)],
    )

def create_end_session_chat() -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[EndSessionContent(type="end-session")],
    )

def create_resource_chat(asset_id: str, uri: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            ResourceContent(
                type="resource",
                resource_id=UUID4(asset_id),
                resource=Resource(
                    uri=uri,
                    metadata={
                        "mime_type": "image/png",
                        "role": "generated-image"
                    }
                )
            )
        ]
    )


chat_trending = Protocol(spec=chat_protocol_spec)


@chat_trending.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")

            prompt = msg.content[0].text
            try:
                await ctx.send(sender, create_text_chat("Awesome! You’re searching for the latest trending hashtags in the "+prompt+" niche. Please wait while we generate your results..."))
                
                hashtags = get_trending_fashion_hashtags(prompt)
                #output = generate_html(hashtags);
                output = ' '.join(hashtags)
                    
                ctx.logger.info(f"Asset permissions set to: {sender}")
                ctx.logger.info(f"hashtags: {output}")
                await ctx.send(sender, create_text_chat("Here are the top trending hashtags in the "+prompt+" niche —ideal for Instagram, TikTok, and other social media platforms:"))
                await ctx.send(sender, create_text_chat(output))

            except Exception as err:
                ctx.logger.error(err)
                await ctx.send(
                    sender,
                    create_text_chat(
                        "Sorry, I couldn't process your request. Please try again later."
                    ),
                )
                return

            await ctx.send(sender, create_end_session_chat())

        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


def generate_html(hashtags):
    items = "\n".join([f"<li>{tag}</li>" for tag in hashtags])
    html_content = f"""
    <html>
    <head><title>Trending TikTok Fashion Hashtags</title></head>
    <body>
        <h1>Trending Fashion Hashtags on TikTok</h1>
        <ul>
            {items}
        </ul>
    </body>
    </html>
    """
    return html_content


@chat_trending.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}")