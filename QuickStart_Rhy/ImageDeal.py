# coding=utf-8
"""
调用各种图像处理工具

Call various image processing tools
"""
import sys
import os
from . import qs_default_console, qs_error_string


def set_img_background():
    """替换图片颜色 | Replace color in image"""
    from .ImageTools.ColorTools import transport_back, get_color_from_str

    try:
        img = sys.argv[2]
        if img == '-help':
            raise IndexError
        if not os.path.exists(img):
            qs_default_console.log(qs_error_string, 'No Such File: %s' % img)
            return
        to = sys.argv[3]
        try:
            frm = sys.argv[4]
        except IndexError:
            frm = '0,0,0,0'
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs stbg <picture> <to_color> [from_color: default transparency]')
        return
    else:
        to = get_color_from_str(to)
        frm = get_color_from_str(frm)
        img = transport_back(img, to, frm)
        iname = sys.argv[2].split('.')
        iname = iname[0] + '_stbg.' + ''.join(iname[1:])
        img.save(iname)


def fmt_img_color():
    from .ImageTools.ColorTools import formatOneColor, get_color_from_str

    try:
        img = sys.argv[2]
        if img == '-help':
            raise IndexError
        if not os.path.exists(img):
            qs_default_console.log(qs_error_string, 'No Such File: %s' % img)
            return
        to = sys.argv[3]
        try:
            exp = sys.argv[4:]
        except IndexError:
            exp = '0,0,0,0'
    except IndexError:
        qs_default_console.log(qs_error_string,
                               'Usage: qs fmti <picture> <to_color> [except_color: default transparency]')
        return
    else:
        to = get_color_from_str(to)
        exp = [get_color_from_str(i) for i in exp]
        img = formatOneColor(img, to, exp)
        iname = sys.argv[2].split('.')
        iname = iname[0] + '_fmt.' + ''.join(iname[1:])
        img.save(iname)


def v2gif():
    """视频转gif | video to gif"""
    from .ImageTools.VideoTools import video_2_gif

    try:
        video = sys.argv[2]
        sz, fps = None, None
        if len(sys.argv) > 3:
            for i in sys.argv[3:]:
                try:
                    if ',' in i:
                        sz = tuple([int(j) for j in i.split(',')])
                    else:
                        fps = int(i)
                except:
                    raise IndexError
        sz = tuple([int(i) for i in sys.argv[3].split(',')]) if len(sys.argv) > 3 and ',' in sys.argv[3] else None
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs v2gif <*.mp4> [width,height] [fps]')
        return
    else:
        video_2_gif(video, sz, fps) if sz and fps else video_2_gif(video, sz) \
            if sz else video_2_gif(video, fps=fps) if fps else video_2_gif(video)


def remove_audio():
    """删除视频的音频 | remove audio in mp4"""
    from .ImageTools.VideoTools import rm_audio
    try:
        videos = sys.argv[2:]
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs rmaudio <video...>')
    else:
        for video in videos:
            rm_audio(video)


def v2mp4():
    """视频转mp4 | transfer video to mp4"""
    from .ImageTools.VideoTools import tomp4
    try:
        videos = sys.argv[2:]
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs v2mp4 <video...>')
    else:
        for video in videos:
            tomp4(video)


def v2mp3():
    """提取视频音频为mp3 | Extract the audio from the video and save it in MP3 format"""
    from .ImageTools.VideoTools import video_2_mp3
    try:
        videos = sys.argv[2:]
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs v2mp3 <video...>')
    else:
        for video in videos:
            video_2_mp3(video)


def icat():
    """Mac::iTerm下预览图片 | Preview the picture under Mac::iTerm"""
    try:
        path = sys.argv[2]
        is_url = '-u' in sys.argv or \
                 (not os.path.exists(path) and (path.startswith('http://') or path.startswith('https://')))
        if not os.path.exists(path) and not is_url:
            qs_default_console.log(qs_error_string, 'No such file:', path)
            raise FileNotFoundError
    except:
        qs_default_console.log(qs_error_string, 'Usage: qs icat <img path/url> [-u if is url]')
    else:
        from .ImageTools.ImagePreview import image_preview
        image_preview(open(path)) if not is_url else image_preview(path, is_url)


def i2png():
    try:
        imgs = sys.argv[2:]
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs i2png <imgs...>')
    else:
        from .ImageTools.ImageTools import topng
        for imgPath in imgs:
            topng(imgPath)


def i2jpg():
    try:
        imgs = sys.argv[2:]
    except IndexError:
        qs_default_console.log(qs_error_string, 'Usage: qs i2jpg <imgs...>')
    else:
        from .ImageTools.ImageTools import tojpg
        for imgPath in imgs:
            tojpg(imgPath)
