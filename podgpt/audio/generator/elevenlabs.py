import requests
import json

from time import sleep

from django.utils.text import slugify

from interface.models import Music
from audio.models import Audio
from audio.generator.designer import compose, add_music, intro_outro

from pydub import AudioSegment
from io import BytesIO


class AudioSynthesiser:
    running = False
    api_key = None
    voice_id = None

    def __init__(self):
        if not AudioSynthesiser.api_key:
            raise Exception('API Key not set.')

        if not AudioSynthesiser.voice_id:
            raise Exception('Voice Id not set.')

    def request(self, content: str):
        status = 200
        for _ in range(5):
            with requests.post(
                f'https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}',
                headers={
                    'accept': 'audio/mpeg',
                    'xi-api-key': self.api_key,
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    'text': str(content)
                })
            ) as response:
                if response.status_code == 200:
                    return response
                status = response.status_code
                print(status)

        return status

    def generate(self, title: str, content: list[str]) -> Audio:
        """
        Pass this into a thread. This function has sleep() in it so it will
        cause the main thread to sleep.
        """

        while (AudioSynthesiser.running):
            sleep(0.2)

        AudioSynthesiser.running = True

        audio = AudioSegment.silent(1_000)

        for section in content:
            response = self.request(section)

            if type(response) == type(1):
                continue

            audio += AudioSegment.silent(2_000) + \
                AudioSegment.from_file(BytesIO(response.content))

        audio_model = Audio.objects.create(name=title)

        audio_model.audio_file.save(
            name=slugify(title) + '.mp3', content=audio.export())
        audio_model.save()

        AudioSynthesiser.running = False

        return audio_model
