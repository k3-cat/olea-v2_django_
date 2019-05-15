# yapf: disable

WORKSTATE = (
    (-2, 'cancelled_f'),
    (-1, 'cancelled'),
    (0, 'normal'),
    (1, 'finished')
)

DEPARTMENT = (
    (40, 'writing'),
    (50, 'reading'),
    (51, 'reading_eng'),
    (60, 'painting'),
    (70, 'post-production')
)

STORAGE_TYPE = (
    (0, 'none'),
    (10, 'folder'),
    (50, 'audio-wav'),
    (51, 'audio-flac'),
    (52, 'audio-mp3'),
    (60, 'picture-png'),
    (70, 'video-mkv'),
    (71, 'video-mp4'),
)

PROGRESS_STATE = (
    (-10, 'error'),         # 特殊
    (-1, 'waiting'),
    (0, 'init'),            # 项目初始化
    (1, 'recruiting'),      # 项目缺人
    (2, 'processing'),      # 不缺人但未完成
    (3, 'done'),            # 项目完成
)
