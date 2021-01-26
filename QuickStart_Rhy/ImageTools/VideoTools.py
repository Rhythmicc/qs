# coding=utf-8
"""
视频处理库, 你需要额外安装moviepy库

Video processing library, you need to install additional moviepy library
"""
import os
from .. import dir_char, user_lang, qs_default_console, qs_error_string


def VideoWrapper(func):
    """
    视频处理的函数装饰器

    Video processing function decorator

    :param func: 函数
    :return: wrapper
    """
    def wrapper(path, *args, **kwargs):
        try:
            import moviepy
        except ImportError:
            qs_default_console.log(
                qs_error_string, 'You need install "moviepy" first' if user_lang != 'zh' else '你需要先安装"moviepy"')
        else:
            if not os.path.exists(path):
                qs_default_console.log(qs_error_string, f'{"No such file" if user_lang != "zh" else "文件不存在"}: {path}')
                return
            if not os.path.isfile(path):
                qs_default_console.log(qs_error_string, f'{"No a file" if user_lang != "zh" else "不是文件"}: {path}')
            func(path, *args, **kwargs)

    return wrapper


@VideoWrapper
def video_2_gif(path: str, size: tuple = (480, 320), fps: int = None):
    """
    视频转gif（gif生成在视频路径的同目录下）

    Video transfer GIF (GIF generated in the same directory as the video path)

    :param path: 视频路径
    :param size: gif尺寸
    :param fps: fps
    :return: None
    """
    import moviepy.editor as mpy
    file_name = '.'.join(os.path.basename(path).split('.')[:-1]) + '.gif'
    dir_name = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
    ct = mpy.VideoFileClip(path) if not size else mpy.VideoFileClip(path).resize(size)
    ct.write_gif(dir_name + file_name, fps=fps) if fps else ct.write_gif(dir_name + file_name)


@VideoWrapper
def rm_audio(path: str):
    """
    删除视频的音频

    Delete the audio of the video

    :param path: 视频路径
    :return: None
    """
    import moviepy.editor as mpy
    file_name = os.path.basename(path)
    if '.' in file_name:
        indx = file_name.index('.')
        file_name = file_name[:indx] + '_rm_audio' + file_name[indx:]
        file_name = file_name.split('.')
        file_name = '.'.join(file_name[:-1]) + '.mp4'
    else:
        file_name += '_rm_audio'
    dir_name = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
    ct = mpy.VideoFileClip(path).set_audio(None)
    ct.write_videofile(dir_name + file_name)


@VideoWrapper
def tomp4(path: str):
    """
    将视频转为mp4

    Convert the video to MP4

    :param path: 视频路径
    :return: None
    """
    import moviepy.editor as mpy
    file_name = os.path.basename(path)
    file_name = '.'.join(file_name.split('.')[:-1]) + '.mp4' if '.' in file_name else file_name + '.mp4'
    dir_name = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
    ct = mpy.VideoFileClip(path)
    ct.write_videofile(dir_name + file_name, audio_codec='aac')


@VideoWrapper
def video_2_mp3(path: str):
    """
    提取视频的音频并保存为mp3格式

    Extract the audio from the video and save it in MP3 format

    :return:
    """
    import moviepy.editor as mpy
    file_name = os.path.basename(path)
    file_name = '.'.join(file_name[:-1].split('.')) + '.mp3' if '.' in file_name else file_name + '.mp3'
    dir_name = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
    mpy.VideoFileClip(path).audio.write_audiofile(dir_name + file_name)
