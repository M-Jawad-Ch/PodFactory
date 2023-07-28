from io import BytesIO

from pydub import AudioSegment


def compose(data: list[bytes]) -> BytesIO:
    if not data:
        return

    result = AudioSegment.silent(1_000)

    for section in data:
        result += AudioSegment.silent(1_000) + \
            AudioSegment.from_mp3(BytesIO(section))

    return result.export()
