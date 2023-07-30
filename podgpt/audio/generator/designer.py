from io import BytesIO

from pydub import AudioSegment

from interface.models import Music


def compose(data: list[bytes], intro: Music, outro: Music) -> BytesIO:
    if not data:
        return

    result = AudioSegment.silent(3_000)

    result = result + \
        AudioSegment.from_file(intro._file.file) if intro else result

    for section in data:
        result += AudioSegment.silent(5_000) + \
            AudioSegment.from_mp3(BytesIO(section))

    result = result + AudioSegment.silent(1_000) + \
        AudioSegment.from_file(outro._file.file) if outro else result

    return result.export()
