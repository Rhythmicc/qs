from PIL import Image
from .. import requirePackage


def is_svg(imgPath: str):
    """
    判断图片是否为svg格式

    check if the image is svg

    :param imgPath: 图片路径 | image path
    :return:
    """
    return imgPath.endswith(".svg") or imgPath.endswith('.svgz')


def is_eps(imgPath: str):
    """
    判断图片是否为eps格式

    check if the image is eps

    :param imgPath: 图片路径 | image path
    :return:
    """
    return imgPath.endswith(".eps") or imgPath.endswith('.epsi') or imgPath.endswith('.epsf')


def is_pdf(imgPath: str):
    """
    判断图片是否为pdf格式

    check if the image is pdf

    :param imgPath: 图片路径 | image path
    :return:
    """
    return imgPath.endswith(".pdf")


def is_heic(imgPath: str):
    """
    判断图片是否为heic格式

    check if the image is heic

    :param imgPath: 图片路径 | image path
    :return:
    """
    return imgPath.endswith(".heic")


def is_pdf(imgPath: str):
    """
    判断图片是否为pdf格式

    check if the image is pdf

    :param imgPath: 图片路径 | image path
    :return:
    """
    return imgPath.endswith(".pdf")


def topng(imgPath: str):
    """
    将图片路径所指的图片转为jpg格式

    transform image to jpg

    :param imgPath: 图片路径 | image path
    :return:
    """
    if is_svg(imgPath):
        requirePackage("cairosvg", "svg2png")(
            url=imgPath, write_to=imgPath + ".png", dpi=300
        )
    elif is_eps(imgPath):
        requirePackage("wand.image", "Image")(filename=imgPath).save(filename=imgPath + ".png")
    elif is_heic(imgPath):
        requirePackage("pillow_heif", "read_heif")(imgPath).save(imgPath + ".png")
    elif is_pdf(imgPath):
        requirePackage('pdfplumber', 'open')(imgPath).pages[0].to_image(resolution=300).original.save(imgPath + ".png")
    else:
        Image.open(imgPath).save(imgPath + ".png", quality=100, optimize=True)


def tojpg(imgPath: str):
    """
    将图片路径所指的图片转为jpg格式

    transform image to jpg

    :param imgPath: 图片路径 | image path
    :return:
    """
    if is_svg(imgPath):
        imgPath = requirePackage("io", "BytesIO", "io")(
            requirePackage("cairosvg", "svg2png", "cairosvg")(url=imgPath, dpi=300)
        )
    elif is_eps(imgPath):
        imgPath = requirePackage("io", "BytesIO", "io")(
            requirePackage("wand.image", "Image", "wand.image")(filename=imgPath).make_blob()
        )
    elif is_heic(imgPath):
        imgPath = requirePackage("io", "BytesIO", "io")(
            requirePackage("pillow_heif", "read_heif")(imgPath).save_to_memory()
        )
    elif is_pdf(imgPath):
        imgPath = requirePackage('pdfplumber', 'open')(imgPath).pages[0].to_image(resolution=300).original.save(imgPath + ".jpg")
    else:
        Image.open(imgPath).convert("RGB").save(imgPath + ".jpg", quality=100, optimize=True)


def topdf(imgPath: str):
    """
    将图片路径所指的图片转为pdf格式

    transform image to pdf

    :param imgPath: 图片路径 | image path
    :return:
    """
    if is_svg(imgPath):
        requirePackage("cairosvg", "svg2pdf")(
            url=imgPath, write_to=imgPath + ".pdf", dpi=300
        )
    elif is_eps(imgPath):
        requirePackage("wand.image", "Image")(filename=imgPath).save(filename=imgPath + ".pdf")
    else:
        Image.open(imgPath).save(imgPath + ".pdf", quality=100, optimize=True)

def imgsConcat(imgs: list):
    """
    合并图片
    """

    from io import BytesIO
    from .. import (
        requirePackage,
        qs_default_console,
        qs_default_status,
        qs_error_string,
        qs_config,
    )

    Image = requirePackage("PIL", "Image", "Pillow")
    try:
        imgs = [Image.open(BytesIO(i)) for i in imgs if i]
    except:
        qs_default_console.print(qs_error_string, "样品图获取失败!")
        return

    if not imgs:
        qs_default_console.print(qs_error_string, "无样品图")
        return

    with qs_default_status("拼接图片中") as st:
        import array, fcntl, termios, sys
        buf = array.array('H', [0, 0, 0, 0])
        fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, buf)
        width, max_height = buf[2], buf[3]
        one_width = width
        heights_len = min(len(imgs), 3)
        heights = [0] * heights_len
        for i in imgs:
            one_height = int(one_width * i.size[1] / i.size[0])
            heights[heights.index(min(heights))] += one_height

        st.update("嗅探最佳拼接方式")

        while max(heights) > max_height and heights_len < len(imgs):
            heights_len += 1
            heights = [0] * heights_len
            one_width = int(width / heights_len)
            for i in imgs:
                one_height = int(one_width * i.size[1] / i.size[0])
                heights[heights.index(min(heights))] += one_height

        result = Image.new("RGBA", (one_width * heights_len * heights_len, max(heights) * heights_len))
        heights = [0] * heights_len

        imgs = [
            i.resize((one_width * heights_len, int(one_width * i.size[1] / i.size[0]) * heights_len)) for i in imgs
        ]
        imgs = sorted(imgs, key=lambda i: -i.size[0] * i.size[1])

        for i in imgs:
            min_height_index = heights.index(min(heights))
            result.paste(i, (one_width * heights_len * min_height_index, heights[min_height_index]))
            heights[min_height_index] += i.size[1]
    return result
