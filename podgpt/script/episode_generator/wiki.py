import aiohttp
import aiolimiter
import asyncio

limiter = aiolimiter.AsyncLimiter(60, 1)


async def wiki_get(session: aiohttp.ClientSession, title: str):
    if limiter:
        await limiter.acquire()
    async with session.get(f'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={title}') as response:
        if response.status != 200:
            return ''

        pages = (await response.json())['query']['pages']

        text = pages[[key for key in pages][0]]['extract']

    return text


async def wiki_search(topic: str):
    try:
        async with aiohttp.ClientSession() as session:
            if limiter:
                await limiter.acquire()
            async with session.get(f'https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch={topic}&format=json') as response:
                titles = (await response.json())['query']['search']

            text = await asyncio.gather(*[wiki_get(session, item['title']) for item in titles])

        return text

    except Exception as e:
        print('Error', e)
        return 'No information found'
