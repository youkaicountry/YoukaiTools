uh_i = ["width", "height", "bits_per_pixel", "bits_per_channel", "number_of_channels", "channel_order", "dpi_x", "dpi_y", "data_pad_bits", "interlace"]

def getBlankUnifiedHeader():
    outh = {}
    for n in uh_i:
        outh[n] = None
    return outh

