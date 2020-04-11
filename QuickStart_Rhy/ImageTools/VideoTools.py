import os
from QuickStart_Rhy import dir_char


def VideoWrapper(func):
    def wrapper(path, *args, **kwargs):
        try:
            import moviepy
        except ImportError as e:
            e = repr(e)
            exit(e)
        else:
            if not os.path.exists(path):
                exit('No such file: %s' % path)
            if not os.path.isfile(path):
                exit('%s not a file!' % path)
            func(path, *args, **kwargs)

    return wrapper


@VideoWrapper
def video_2_gif(path, size=(480, 320), fps=None):
    import moviepy.editor as mpy
    file_name = '.'.join(os.path.basename(path).split('.')[:-1]) + '.gif'
    dir_name = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
    ct = mpy.VideoFileClip(path) if not size else mpy.VideoFileClip(path).resize(size)
    ct.write_gif(dir_name + file_name, fps=fps) if fps else ct.write_gif(dir_char + file_name)


@VideoWrapper
def rm_audio(path):
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
def tomp4(path):
    import moviepy.editor as mpy
    file_name = os.path.basename(path)
    file_name = '.'.join(file_name[:-1]) + '.mp4' if '.' in file_name else file_name + '.mp4'
    dir_name = dir_char.join(os.path.abspath(path).split(dir_char)[:-1]) + dir_char
    ct = mpy.VideoFileClip(path)
    ct.write_videofile(dir_name + file_name)
