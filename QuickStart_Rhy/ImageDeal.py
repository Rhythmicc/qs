# coding=utf-8
"""
调用各种图像处理工具

Call various image processing tools
"""
import sys
import os


def set_img_background():
    """替换图片颜色 | Replace color in image"""
    from .ImageTools.ColorTools import transport_back, get_color_from_str

    try:
        img = sys.argv[2]
        if img == '-help':
            raise IndexError
        if not os.path.exists(img):
            exit('[ERROR] No Such File: %s' % img)
        to = sys.argv[3]
        try:
            frm = sys.argv[4]
        except IndexError:
            frm = '0,0,0,0'
    except IndexError:
        print('Usage: qs -stbg picture to_color [from_color: default transparency]')
        exit(0)
    else:
        to = get_color_from_str(to)
        frm = get_color_from_str(frm)
        img = transport_back(img, to, frm)
        iname = sys.argv[2].split('.')
        iname = iname[0] + '_stbg.' + ''.join(iname[1:])
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
        print('Usage: qs -v2gif *.mp4 width,height fps')
        exit(0)
    else:
        video_2_gif(video, sz, fps) if sz and fps else video_2_gif(video, sz) \
            if sz else video_2_gif(video, fps=fps) if fps else video_2_gif(video)


def remove_audio():
    """删除视频的音频 | remove audio in mp4"""
    from .ImageTools.VideoTools import rm_audio
    try:
        video = sys.argv[2]
    except IndexError:
        exit('Usage: qs -rmaudio *.mp4')
    else:
        rm_audio(video)


def v2mp4():
    """视频转mp4 | transfer video to mp4"""
    from .ImageTools.VideoTools import tomp4
    try:
        video = sys.argv[2]
    except IndexError:
        exit('Usage: qs -v2mp4 <video>')
    else:
        tomp4(video)


def v2mp3():
    """提取视频音频为mp3 | Extract the audio from the video and save it in MP3 format"""
    from .ImageTools.VideoTools import video_2_mp3
    try:
        video = sys.argv[2]
    except IndexError:
        exit('Usage: qs -v2mp3 <video>')
    else:
        video_2_mp3(video)


def icat():
    """Mac::iTerm下预览图片 | Preview the picture under Mac::iTerm"""
    try:
        path = sys.argv[2]
        is_url = '-u' in sys.argv
        if not os.path.exists(path) and not is_url:
            print('No such file:', path)
            raise FileNotFoundError
    except:
        exit('Usage: qs -icat <img path/url> [-u if is url]')
    else:
        from .ImageTools.ImagePreview import image_preview
        image_preview(open(path)) if not is_url else image_preview(path, is_url)
