import json

from .gpt import prompt_gpt, completion_to_content


async def generate_overview(prompt: str, functions):
    messages = [
        {
            'role': 'system',
            'content':
            """
You are a writer/producer/director. Your job is to write an overview of entire podcasts series.
The overview should be in JSON format. The JSON should be a list, each item in the list should have a title, which would be
the title of the episode and the content, which should be list of the main points to be discussed in the episode. The usual number
of episodes in a series is 10 to 15 so make sure to keep that in mind.
            
An example overview is as follows:
[
    {"title":"title of episode 1","content": ["Point mentioned 1","Point mentioned 2","Point mentioned 3","Point mentioned 4","Point mentioned 5","Point mentioned 6","Point mentioned 7"]},
    {"title":"title of episode 2","content": ["Point mentioned 1","Point mentioned 2","Point mentioned 3","Point mentioned 4","Point mentioned 5","Point mentioned 6","Point mentioned 7"]},
    {"title":"title of episode 3","content": ["Point mentioned 1","Point mentioned 2","Point mentioned 3","Point mentioned 4","Point mentioned 5","Point mentioned 6","Point mentioned 7"]},
    {"title":"title of episode 4","content": ["Point mentioned 1","Point mentioned 2","Point mentioned 3","Point mentioned 4","Point mentioned 5","Point mentioned 6","Point mentioned 7"]},
    {"title":"title of episode 5","content": ["Point mentioned 1","Point mentioned 2","Point mentioned 3","Point mentioned 4","Point mentioned 5","Point mentioned 6","Point mentioned 7"]},
]

The number of points in an episode must also be 15 - 20."""
        },
        {
            'role': 'user',
            'content': f'Write me an overview of a podcast based on {prompt}'
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

    else:
        return completion


async def generate_episode_overview(prompt: str, guidelines: str, functions):
    guidelines = f'These are additional guidelines:\n{guidelines}' if guidelines else ''

    messages = [
        {
            'role': 'system',
            'content':
            f"""You are a writer/producer/director. Your job is to write an overview of an entire episode of a podcast series.
The overview should be in JSON format. The JSON should be a list of the topics to consider including in an episode.
Write a minimum of ten topics and add more if less are provided to you. An example of your response is given below, strictly follow it:

[ "topic 1", "topic 2", "topic 3", "topic 4", "topic 5", "topic 6", "topic 7", "topic 8", "topic 9", "topic 10" ]

Your generated response must be in the above given syntax, meaning that you must only return a list of topics.

{guidelines}
"""
        },
        {
            'role': 'user',
            'content': f'Write me an overview of an episode that has the following information:\n\n{prompt}'
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

        return await prompt_gpt(messages)

    for _ in range(5):
        try:
            json.loads(completion_to_content(completion))
            return completion
        except:
            print('retrying json')
            messages += [
                {
                    'role': 'assistant',
                    'content': completion_to_content(completion)},
                {
                    'role': 'user',
                    'content': "Your response is not a valid JSON. Make appropriate corrections and remove repititions if any."
                }
            ]

            completion = await prompt_gpt(messages)
