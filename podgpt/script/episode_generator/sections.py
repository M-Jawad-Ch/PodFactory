import json

from .gpt import prompt_gpt


async def generate_plug(plug_info: str, past):
    messages = [{
        'role': 'system',
        'content': f"""
This is one of the services you provide:
{plug_info}
"""
    },
        {
        'role': 'user',
        'content': f"""
This is a podcast episode, all the elements here are sections of the episode.
{past}

You are the host of a podcast episode. Advertise the above service to your listeners.
The plug should only be a couple of sentences long.
"""
    }]

    return await prompt_gpt(messages)


async def generate_episode_section(prompt: str, episode_overview: dict, topic: str, past, guidelines: str, functions):
    guidelines = f'These are additional guidelines:\n{guidelines}' if guidelines else ''

    messages = [
        {
            'role': 'system',
            'content':
            f"""
You are a writer/producer/director of a podcast series. You are working on a podcast with the title of {topic}.
The overview of the entire episode is: {episode_overview}.
Use the function called the 'wiki_search' to get relevant information.
The parameter topic for the function is the search string you would use to get relevant articles.

This is what you have generated uptill now:
{past}

Adhere to the following guidelines:
- Cut most adverbs, use precise adjectives and verbs instead
- Use active voice
- Use simple sentences

Try to make the podcast sound like you are telling a story. Make it seem like an amazaing experience,
and walk the listner through the environment. Make them imagine the sounds and the places. You are the narrator
of the story.

Remember, the data received from the wikipeida articles is not ours.

{guidelines}"""
        },
        {
            'role': 'user',
            'content': f"""Write a section on the following topic: {prompt}"""
        }
    ]

    completion = await prompt_gpt(messages, functions.get('definations'))

    if not completion:
        return None

    func_call = completion['choices'][0]['message'].get('function_call')

    if func_call:
        func = functions.get('available_funcs')[func_call['name']]
        args = json.loads(func_call['arguments'])

        res = await func(args.get('topic'))

        messages.append({
            'role': 'function',
            'name': func_call['name'],
            'content': f'{res}'
        })

        completion = await prompt_gpt(messages)

    return completion


async def generate_intro(episode, guidelines: str):
    guidelines = f'These are additional guidelines:\n{guidelines}' if guidelines else ''

    messages = [
        {
            'role': 'system',
            'content': """You are a skilled writer. You write the intorductory section of podcasts."""
        },
        {
            'role': 'user',
            'content': f"""
'My name is Clayton Hester. To view the rest of the Conceit Media podcasts, go to www.conceit.audio. That's conceit.audio.'
That should be at the start of the podcasts. After this, instruct the user to share the current podcast with their friends and family.
After that, write a couple of sentences about the episode. Here is the overview of the episode:

{episode}

{guidelines}"""
        }
    ]

    return await prompt_gpt(messages)
