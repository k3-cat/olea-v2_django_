import os
from pydub import AudioSegment


def create_if_not_exist(file_dir):
    dir_ = os.path.dirname(file_dir)
    if os.path.exists(dir_):
        return
    os.mkdir(dir_)

def get_audio_info(file_dir, mime):
    sound = AudioSegment.from_file(file_dir, format=mime.replace('audio/', ''))
    if sound.channels < 2:
        raise Exception
    metadata = {
        'frame_rate': sound.frame_rate,
        'frame_width': sound.frame_width,
        'duration': sound.duration_seconds / 1000
    }
    return metadata


MIME_TYPE_ID = {
    'audio/wav': 'audio-wav',
    'audio/flac': 'audio-flac',
    'audio/mp3': 'audio-mp3',
    'image/png': 'picture-png',
    'video/x-matroska': 'video-mkv',
    'video/mp4': 'video-mp4'
} # yapf: disable

def mime_to_type_id(mime):
    return MIME_TYPE_ID[mime]
