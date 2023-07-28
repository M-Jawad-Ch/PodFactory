from django.apps import AppConfig
from django.conf import settings

import environ
from os.path import join


class AudioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audio'

    def ready(self) -> None:
        env = environ.Env()
        environ.Env.read_env(join(settings.BASE_DIR, '.env'))

        from audio.generator.elevenlabs import AudioSynthesiser

        AudioSynthesiser.api_key = env.get_value('ELEVEN_LABS_API_KEY')
        AudioSynthesiser.voice_id = env.get_value('VOICE_ID')

        return super().ready()
