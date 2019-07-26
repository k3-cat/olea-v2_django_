from pydub import AudioSegment


def get_audio_info(file_dir):
    sound = AudioSegment.from_file(file_dir, format='flac')
    metadata = {
        'frame_rate': sound.frame_rate,
        'frame_width': sound.frame_width,
        'duration': sound.duration_seconds / 1000
    }
    return metadata
