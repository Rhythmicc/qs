from PIL import Image


def transport_back(src: str, to_color, from_color=(0, 0, 0, 0)):
    src = Image.open(src)
    src = src.convert('RGBA')
    L, H = src.size
    color_0 = from_color
    transparency_flag = False if color_0[-1] else True
    for h_indx in range(H):
        for l_indx in range(L):
            dot = (l_indx, h_indx)
            color_1 = src.getpixel(dot)
            if transparency_flag and not color_1[-1]:
                src.putpixel(dot, to_color)
            elif color_0[:-1] == color_1[:-1]:
                src.putpixel(dot, to_color)
    return src


def get_color_from_str(str_color: str):
    if ',' in str_color:
        str_color = [int(i) for i in str_color.split(',')]
        if len(str_color) == 3:
            str_color.append(255)
        str_color = tuple(str_color)
    elif len(str_color) == 6:
        str_color = (int(str_color[:2], 16), int(str_color[2:4], 16), int(str_color[4:], 16), 255)
    else:
        exit('ERROR COLOR!')
    return str_color
