from io import BytesIO

from pydub import AudioSegment


def compose(data: list[bytes]) -> BytesIO:
    if not data:
        return

    result: AudioSegment = AudioSegment.from_mp3(BytesIO(data[0]))
    for idx in range(1, len(data)):
        _section = AudioSegment.from_mp3(BytesIO(data[idx]))
        result = result.append(_section + AudioSegment.silent(10_000))

    return result.export()
