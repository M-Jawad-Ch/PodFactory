import asyncio
import json

from script.models import Script

from script.episode_generator.gpt import completion_to_content
from script.episode_generator.generator import generate_episode, functions
from script.episode_generator.overview import generate_overview


def generate_series(title: str, guidelines: str, plug_info):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    overview = loop.run_until_complete(
        generate_overview(title, functions))

    overview = json.loads(overview)

    episodes = asyncio.gather(*[
        generate_episode(overview_episode, title, guidelines, plug_info) for overview_episode in overview
    ])

    episodes = loop.run_until_complete(episodes)
    loop.close()

    scripts = []

    for idx, episode in enumerate(episodes):
        title = overview[idx]['title']
        content = episode

        scripts.append(Script.objects.create(
            title=title, contents=json.dumps(content)))

    return scripts
