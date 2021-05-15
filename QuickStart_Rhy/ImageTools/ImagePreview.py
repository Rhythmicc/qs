"""
在终端预览图片 | 目前仅有MacOS下的iTerm可用, 你需要自行安装imgcat库

preview image on terminal | At present, only iTerm under MacOS is available,
you need to install imgcat library by yourself
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .. import qs_default_console
from .. import headers
import math
import base64
import sys
import os
import struct
import io
import subprocess


TMUX_WRAP_ST = b'\033Ptmux;'
TMUX_WRAP_ED = b'\033\\'

OSC = b'\033]'
CSI = b'\033['
ST  = b'\a'      # \a = ^G (bell)


def get_image_shape(buf):
    '''
    Extracts image shape as 2-tuple (width, height) from the content buffer.

    Supports GIF, PNG and other image types (e.g. JPEG) if PIL/Pillow is installed.
    Returns (None, None) if it can't be identified.
    '''
    def _unpack(fmt, buffer, mode='Image'):
        try:
            return struct.unpack(fmt, buffer)
        except struct.error:
            raise ValueError("Invalid {} file".format(mode))

    # TODO: handle 'stream-like' data efficiently, not storing all the content into memory
    L = len(buf)

    if L >= 10 and buf[:6] in (b'GIF87a', b'GIF89a'):
        return _unpack("<hh", buf[6:10], mode='GIF')
    elif L >= 24 and buf.startswith(b'\211PNG\r\n\032\n') and buf[12:16] == b'IHDR':
        return _unpack(">LL", buf[16:24], mode='PNG')
    elif L >= 16 and buf.startswith(b'\211PNG\r\n\032\n'):
        return _unpack(">LL", buf[8:16], mode='PNG')
    else:
        # everything else: get width/height from PIL
        # TODO: it might be inefficient to write again the memory-loaded content to buffer...
        b = io.BytesIO()
        b.write(buf)

        try:
            from PIL import Image
            im = Image.open(b)
            return im.width, im.height
        except (IOError, OSError) as ex:
            # PIL.Image.open throws an error -- probably invalid byte input are given
            sys.stderr.write("Warning: PIL cannot identify image; this may not be an image file" + "\n")
        except ImportError:
            # PIL not available
            sys.stderr.write("Warning: cannot determine the image size; please install Pillow" + "\n")
            sys.stderr.flush()
        finally:
            b.close()

        return None, None


def _isinstance(obj, module, clsname):
    """A helper that works like isinstance(obj, module:clsname), but even when
    the module hasn't been imported or the type is not importable."""

    if module not in sys.modules:
        return False

    try:
        clstype = getattr(sys.modules[module], clsname)
        return isinstance(obj, clstype)
    except AttributeError:
        return False


def to_content_buf(data):
    # TODO: handle 'stream-like' data efficiently, rather than storing into RAM

    if isinstance(data, bytes):
        return data

    elif isinstance(data, io.BufferedReader):
        buf = data
        return buf.read()

    elif isinstance(data, io.TextIOWrapper):
        return data.buffer.read()

    elif _isinstance(data, 'numpy', 'ndarray'):
        # numpy ndarray: convert to png
        im = data
        if len(im.shape) == 2:
            mode = 'L'     # 8-bit pixels, grayscale
            im = im.astype(sys.modules['numpy'].uint8)
        elif len(im.shape) == 3 and im.shape[2] in (3, 4):
            mode = None    # RGB/RGBA
            if im.dtype.kind == 'f':
                im = (im * 255).astype('uint8')
        else:
            raise ValueError("Expected a 3D ndarray (RGB/RGBA image) or 2D (grayscale image), "
                             "but given shape: {}".format(im.shape))

        try:
            from PIL import Image
        except ImportError as e:
            raise ImportError(e.msg +
                              "\nTo draw numpy arrays, we require Pillow. " +
                              "(pip install Pillow)")       # TODO; reraise

        with io.BytesIO() as buf:
            # mode: https://pillow.readthedocs.io/en/4.2.x/handbook/concepts.html#concept-modes
            Image.fromarray(im, mode=mode).save(buf, format='png')
            return buf.getvalue()

    elif _isinstance(data, 'torch', 'Tensor'):
        # pytorch tensor: convert to png
        im = data
        try:
            from torchvision import transforms
        except ImportError as e:
            raise ImportError(e.msg +
                              "\nTo draw torch tensor, we require torchvision. " +
                              "(pip install torchvision)")

        with io.BytesIO() as buf:
            transforms.ToPILImage()(im).save(buf, format='png')
            return buf.getvalue()

    elif _isinstance(data, 'tensorflow.python.framework.ops', 'EagerTensor'):
        im = data
        return to_content_buf(im.numpy())

    elif _isinstance(data, 'PIL.Image', 'Image'):
        # PIL/Pillow images
        img = data

        with io.BytesIO() as buf:
            img.save(buf, format='png')
            return buf.getvalue()

    elif _isinstance(data, 'matplotlib.figure', 'Figure'):
        # matplotlib figures
        fig = data
        if fig.canvas is None:
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            FigureCanvasAgg(fig)

        with io.BytesIO() as buf:
            fig.savefig(buf)
            return buf.getvalue()

    else:
        raise TypeError("Unsupported type : {}".format(type(data)))


def get_tty_size():
    with open('/dev/tty') as tty:
        rows, columns = subprocess.check_output(['stty', 'size'], stdin=tty).split()
    return int(rows), int(columns)


def real_height(buf, pixels_per_line=24):
    im_width, im_height = get_image_shape(buf)
    if im_height:
        assert pixels_per_line > 0
        height = (im_height + (pixels_per_line - 1)) // pixels_per_line

        # automatically limit height to the current tty,
        # otherwise the image will be just erased
        try:
            tty_height, _ = get_tty_size()
            return max(1, min(height, tty_height - 9))
        except OSError:
            # may not be a terminal
            pass
    else:
        # image height unavailable, fallback?
        return 10


def imgcat(buf, width=None, height=None, preserve_aspect_ratio=True, fp=None):
    """
    Print image on terminal (iTerm2).

    Follows the file-transfer protocol of iTerm2 described at
    https://www.iterm2.com/documentation-images.html.

    Args:
        :param buf: the content of image in buffer interface, numpy array, etc.
        :param width: the width for displaying image, in number of characters (columns)
        :param height: the height for displaying image, in number of lines (rows)
        :param fp: The buffer to write to, defaults sys.stdout
        :param filename:
    """
    if fp is None:
        fp = sys.stdout.buffer  # for stdout, use buffer interface (py3)

    if len(buf) == 0:
        raise ValueError("Empty buffer")

    if height is None:
        height = real_height(buf)

    # need to detect tmux
    is_tmux = 'TMUX' in os.environ and 'tmux' in os.environ['TMUX']

    # tmux: print some margin and the DCS escape sequence for passthrough
    # In tmux mode, we need to first determine the number of actual lines
    if is_tmux:
        fp.write(b'\n' * height)
        # move the cursers back
        fp.write(CSI + b'?25l')
        fp.write(CSI + str(height).encode() + b"F")     # PEP-461
        fp.write(TMUX_WRAP_ST + b'\033')

    # now starts the iTerm2 file transfer protocol.
    fp.write(OSC)
    fp.write(b'1337;File=inline=1')
    fp.write(b';size=' + str(len(buf)).encode())
    fp.write(b';height=' + str(height).encode())
    if width:
        fp.write(b';width=' + str(width).encode())
    if not preserve_aspect_ratio:
        fp.write(b';preserveAspectRatio=0')
    fp.write(b':')
    fp.flush()

    buf_base64 = base64.b64encode(buf)
    fp.write(buf_base64)

    fp.write(ST)

    if is_tmux:
        # terminate DCS passthrough mode
        fp.write(TMUX_WRAP_ED)
        # move back the cursor lines down
        fp.write(CSI + str(height).encode() + b"E")
        fp.write(CSI + b'?25h')
    else:
        fp.write(b'\n')

    # flush is needed so that the cursor control sequence can take effect
    fp.flush()


def image_preview(img, is_url=False, set_proxy: str = '', set_referer: str = '',
                  qs_console_status=None):
    """
    在终端预览图片 | 目前仅有MacOS下的iTerm可用

    preview image on terminal | At present, only iTerm under MacOS is available

    :param is_url:
    :param img: opened file, numpy array, PIL.Image, matplotlib fig
    :param set_proxy: set proxy
    :param set_referer: set refer
    :param qs_console_status:
    :return:
    """
    try:
        if not is_url and isinstance(img, str):
            is_url = img.startswith('http')
        if is_url:
            from PIL import Image
            from io import BytesIO
            import requests
            if set_referer:
                headers['referer'] = set_referer
            proxies = {
                'http': 'http://' + set_proxy,
                'https': 'https://' + set_proxy
            } if set_proxy else {}
            res = requests.get(img, headers=headers, proxies=proxies).content
            if qs_console_status:
                qs_console_status.update(status='Opening')
            img = Image.open(BytesIO(res))
        if qs_console_status:
            qs_console_status.stop()

        buf = to_content_buf(img)
        width, height = get_image_shape(buf)
        _real_height = real_height(buf)
        _real_width = math.ceil(width / height * _real_height) * 2 + 1

        qs_default_console.print(' ' * int(max((qs_default_console.width - _real_width) / 2, 0)), end='')

        imgcat(buf, height=real_height(buf))
    except Exception as e:
        if qs_console_status:
            from .. import qs_error_string
            qs_default_console.print(qs_error_string, repr(e))
            qs_console_status.stop()
        return
