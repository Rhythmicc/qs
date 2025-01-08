"""
在终端预览图片 | 仅有MacOS下的iTerm2可用

preview image on terminal | Only iTerm2 is available,
"""
from .. import qs_default_console, qs_console_width, qs_default_status
from .. import _ask, user_lang, force_show_img, qs_config
import math
import base64
import sys
import os
import struct
import io

# 记录强制显示状态，避免重复询问
is_iterm2 = "ITERM_SESSION_ID" in os.environ
is_kitty = "KITTY_PID" in os.environ or "GHOSTTY_BIN_DIR" in os.environ
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
            from .. import requirePackage
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


def to_content_buf(data, fmt="png", width: int = 0, height: int = 0, bypass=False):
    # TODO: handle 'stream-like' data efficiently, rather than storing into RAM
    from .. import requirePackage
    if bypass:
        return data
    
    if isinstance(data, bytes):
        # force transform data to png format
        img = requirePackage("PIL", "Image", "Pillow").open(io.BytesIO(data))
        if width and height:
            rate = img.size[0] / img.size[1]
            ass_height = width / rate
            ass_width = rate * height
            if ass_height > height:
                width = math.floor(height * rate)
            if ass_width > width:
                height = math.floor(width / rate)
            img = img.resize((width, height))
        with io.BytesIO() as buf:
            img.save(buf, format=fmt)
            return buf.getvalue()

    elif isinstance(data, io.BufferedReader):
        buf = data
        if width and height:
            img = requirePackage("PIL", "Image", "Pillow").open(buf)
            rate = img.size[0] / img.size[1]
            ass_height = width / rate
            ass_width = rate * height
            if ass_height > height:
                width = math.floor(height * rate)
            if ass_width > width:
                height = math.floor(width / rate)
            img = img.resize((width, height))
            with io.BytesIO() as buf:
                img.save(buf, format=fmt)
                return buf.getvalue()
        return buf.read()

    elif isinstance(data, io.TextIOWrapper):
        buf = data.buffer
        if width and height:
            img = requirePackage("PIL", "Image", "Pillow").open(buf)
            rate = img.size[0] / img.size[1]
            ass_height = width / rate
            ass_width = rate * height
            if ass_height > height:
                width = math.floor(height * rate)
            if ass_width > width:
                height = math.floor(width / rate)
            img = img.resize((width, height))
            with io.BytesIO() as buf:
                img.save(buf, format=fmt)
                return buf.getvalue()
        return buf.read()

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
            img = requirePackage("PIL", "Image", "Pillow").fromarray(im, mode=mode)
            if width and height:
                rate = img.size[0] / img.size[1]
                ass_height = width / rate
                ass_width = rate * height
                if ass_height > height:
                    width = math.floor(height * rate)
                if ass_width > width:
                    height = math.floor(width / rate)
                img = img.resize((width, height))
            img.save(buf, format=fmt)
            return buf.getvalue()

    elif _isinstance(data, "torch", "Tensor"):
        # pytorch tensor: convert to png
        from .. import requirePackage

        im = data

        with io.BytesIO() as buf:
            img = requirePackage("torchvision", "transforms").ToPILImage()(im)
            if width and height:
                rate = img.size[0] / img.size[1]
                ass_height = width / rate
                ass_width = rate * height
                if ass_height > height:
                    width = math.floor(height * rate)
                if ass_width > width:
                    height = math.floor(width / rate)
                img = img.resize((width, height))
            img.save(buf, format=fmt)
            return buf.getvalue()

    elif _isinstance(data, "tensorflow.python.framework.ops", "EagerTensor"):
        im = data
        return to_content_buf(im.numpy())

    elif _isinstance(data, "PIL.Image", "Image"):
        # PIL/Pillow images
        img = data

        with io.BytesIO() as buf:
            if width and height:
                rate = img.size[0] / img.size[1]
                ass_height = width / rate
                ass_width = rate * height
                if ass_height > height:
                    width = math.floor(height * rate)
                if ass_width > width:
                    height = math.floor(width / rate)
                img = img.resize((width, height))
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
            if width and height:
                img = requirePackage("PIL", "Image", "Pillow").open(buf)
                rate = img.size[0] / img.size[1]
                ass_height = width / rate
                ass_width = rate * height
                if ass_height > height:
                    width = math.floor(height * rate)
                if ass_width > width:
                    height = math.floor(width / rate)
                img = img.resize((width, height))
                buf = io.BytesIO()
                img.save(buf, format=fmt)
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

    if is_iterm2:
        # if not is_iterm2 and not force_show:
        #     raise RuntimeError(
        #         "This function is only supported in iTerm2. "
        #         "Please set `force_show=True` to force show the image."
        #     )
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
    elif is_kitty:
        # Kitty graphics protocol
        # https://sw.kovidgoyal.net/kitty/graphics-protocol.html
        from base64 import standard_b64encode
        def serialize_gr_command(**cmd):
            payload = cmd.pop('payload', None)
            cmd = ','.join(f'{k}={v}' for k, v in cmd.items())
            ans = []
            w = ans.append
            w(b'\033_G'), w(cmd.encode('ascii'))
            if payload:
                w(b';')
                w(payload)
            w(b'\033\\')
            return b''.join(ans)

        def write_chunked(**cmd):
            data = standard_b64encode(cmd.pop('data'))
            while data:
                chunk, data = data[:4096], data[4096:]
                m = 1 if data else 0
                fp.write(serialize_gr_command(payload=chunk, m=m, **cmd))
                fp.flush()
                cmd.clear()
            fp.write(b"\n")
            fp.flush()
        write_chunked(a='T', f=100, data=buf)
    else:
        raise RuntimeError(
            "This function is only supported in iTerm2. "
        )


def imgcat_stream(
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

    is_iterm2 = "ITERM_SESSION_ID" in os.environ

    if not is_iterm2 and not force_show:
        raise RuntimeError(
            "This function is only supported in iTerm2. "
            "Please set `force_show=True` to force show the image."
        )
    # now starts the iTerm2 file transfer protocol.
    fp.write(OSC)
    fp.write(b"1337;File=inline=1")
    fp.write(b";size=" + str(len(buf[1])).encode())
    if width_scale:
        fp.write(b";width=" + f'{width_scale}%%%%'.encode())
    if height_scale:
        fp.write(b";height=" + f'{height_scale}%%%%'.encode())
    if not preserve_aspect_ratio:
        fp.write(b";preserveAspectRatio=0")
    fp.write(b";inline=1")
    fp.write(b":")
    fp.flush()
    # fp.write(base64.b64encode(buf))
    buf = buf[0]
    for chunk in buf.iter_content(24576):
        fp.write(base64.b64encode(chunk))
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
    from .. import requirePackage

    global force_show_option, has_set_force_show_option
    try:
        bypass_flag = False
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
                write_to_memory=True
            ):
                if img.endswith('.svg'):
                    img_bytes = requirePackage("cairosvg", "svg2png")(bytestring=img_bytes)
                    bypass_flag = True
                img = img_bytes
            else:
                return qs_default_console.print(
                    requirePackage('.', 'qs_error_string'),
                    "Failed to download image" if user_lang != "zh" else "图片下载失败",
                )
        elif isinstance(img, str) and os.path.exists(img):
            if img.endswith('.svg') or img.endswith('.svgz'):
                qs_default_console.print(requirePackage('.', 'qs_warning_string'), 'Convert svg to png (dpi=300) ...' if user_lang != 'zh' else 'svg将转换为png (dpi=300) ...')
                img = requirePackage("io", "BytesIO")(requirePackage("cairosvg", "svg2png")(url=img, dpi=300))
                bypass_flag = True
            elif img.endswith('.eps') or img.endswith('.epsf') or img.endswith('.epsi'):
                qs_default_console.print(requirePackage('.', 'qs_warning_string'), 'Convert eps to png (dpi=300) ...' if user_lang != 'zh' else 'eps将转换为png (dpi=300) ...')
                img = requirePackage("io", "BytesIO")(requirePackage("wand.image", "Image")(filename=img).make_blob())
                bypass_flag = True
            img = requirePackage("PIL", "Image", "Pillow").open(img)
        else:
            qs_default_console.print(
                requirePackage('.', 'qs_warning_string'),
                '将自适应解析图片格式' if user_lang != 'zh' else 'Will adaptively parse the image format',
            )

        _st = qs_default_status.status

        qs_default_status(
            "Loading image" if user_lang != "zh" else "正在加载图片",
        ).start()

        import array, fcntl, termios
        buf = array.array('H', [0, 0, 0, 0])
        fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, buf)
        theight, twidth, width, height = buf[0], buf[1], buf[2], buf[3]
        th_pixels = math.floor(height / theight)
        tw_pixels = math.floor(width / twidth)

        buf = to_content_buf(img, bypass=bypass_flag, width=width, height=height - (4 if is_kitty else 3) * th_pixels)
        iwidth, _ = get_image_shape(buf)
        tiwidth = math.ceil(iwidth / tw_pixels)
        pre_space = ' ' * ((twidth - tiwidth) // 2)
        qs_default_status.stop()
        print(pre_space, end='')
        sys.stdout.flush()
        imgcat(buf, force_show=force_show_option)

        if _st:
            qs_default_status.start()
    except Exception:
        qs_default_status.stop()
        qs_default_console.print_exception()
        return
