import random


def random_char_challenge(length):
    chars = 'abcdefghijklmnopqrstuvwxyz'
    ret = ''
    for i in range(length):
        ret += random.choice(chars)
    return ret.upper()


def filter_smooth(image, filter_code):
    return image.filter(filter_code)


def noise_dots(draw, image, fill):
    size = image.size
    for p in range(int(size[0] * size[1] * 0.1)):
        x = random.randint(0, size[0])
        y = random.randint(0, size[1])
        draw.point((x, y), fill=fill)
    return draw


def noise_arcs(draw, image, fill):
    size = image.size
    draw.arc([-20, -20, size[0], 20], 0, 295, fill=fill)
    draw.line([-20, 20, size[0] + 20, size[1] - 20], fill=fill)
    draw.line([-20, 0, size[0] + 20, size[1]], fill=fill)
    return draw


class OBJDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dict_obj):
    if not isinstance(dict_obj, dict):
        return dict_obj
    inst = OBJDict()
    for k, v in dict_obj.items():
        inst[k] = dict_to_object(v)
    return inst
