# coding=utf-8
"""
修改图像颜色工具

Modify image color tool
"""
from .. import requirePackage

Image = requirePackage("PIL", "Image")


def transport_back(
    src: str, to_color: tuple, from_color: tuple = (0, 0, 0, 0)
) -> Image.Image:
    """
    图片颜色替换

    Image color replacement

    :param src: 图片路径
    :param to_color: RGBA四元组 -> 转换至目标颜色
    :param from_color: RGBA四元组 -> 需要被转换的颜色
    :return:
    """
    src = Image.open(src)
    src = src.convert("RGBA")
    L, H = src.size
    color_0 = from_color
    transparency_flag = False if color_0[-1] else True
    for h_indx in range(H):
        for l_indx in range(L):
            dot = (l_indx, h_indx)
            color_1 = src.getpixel(dot)
            if transparency_flag and not color_1[-1]:
                src.putpixel(dot, to_color)
            elif color_0[:-1] == color_1[:-1] and color_1[-1]:
                src.putpixel(dot, to_color)
    return src


def formatOneColor(src: str, to_color: tuple, except_color=None) -> Image.Image:
    """
    格式化图片颜色

    Format image color

    :param src: 图片路径
    :param to_color: RGBA四元组 -> 转换至目标颜色
    :param except_color: RGBA四元组 -> 忽略的颜色
    :return:
    """
    if except_color is None:
        except_color = [(0, 0, 0, 0)]
    src = Image.open(src)
    src = src.convert("RGBA")
    L, H = src.size
    for h_indx in range(H):
        for l_indx in range(L):
            color_1 = src.getpixel(dot := (l_indx, h_indx))
            if color_1 not in except_color:
                src.putpixel(dot, to_color)
    return src


def get_color_from_str(str_color: str) -> tuple:
    """
    解析字符串为RGBA四元组

    Parse strings for RGBA quaternions

    :param str_color: 表示颜色的字符串(支持16进制、RGB或RGBA) | String representing color (hex, RGB, or RGBA support)
    :return: RGBA四元组 | RGBA quad
    """
    if "," in str_color:
        str_color = [int(i) for i in str_color.split(",")]
        if len(str_color) == 3:
            str_color.append(255)
        str_color = tuple(str_color)
    elif len(str_color) == 6:
        str_color = (
            int(str_color[:2], 16),
            int(str_color[2:4], 16),
            int(str_color[4:], 16),
            255,
        )
    else:
        exit("ERROR COLOR!")
    return str_color
