import json


from .wiki import wiki_search
from .gpt import completion_to_content
from .overview import generate_episode_overview
from .sections import generate_episode_section, generate_intro, generate_plug

functions = {
    'definations': [{
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
    }],
    'available_funcs': {
        'wiki_search': wiki_search
    }
}


async def generate_episode(overview: str, topic: str, guidelines: str, plug_info):
    episode_overview = await generate_episode_overview(overview, guidelines, functions)

    contents = []

    for section in episode_overview:
        contents.append(
            await generate_episode_section(
                section,
                episode_overview,
                topic,
                contents[-2:],
                guidelines,
                functions
            ))

    center = int(len(contents) / 2)
    temp = []

    for idx, content in enumerate(contents):
        if idx == center:
            if contents and plug_info:
                try:
                    temp.append(
                        await generate_plug(
                            plug_info,
                            [
                                completion_to_content(content)
                                for content in contents
                            ]
                        )
                    )
                except Exception as e:
                    print(e)
                    pass
            temp.append(content)

        else:
            temp.append(content)

    contents = temp

    contents = [completion_to_content(completion)
                for completion in contents if completion]

    contents = [completion_to_content(await generate_intro(episode_overview, guidelines)), *contents]

    return contents
