import requests
import json

from time import sleep

from audio.models import Audio


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
            with requests.patch(
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

    def generate(self, content: list[str]):
        """
        Pass this into a thread. This function has sleep() in it so it will
        cause the main thread to sleep.
        """

        while (AudioSynthesiser.running):
            sleep(0.2)

        AudioSynthesiser.running = True

        responses: list[requests.Response | int] = []

        for section in content:
            responses.append(self.request(section))

        responses = [response.content for response in responses if type(
            response) != type(1)]

        AudioSynthesiser.running = False
