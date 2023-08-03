from .gpt import completion_to_content, prompt_gpt


async def add_audio_tags(content: str):
    messages = [
        {
            'role': 'system',
            'content': """
You are a sound designer\engineer. Your job is to add audio sound effects to parts a script.
The sound effects should be specific and related to the context. The syntax of the audio tags you will add is as folows:
The sound effect will be enclosed in '<' and '>' like <The sound of metal objects falling>.
Donot change the script only add the audio tags."""
        },
        {
            'role': 'user',
            'content': f"Add sound effects to the following: {content}"
        }
    ]

    return completion_to_content(await prompt_gpt(messages))
