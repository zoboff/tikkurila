# encoding=utf8


def rgb_to_hex(r, g, b) -> str:
    return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()


def hex_to_rgb(value) -> 'R, G, B':
    # correct the value
    value = value.lstrip('#')
    value = value.zfill(6)
    value = value[0:6]
    # R, G, B
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
