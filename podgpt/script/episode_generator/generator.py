import json
import aiolimiter


from .wiki import wiki_search
from .gpt import completion_to_content
from .overview import generate_episode_overview
from .sections import generate_episode_section, generate_intro

functions = {
    'definations': {
        "name": "wiki_search",
        "description": "Get the summarised articles from the Wikipedia.",
        "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to get the relevant information, e.g. Astrology",
                    }
                },
            "required": ["topic"],
        },
    },
    'available_funcs': {
        'wiki_search': wiki_search
    }
}


async def generate_episode(overview: str, topic: str, guidelines: str, limiter: aiolimiter.AsyncLimiter):
    await limiter.acquire()

    episode_overview = completion_to_content(await generate_episode_overview(overview, guidelines, functions))
    episode_overview = json.loads(episode_overview)

    contents = []

    for section in episode_overview:
        contents.append(await generate_episode_section(section, episode_overview, topic, contents, guidelines, functions))

    contents = [completion_to_content(completion)
                for completion in contents if completion]

    contents = [completion_to_content(await generate_intro(episode_overview, guidelines)), *contents]

    return contents
