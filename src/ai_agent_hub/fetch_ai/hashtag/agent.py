import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents_core.models import ErrorMessage

from chat_trending import chat_trending
from preplexity_model import get_trending_fashion_hashtags

AGENT_SEED = os.getenv("AGENT_SEED", "image-generator-agent-seed-phrase")
AGENT_NAME = os.getenv("AGENT_NAME", "Image Generator Agent")

AGENT_SEED = "RUBARU Hashtag Generator"
AGENT_NAME = "Srija"

PORT = 8000
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=PORT,
    mailbox=True,
)


# Include protocol
agent.include(chat_trending, publish_manifest=True)

@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")

if __name__ == "__main__":
    agent.run()