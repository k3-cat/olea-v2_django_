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


MIME_FTYPE = {
    'audio/wav': 51,
    'audio/flac': 51,
    'image/png': 61,
    'video/x-matroska': 71,
    'video/mp4': 72
} # yapf: disable

def mime_to_ftype(mime):
    return MIME_FTYPE[mime] if mime in MIME_FTYPE else 0


def safe_delete(work):
    dir_ = get_file_path(work=work)
    name = get_file_name(work)
    shutil.move(dir_, f'{settings.STOEAGE_DIR}/0/{name}')
