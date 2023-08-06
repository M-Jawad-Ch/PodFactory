import boto3
import requests
import json

from botocore.exceptions import NoCredentialsError
from django.conf import settings

from pydub import AudioSegment
from io import BytesIO

from django.contrib.sites.models import Site
from audio.models import Audio
from interface.models import Music

function_url = 'https://il774ictmvehzycz4ghcdfoffa0dtonk.lambda-url.ap-south-1.on.aws/'


def download(bucket, fileName, file):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )

    s3.download_fileobj(bucket, fileName, file)


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY
    )

    try:
        s3.upload_fileobj(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        print('File not found')
        return False
    except NoCredentialsError:
        print('Credentials not available')
        return False


def intro_outro(audio: Audio, intro: Music, outro: Music, site: Site):
    res = requests.post(
        function_url,
        data=json.dumps({
            'type': 'intro_outro',
            'audio': 'http://' + site.domain + audio.audio_file.url,
            'intro': 'http://' + site.domain + intro._file.url if intro else None,
            'outro': 'http://' + site.domain + outro._file.url if outro else None
        })
    )

    if res.status_code == 200 and res.json().get('success'):
        bytesIo = BytesIO()
        download('blake-message-bucket', 'final.mp3', bytesIo)
        audio.audio_file.save(content=bytes)
        return audio


def compose(data: list[bytes], site: Site) -> bytes | None:
    Audios = [Audio.objects.create() for _ in range(len(data))]

    for idx, audio in enumerate(Audios):
        audio.audio_file.save(
            name=audio.name + '.mp3',
            content=data[idx]
        )

    urls = ['http://' + site.domain + audio.audio_file.url
            for audio in Audios]

    res = requests.get(
        function_url,
        data=json.dumps({
            'type': 'compose',
            'urls': urls
        })
    )

    if res.status_code == 200 and res.json().get('success'):
        [audio.delete() for audio in Audios]

        bytesIo = BytesIO()
        download('blake-message-bucket', 'final.mp3', bytesIo)
        return bytesIo


def add_music(audio: Audio, music: Music, site: Site) -> Audio:
    audio_url = 'http://' + site.domain + audio.audio_file.url
    music_url = 'http://' + site.domain + music._file.url

    res = requests.post(
        function_url,
        data=json.dumps({
            'type': 'add_music',
            'music': music_url,
            'audio': audio_url
        })
    )

    if res.status_code == 200 and res.json().get('success'):
        bytesIo = BytesIO()
        download('blake-message-bucket', 'final.mp3', bytesIo)
        audio.audio_file.save(content=bytesIo)

        return audio
