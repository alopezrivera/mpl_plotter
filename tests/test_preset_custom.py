from mpl_plotter.presets.custom import generate_preset_2d, two_d
from mpl_plotter.presets.custom import generate_preset_3d, three_d


def test_2d():

    generate_preset_2d(preset_dest="presets", preset_name="MYPRESET2D", disable_warning=True, overwrite=False)

    # Proceed to customize your 2D plots using the preset

    my_plot = two_d(preset_dir="presets", preset_name="MYPRESET2D").line

    my_plot(show=True, demo_pad_plot=True, color="blue", title="TITLE", title_size=200, aspect=1)


def test_3d():

    generate_preset_3d(preset_dest="presets", preset_name="MYPRESET3D", disable_warning=True, overwrite=False)

    # Proceed to customize your 2D plots using the preset

    my_plot = three_d(preset_dir="presets", preset_name="MYPRESET3D").line

    my_plot(show=True, demo_pad_plot=True, color="blue", title="TITLE", title_size=100, aspect=1)


test_3d()
