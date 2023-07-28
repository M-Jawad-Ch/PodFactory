import openai
import aiolimiter
import tiktoken
import json

limiter = aiolimiter.AsyncLimiter(60, 1)
enc = None
model = 'gpt-3.5-turbo-16k-0613'  # 'gpt-4-0613'


def completion_to_content(x): return x['choices'][0]['message']['content']


async def prompt_gpt(messages, functions=None):
    for _ in range(5):
        try:
            await limiter.acquire()
            if functions:
                completion = await openai.ChatCompletion.acreate(
                    messages=messages,
                    model=model,
                    functions=functions
                )

                try:
                    with open('alpha.json', 'r') as f:
                        data = json.load(f)

                    if not data:
                        data = []

                    if completion_to_content(completion):
                        data.append(
                            [
                                *[
                                    message['content'] for message in messages[-2:]
                                ],
                                completion_to_content(completion)
                            ]
                        )

                    with open('alpha.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
                except:
                    print('Failed')

                return completion
            else:
                completion = await openai.ChatCompletion.acreate(
                    messages=messages,
                    model=model,
                )

                try:
                    with open('alpha.json', 'r') as f:
                        data = json.load(f)

                    if not data:
                        data = []

                    if completion_to_content(completion):
                        data.append(
                            [
                                *[
                                    message['content'] for message in messages[-2:]
                                ],
                                completion_to_content(completion)
                            ]
                        )

                    with open('alpha.json', 'w') as f:
                        f.write(json.dumps(data, indent=4))
                except:
                    print('Failed')

                return completion
        except Exception as e:
            print(e)


async def summarize(prompt: str):
    messages = [
        {
            'role': 'system',
            'content': """
You are an exceptional writer/journalist. You summarize content by describing in a compact and consice manner
without losing any important and valid information. You summarize the content and quote the orignal source whenever you 
deem it necessary.
"""
        },
        {
            'role': 'user',
            'content': f"""
You are given an article within the <article> and </article> tags.

<article>
{prompt}
</article>

Summarize the given article."""
        }
    ]

    return await prompt_gpt(messages)


def get_token_count(s: str):
    enc = tiktoken.get_encoding("cl100k_base") if not enc else enc
    return len(enc.encode(s))
