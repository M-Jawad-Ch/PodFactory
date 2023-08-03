from io import BytesIO

import numpy as np
from math import ceil
from pydub import AudioSegment
from pydub.effects import speedup

from interface.models import Music, Audio


def compose(data: list[bytes]):
    if not data:
        return

    result = AudioSegment.silent(1_000)

    for section in data:
        result += AudioSegment.silent(5_000) + \
            AudioSegment.from_mp3(BytesIO(section))

    return result


def intro_outro(audio: AudioSegment, intro: Music, outro: Music):
    if intro:
        intro: AudioSegment = AudioSegment.from_file(intro._file.file)

    if outro:
        outro: AudioSegment = AudioSegment.from_file(outro._file.file)

    if intro:
        audio = intro + AudioSegment.silent(1_500) + audio

    if outro:
        audio = audio + AudioSegment.silent(1_500) + outro

    return audio


def add_music(audio: AudioSegment, _music: Music):
    music: AudioSegment = AudioSegment.from_file(_music._file.file)
    music -= 25

    audio = audio.overlay(music, loop=True)

    return audio

    """music = music.set_channels(1)
    audio = audio.set_channels(1)

    rate = audio.frame_count() / audio.duration_seconds
    music_rate = music.frame_count() / music.duration_seconds

    if rate < music_rate:
        audio = speedup(audio, music_rate / rate)
        audio.set_frame_rate(int(music_rate))
    else:
        music = speedup(music, rate/music_rate)
        music.set_frame_rate(int(rate))

    audio = np.array(audio.get_array_of_samples())
    music = np.array(music.get_array_of_samples())

    music = music * audio.mean() / music.mean()

    music = music[:len(audio)]
    times = len(audio) / len(music)
    music = np.resize(music, ceil(len(music)*times))
    music = music[:len(audio)]

    audio: np.ndarray = audio / audio.max()
    music: np.ndarray = music / music.max()

    music = music / (abs(audio) + 1) ** 3
    music /= 6

    final_samples = music + audio

    final_samples = np.int32(final_samples * 10**9)

    final_samples = AudioSegment(
        final_samples.tobytes(),
        frame_rate=int(max(rate, music_rate)),
        sample_width=final_samples.dtype.itemsize,
        channels=1
    )

    return final_samples"""
