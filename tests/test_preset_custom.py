import unittest

from mpl_plotter.presets.custom import generate_preset_2d, two_d
from mpl_plotter.presets.custom import generate_preset_3d, three_d


class PresetTests(unittest.TestCase):

    def test_2d(self):
        """
        Preferred use:

            generate_preset_2d(preset_dest="presets", preset_name="MYPRESET2D", disable_warning=True, overwrite=False)

            my_plot = three_d(preset_dir="presets", preset_name="MYPRESET2D").line

        Use to enable testing:
        """
        from tests.presets.MYPRESET2D import preset
        my_plot = two_d(direct_preset=preset).line

        my_plot(show=True, demo_pad_plot=True, color="blue", title="TITLE")

    def test_3d(self):
        """
        Preferred use:

            generate_preset_3d(preset_dest="presets", preset_name="MYPRESET3D", disable_warning=True, overwrite=False)

            my_plot = three_d(preset_dir="presets", preset_name="MYPRESET3D").line

        Use to enable testing:
        """
        from tests.presets.MYPRESET3D import preset
        my_plot = three_d(direct_preset=preset).line

        my_plot(show=True, demo_pad_plot=True, color="blue", title="TITLE")

