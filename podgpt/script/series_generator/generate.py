import asyncio
import json

from script.models import Script

from episode_generator.generator import generate_episode, functions
from episode_generator.overview import generate_episode_overview


def generate_series(title: str, guidelines: str):
    loop = asyncio.new_event_loop()

    overview = loop.run_until_complete(
        generate_episode_overview(title, guidelines, functions))

    overview = json.loads(overview)

    episodes = asyncio.gather(*[
        generate_episode(overview, title, guidelines)
    ])

    episodes = loop.run_until_complete(episodes)

    for idx, episode in enumerate(episodes):
        title = overview[idx]['title']
        content = episode

        Script.objects.create(title=title, contents=json.dumps(content))
