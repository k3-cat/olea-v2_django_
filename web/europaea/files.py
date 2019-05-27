import os
import shutil

from django.conf import settings


def get_file_dir(pid=None, work=None):
    if pid:
        return f'{settings.STOEAGE_DIR}/1/{pid}/'
    if work:
        return f'{settings.STOEAGE_DIR}/1/{work.project}/'


def get_file_name(work):
    return f'{work.dep}-{work.role}-{work.user}'


def get_file_path(work):
    dir_ = get_file_dir(work=work)
    name = get_file_name(work)
    return f'{dir_}/{name}'


def create_if_not_exist(pid):
    dir_ = get_file_dir(pid)
    if os.path.exists(dir_):
        return
    os.mkdir(dir_)


MIME_TYPE_ID = {
    'audio/flac': 'audio-flac',
    'image/png': 'picture-png',
    'video/x-matroska': 'video-mkv',
    'video/mp4': 'video-mp4'
} # yapf: disable

def mime_to_type_id(mime):
    return MIME_TYPE_ID[mime]


def safe_delete(work):
    dir_ = get_file_path(work=work)
    name = get_file_name(work)
    shutil.move(dir_, f'{settings.STOEAGE_DIR}/0/{name}')
