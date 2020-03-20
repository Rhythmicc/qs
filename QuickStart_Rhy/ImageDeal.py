import sys
import os


def set_img_background():
    from QuickStart_Rhy.ImageDeal.ColorTools import transport_back, get_color_from_str

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
