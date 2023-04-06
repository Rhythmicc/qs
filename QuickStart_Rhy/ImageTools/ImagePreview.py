"""
在终端预览图片 | 仅有MacOS下的iTerm2可用

preview image on terminal | Only iTerm2 is available,
"""
from .. import qs_default_console, qs_console_width, requirePackage, qs_default_status
from .. import _ask, user_lang, force_show_img, qs_config
import math
import base64
import sys
import os
import struct
import io

# 记录强制显示状态，避免重复询问
force_show_option = False
has_set_force_show_option = False

TMUX_WRAP_ST = b"\033Ptmux;"
TMUX_WRAP_ED = b"\033\\"

OSC = b"\033]"
CSI = b"\033["
ST = b"\a"  # \a = ^G (bell)


def get_image_shape(buf):
    """
    Extracts image shape as 2-tuple (width, height) from the content buffer.

    Supports GIF, PNG and other image types (e.g. JPEG) if PIL/Pillow is installed.
    Returns (None, None) if it can't be identified.
    """

    def _unpack(fmt, buffer, mode="Image"):
        try:
            return struct.unpack(fmt, buffer)
        except struct.error:
            raise ValueError("Invalid {} file".format(mode))

    # TODO: handle 'stream-like' data efficiently, not storing all the content into memory
    L = len(buf)

    if L >= 10 and buf[:6] in (b"GIF87a", b"GIF89a"):
        return _unpack("<hh", buf[6:10], mode="GIF")
    elif L >= 24 and buf.startswith(b"\211PNG\r\n\032\n") and buf[12:16] == b"IHDR":
        return _unpack(">LL", buf[16:24], mode="PNG")
    elif L >= 16 and buf.startswith(b"\211PNG\r\n\032\n"):
        return _unpack(">LL", buf[8:16], mode="PNG")
    else:
        # everything else: get width/height from PIL
        # TODO: it might be inefficient to write again the memory-loaded content to buffer...
        b = io.BytesIO()
        b.write(buf)

        try:
            im = requirePackage("PIL", "Image", "Pillow").open(b)
            return im.width, im.height
        except (IOError, OSError) as ex:
            # PIL.Image.open throws an error -- probably invalid byte input are given
            sys.stderr.write(
                "Warning: PIL cannot identify image; this may not be an image file"
                + "\n"
            )
        except ImportError:
            # PIL not available
            sys.stderr.write(
                "Warning: cannot determine the image size; please install Pillow" + "\n"
            )
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


def to_content_buf(data, fmt="png"):
    # TODO: handle 'stream-like' data efficiently, rather than storing into RAM

    if isinstance(data, bytes):
        return data

    elif isinstance(data, io.BufferedReader):
        buf = data
        return buf.read()

    elif isinstance(data, io.TextIOWrapper):
        return data.buffer.read()

    elif _isinstance(data, "numpy", "ndarray"):
        # numpy ndarray: convert to png
        im = data
        if len(im.shape) == 2:
            mode = "L"  # 8-bit pixels, grayscale
            im = im.astype(sys.modules["numpy"].uint8)
        elif len(im.shape) == 3 and im.shape[2] in (3, 4):
            mode = None  # RGB/RGBA
            if im.dtype.kind == "f":
                im = (im * 255).astype("uint8")
        else:
            raise ValueError(
                "Expected a 3D ndarray (RGB/RGBA image) or 2D (grayscale image), "
                "but given shape: {}".format(im.shape)
            )

        with io.BytesIO() as buf:
            # mode: https://pillow.readthedocs.io/en/4.2.x/handbook/concepts.html#concept-modes
            requirePackage("PIL", "Image", "Pillow").fromarray(im, mode=mode).save(
                buf, format=fmt
            )
            return buf.getvalue()

    elif _isinstance(data, "torch", "Tensor"):
        # pytorch tensor: convert to png
        from .. import requirePackage

        im = data

        with io.BytesIO() as buf:
            requirePackage("torchvision", "transforms").ToPILImage()(im).save(
                buf, format=fmt
            )
            return buf.getvalue()

    elif _isinstance(data, "tensorflow.python.framework.ops", "EagerTensor"):
        im = data
        return to_content_buf(im.numpy())

    elif _isinstance(data, "PIL.Image", "Image"):
        # PIL/Pillow images
        img = data

        with io.BytesIO() as buf:
            img.save(buf, format=fmt)
            return buf.getvalue()

    elif _isinstance(data, "matplotlib.figure", "Figure"):
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


def real_height(buf, pixels_per_line=qs_config.basicSelect("terminal_font_size")):
    _, im_height = get_image_shape(buf)
    if im_height:
        assert pixels_per_line > 0
        height = (im_height + (pixels_per_line - 1)) // pixels_per_line

        # automatically limit height to the current tty,
        # otherwise the image will be just erased
        try:
            return max(1, min(height, qs_default_console.height - 9))
        except OSError:
            # may not be a terminal
            pass
    else:
        # image height unavailable, fallback?
        return 10


def imgcat(
    buf,
    width_scale=None,
    height_scale=None,
    preserve_aspect_ratio=True,
    fp=None,
    force_show: bool = False,
):
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

    is_iterm2 = "ITERM_SESSION_ID" in os.environ

    if not is_iterm2 and not force_show:
        raise RuntimeError(
            "This function is only supported in iTerm2. "
            "Please set `force_show=True` to force show the image."
        )
    # now starts the iTerm2 file transfer protocol.
    fp.write(OSC)
    fp.write(b"1337;File=inline=1")
    fp.write(b";size=" + str(len(buf)).encode())
    if width_scale:
        fp.write(b";width=" + f'{width_scale}%%%%'.encode())
    if height_scale:
        fp.write(b";height=" + f'{height_scale}%%%%'.encode())
    if not preserve_aspect_ratio:
        fp.write(b";preserveAspectRatio=0")
    fp.write(b";inline=1")
    fp.write(b":")
    fp.flush()
    fp.write(base64.b64encode(buf))
    fp.write(ST)
    fp.write(b"\n")
    # flush is needed so that the cursor control sequence can take effect
    fp.flush()


def image_preview(
    img,
    is_url=False,
    set_proxy: str = "",
    set_referer: str = "",
    set_width_in_rc_file: int = 0,
    set_height_in_rc_file: int = 0,
    force_show: bool = force_show_img,
):
    """
    在终端预览图片 | 目前仅有MacOS下的iTerm可用, 但你可以开启强制显示选项预览

    preview image on terminal | At present, only iTerm under MacOS is available, but you can enable force show option to preview

    :param force_show: 强制显示图片，即使终端非iTerm2
    :param set_width_in_rc_file: 设置图片宽度，以像素为单位，默认为0，即不设置
    :param is_url: 是否为url
    :param img: opened file, numpy array, PIL.Image, matplotlib fig
    :param set_proxy: set proxy
    :param set_referer: set refer
    :param _fake_show: 返回图片比特流，用于自定义显示
    :return:
    """
    global force_show_option, has_set_force_show_option
    try:
        if not (
            force_show_option
            or force_show
            or (
                not has_set_force_show_option
                and _ask(
                    {
                        "type": "confirm",
                        "message": "Preview image on this terminal?"
                        if user_lang != "zh"
                        else "确认在该终端预览图片?",
                        "default": False,
                    }
                )
            )
        ):
            has_set_force_show_option = True
            return
        else:
            has_set_force_show_option = True
            force_show_option = True
        if not is_url and (isinstance(img, str) and not os.path.exists(img)):
            is_url = img.startswith("http")

        if is_url:
            if img_bytes := requirePackage(".NetTools.NormalDL", "normal_dl")(
                img,
                set_referer=set_referer,
                set_proxy=set_proxy,
                disableStatus=True,
                write_to_memory=True,
            ):
                img = requirePackage("PIL", "Image", "Pillow").open(
                    requirePackage("io", "BytesIO")(img_bytes)
                )
            else:
                return qs_default_console.print(
                    requirePackage('.', 'qs_error_string'),
                    "Failed to download image" if user_lang != "zh" else "图片下载失败",
                )
        elif not is_url and isinstance(img, str) and os.path.exists(img):
            img = requirePackage("PIL", "Image", "Pillow").open(img)

        _st = qs_default_status.status

        qs_default_status(
            "Loading image" if user_lang != "zh" else "正在加载图片",
        ).start()

        buf = to_content_buf(img)

        qs_default_status("Calculating the position of the image" if user_lang != "zh" else "计算图片摆放位置")

        width, height = get_image_shape(buf)
        console_width = (
            qs_console_width if not set_width_in_rc_file else set_width_in_rc_file
        )
        console_height = qs_default_console.height if not set_height_in_rc_file else set_height_in_rc_file

        max_width_scale = set_width_in_rc_file / qs_console_width if set_width_in_rc_file else 1
        max_height_scale = set_height_in_rc_file / qs_default_console.height if set_height_in_rc_file else 1
        max_width_scale *= max_height_scale
        
        rate = width / height
        _real_height = math.ceil(height / qs_config.basicSelect("terminal_font_size"))
        _real_width = math.ceil(
            width
            * qs_config.basicSelect("terminal_font_rate", 2.049)
            / qs_config.basicSelect("terminal_font_size")
        )

        if _real_width > console_width:
            height_scale = console_width / _real_width
            _real_height = math.floor(_real_height * height_scale)
            _real_width = console_width
        if _real_height > console_height:
            width_scale = console_height / _real_height
            _real_width = math.floor(_real_width * width_scale)

        qs_default_status.stop()
        if rate > 1:
            imgcat(
                buf,
                width_scale=max_width_scale * 100,
                force_show=force_show_option,
            )
        else:
            qs_default_console.print(
                " " * math.floor((qs_console_width - _real_width) / 2),
                end="",
            )
            imgcat(
                buf,
                height_scale=max_height_scale * 100,
                force_show=force_show_option,
            )

        if _st:
            qs_default_status.start()
    except Exception:
        qs_default_status.stop()
        qs_default_console.print_exception()
        return
