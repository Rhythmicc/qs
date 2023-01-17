from PIL import Image


def topng(imgPath: str):
    """
    将图片路径所指的图片转为jpg格式

    transform image to jpg

    :param imgPath: 图片路径 | image path
    :return:
    """
    Image.open(imgPath).save(imgPath + ".png", quality=100)


def tojpg(imgPath: str):
    """
    将图片路径所指的图片转为jpg格式

    transform image to jpg

    :param imgPath: 图片路径 | image path
    :return:
    """
    Image.open(imgPath).convert("RGB").save(imgPath + ".jpg", quality=100)


def imgsConcat(imgs: list):
    """
    合并图片
    """

    from io import BytesIO
    from .. import (
        terminal_font_size,
        requirePackage,
        qs_default_console,
        qs_default_status,
        qs_error_string,
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
        heights_len = min(len(imgs), 3)

        one_width = int(
            qs_default_console.width * terminal_font_size / heights_len / 2.125
        )

        heights = [0] * heights_len
        for i in imgs:
            one_height = int(one_width * i.size[1] / i.size[0])
            heights[heights.index(min(heights))] += one_height

        st.update("嗅探最佳拼接方式")
        max_height = qs_default_console.height * terminal_font_size

        while max(heights) > max_height and heights_len < len(imgs):
            heights_len += 1
            heights = [0] * heights_len
            one_width = int(
                qs_default_console.width / heights_len * terminal_font_size / 2.125
            )
            for i in imgs:
                one_height = int(one_width * i.size[1] / i.size[0])
                heights[heights.index(min(heights))] += one_height

        result = Image.new("RGBA", (one_width * heights_len, max(heights)))
        heights = [0] * heights_len

        imgs = [
            i.resize((one_width, int(one_width * i.size[1] / i.size[0]))) for i in imgs
        ]
        imgs = sorted(imgs, key=lambda i: -i.size[0] * i.size[1])

        for i in imgs:
            min_height_index = heights.index(min(heights))
            result.paste(i, (one_width * min_height_index, heights[min_height_index]))
            heights[min_height_index] += i.size[1]
    return result
