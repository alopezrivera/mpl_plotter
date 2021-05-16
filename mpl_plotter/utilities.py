import matplotlib.font_manager

from Alexandria.general.console import print_color


def get_available_fonts():
    """
    :return: Print all available fonts
    """
    flist = matplotlib.font_manager.get_fontconfig_fonts()
    names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]

    print_color("Matplotlib: available fonts", "blue")
    for i in range(len(names)):
        n = f"{i+1}"
        numeral = n + "." + " "*(4-len(n))
        print(numeral+'"'+names[i]+'"')


get_available_fonts()
