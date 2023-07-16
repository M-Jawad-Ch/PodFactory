import openai
import aiolimiter
import tiktoken

limiter = aiolimiter.AsyncLimiter(60, 1)
enc = tiktoken.get_encoding("cl100k_base")


def completion_to_content(x): return x['choices'][0]['message']['content']


async def prompt_gpt(messages, functions=None):
    for _ in range(5):
        try:
            await limiter.acquire()
            if functions:
                completion = await openai.ChatCompletion.acreate(
                    messages=messages,
                    model='gpt-3.5-turbo-16k',
                    functions=functions
                )

                return completion
            else:
                completion = await openai.ChatCompletion.acreate(
                    messages=messages,
                    model='gpt-3.5-turbo-16k',
                )

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
    return len(enc.encode(s))
