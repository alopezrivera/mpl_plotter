import os
import sys
from pathlib import Path
from importlib import util
from mpl_plotter.two_d import line as mpl_line2, scatter as mpl_scatter2
from mpl_plotter.three_d import line as mpl_line3, scatter as mpl_scatter3


class two_d():

    def __init__(self, preset_dir="", preset_name="preset_2d", direct_preset=None):
        global preset
        preset = find_preset(preset_dir, preset_name) if isinstance(direct_preset, type(None)) else direct_preset

    class line(mpl_line2):

        def __init__(self, x=None, y=None, **kwargs):

            input = {**preset, **kwargs}

            super().__init__(x=x, y=y, **input)

    class scatter(mpl_scatter2):

        def __init__(self, x=None, y=None, **kwargs):

            input = {**preset, **kwargs}

            super().__init__(x=x, y=y, **input)


class three_d:

    def __init__(self, preset_dir="", preset_name="preset_3d", direct_preset=None):
        global preset
        preset = find_preset(preset_dir, preset_name) if isinstance(direct_preset, type(None)) else direct_preset

    class line(mpl_line3):

        def __init__(self, x=None, y=None, **kwargs):

            input = {**preset, **kwargs}

            super().__init__(x=x, y=y, **input)

    class scatter(mpl_scatter3):

        def __init__(self, x=None, y=None, **kwargs):

            input = {**preset, **kwargs}

            super().__init__(x=x, y=y, **input)


def find_preset(dest, preset_name):
    preset_path = f"{'/'.join(sys.argv[0].split('/')[:-1])}/" + (f"{dest}/" if dest != "" else "") + f"{preset_name}.py"

    if os.path.isfile(preset_path):
        spec = util.spec_from_file_location(f"{dest}.{preset_name}" if dest != "" else f"{preset_name}", preset_path)
        preset = util.module_from_spec(spec)
        spec.loader.exec_module(preset)
    else:
        sys.exit(f"UNABLE TO RUN\n"
                 f"Preset file does not exist: {preset_path}\n\n"
                 f"     Please ensure the path is correct, or create it by calling:\n\n"
                 f"     from mpl_plotter.presets.custom import generate_preset_2d/3d\n"
                 f"     generate_preset_2d/3d()\n")

    return preset.preset


def make_preset_directory(preset_dest, preset_name):
    if preset_dest != "":
        Path(f"{preset_dest}/").mkdir(parents=True, exist_ok=True)
        with open(f"{preset_dest}/__init__.py", "w"): pass
    fname = "/".join(sys.argv[0].split("/")[:-1]) \
            + (f"/{preset_dest}" if preset_dest != "" else "") \
            + f"/{preset_name}.py"
    return fname


def generate_preset_2d(preset_dest="", overwrite=False, disable_warning=False, preset_name="preset_2d"):
    """
    :param preset_dest: Preset destination directory
    :param overwrite: Overwrite found presets automatically
    :param disable_warning: Disable overwriting warning
    :param preset_name: Name of preset to be created
    :return: None
    """

    fname = make_preset_directory(preset_dest, preset_name)

    preset = \
        'preset = {\n' \
        '    ## Backend\n' \
        '    #"backend": "Qt5Agg",\n' \
        '    ## Fonts\n' \
        '    #"font": "serif",\n' \
        '    #"math_font": "dejavuserif",\n' \
        '    #"font_color": "black",\n' \
        '    ## Figure\n' \
        '    ## axes\n' \
        '    #"fig": None,\n' \
        '    #"ax": None,\n' \
        '    #"figsize": (6, 6),\n' \
        '    #"shape_and_position": 111,\n' \
        '    #"prune": None,\n' \
        '    #"resize_axes": True,\n' \
        '    #"scale": None,\n' \
        '    #"aspect": 1,\n' \
        '    ## Setup\n' \
        '    #"workspace_color": None,\n' \
        '    #"workspace_color2": None,\n' \
        '    #"background_color_figure": "white",\n' \
        '    #"background_color_plot": "white",\n' \
        '    #"background_alpha": 1,\n' \
        '    #"style": None,\n' \
        '    #"light": None,\n' \
        '    #"dark": None,\n' \
        '    ## Spines\n' \
        '    #"spine_color": None,\n' \
        '    #"blend_edges": False,\n' \
        '    #"spines_removed": (0, 0, 1, 1),\n' \
        '    ## Bounds\n' \
        '    #"x_upper_bound": None,\n' \
        '    #"x_lower_bound": None,\n' \
        '    #"y_upper_bound": None,\n' \
        '    #"y_lower_bound": None,\n' \
        '    #"x_bounds": None,\n' \
        '    #"y_bounds": None,\n' \
        '    ## Pads\n' \
        '    #"demo_pad_plot": True,\n' \
        '    #"x_upper_resize_pad": 0,\n' \
        '    #"x_lower_resize_pad": 0,\n' \
        '    #"y_upper_resize_pad": 0,\n' \
        '    #"y_lower_resize_pad": 0,\n' \
        '    ## Grid\n' \
        '    #"grid": True,\n' \
        '    #"grid_color": "lightgrey",\n' \
        '    #"grid_lines": "-.",\n' \
        '    ## Color\n' \
        '    #"color": "darkred",\n' \
        '    #"cmap": "RdBu_r",\n' \
        '    #"alpha": None,\n' \
        '    #"norm": None,\n' \
        '    ## Title\n' \
        '    #"title": None,\n' \
        '    #"title_size": 12,\n' \
        '    #"title_y": 1.025,\n' \
        '    #"title_weight": None,\n' \
        '    #"title_font": None,\n' \
        '    #"title_color": None,\n' \
        '    ## Labels\n' \
        '    #"x_label": None,\n' \
        '    #"x_label_size": 20,\n' \
        '    #"x_label_pad": 10,\n' \
        '    #"x_label_rotation": None,\n' \
        '    #"x_label_weight": None,\n' \
        '    #"y_label": None,\n' \
        '    #"y_label_size": 20,\n' \
        '    #"y_label_pad": 10,\n' \
        '    #"y_label_rotation": None,\n' \
        '    #"y_label_weight": None,\n' \
        '    ## Ticks\n' \
        '    #"x_tick_number": 3,\n' \
        '    #"x_tick_labels": None,\n' \
        '    #"y_tick_number": 3,\n' \
        '    #"y_tick_labels": None,\n' \
        '    #"x_label_coords": None,\n' \
        '    #"y_label_coords": None,\n' \
        '    #"tick_color": None,\n' \
        '    #"tick_label_pad": 5,\n' \
        '    #"ticks_where": (1, 1, 0, 0),\n' \
        '    ## Tick labels\n' \
        '    #"tick_label_size": None,\n' \
        '    #"x_tick_label_size": 15,\n' \
        '    #"y_tick_label_size": 15,\n' \
        '    #"x_custom_tick_locations": None,\n' \
        '    #"y_custom_tick_locations": None,\n' \
        '    #"fine_tick_locations": True,\n' \
        '    #"x_custom_tick_labels": None,\n' \
        '    #"y_custom_tick_labels": None,\n' \
        '    #"x_date_tick_labels": False,\n' \
        '    #"date_format": "%Y-%m-%d",\n' \
        '    #"tick_ndecimals": 1,\n' \
        '    #"x_tick_ndecimals": None,\n' \
        '    #"y_tick_ndecimals": 3,\n' \
        '    #"x_tick_rotation": None,\n' \
        '    #"y_tick_rotation": None,\n' \
        '    #"tick_labels_where": (1, 1, 0, 0),\n' \
        '    ## Color bar\n' \
        '    #"color_bar": False,\n' \
        '    #"cb_pad": 0.2,\n' \
        '    #"cb_axis_labelpad": 10,\n' \
        '    #"shrink": 0.75,\n' \
        '    #"extend": "neither",\n' \
        '    #"cb_title": None,\n' \
        '    #"cb_orientation": "vertical",\n' \
        '    #"cb_title_rotation": None,\n' \
        '    #"cb_title_style": "normal",\n' \
        '    #"cb_title_size": 10,\n' \
        '    #"cb_top_title_y": 1,\n' \
        '    #"cb_ytitle_labelpad": 10,\n' \
        '    #"cb_title_weight": "normal",\n' \
        '    #"cb_top_title": False,\n' \
        '    #"cb_y_title": False,\n' \
        '    #"cb_top_title_pad": None,\n' \
        '    #"x_cb_top_title": 0,\n' \
        '    #"cb_vmin": None,\n' \
        '    #"cb_vmax": None,\n' \
        '    #"cb_hard_bounds": False,\n' \
        '    #"cb_outline_width": None,\n' \
        '    #"cb_tick_number": 5,\n' \
        '    #"cb_ticklabelsize": 10,\n' \
        '    #"tick_ndecimals_cb": None,\n' \
        '    ## Legend\n' \
        '    #"plot_label": None,\n' \
        '    #"legend": False,\n' \
        '    #"legend_loc": "upper right",\n' \
        '    #"legend_bbox_to_anchor": None,\n' \
        '    #"legend_size": 15,\n' \
        '    #"legend_weight": "normal",\n' \
        '    #"legend_style": "normal",\n' \
        '    #"legend_handleheight": None,\n' \
        '    #"legend_ncol": 1,\n' \
        '    ## Subplots\n' \
        '    #"show": False,\n' \
        '    #"zorder": None,\n' \
        '    ## Save\n' \
        '    #"filename": None,\n' \
        '    #"dpi": None,\n' \
        '    ## Suppress output\n' \
        '    #"suppress": True,\n' \
        '}'

    if not disable_warning:
        if os.path.isfile(fname):
            ow = "The preset file will be overwritten. Change this by setting **overwrite=False** in the call.\n"
            no_ow = "The preset file will not be overwritten. Change this by setting **overwrite=True** in the call.\n"
            disable = "Disable this warning by setting **disable_warning=True** in the call.\n"
            print("WARNING: OVERWRITING CURRENT PRESET FILE?\n" + (ow if overwrite else no_ow) + disable)

    if os.path.isfile(fname):
        if overwrite:
            with open(fname, "w") as file:
                print(preset, file=file)
        else:
            pass
    else:
        with open(fname, "w") as file:
            print(preset, file=file)


def generate_preset_3d(preset_dest="", overwrite=False, disable_warning=False, preset_name="preset_3d"):
    """
    :param preset_dest: Preset destination directory
    :param overwrite: Overwrite found presets automatically
    :param disable_warning: Disable overwriting warning
    :param preset_name: Name of preset to be created
    :return: None
    """

    fname = make_preset_directory(preset_dest, preset_name)

    preset = \
    'preset = { \n' \
    '    ## Scale \n' \
    '    # "x_scale": 1, \n' \
    '    # "y_scale": 1, \n' \
    '    # "z_scale": 1, \n' \
    '    ## Backend \n' \
    '    # "backend": "Qt5Agg", \n' \
    '    ## Fonts \n' \
    '    # "font": "serif", \n' \
    '    # "math_font": "dejavuserif", \n' \
    '    # "font_color": "black", \n' \
    '    ## Figure, axis \n' \
    '    # "fig": None, \n' \
    '    # "ax": None, \n' \
    '    # "figsize": None, \n' \
    '    # "shape_and_position": 111, \n' \
    '    # "azim": -137, \n' \
    '    # "elev": 26, \n' \
    '    ## Setup \n' \
    '    # "prune": None, \n' \
    '    # "resize_axes": True, \n' \
    '    # "aspect": 1, \n' \
    '    # "box_to_plot_pad": 10, \n' \
    '    ## Spines \n' \
    '    # "spines_juggled": (1,0,2), \n' \
    '    # "spine_color": None, \n' \
    '    # "workspace_color": None, \n' \
    '    # "workspace_color2": None, \n' \
    '    # "background_color_figure": "white", \n' \
    '    # "background_color_plot": "white", \n' \
    '    # "background_alpha": 1, \n' \
    '    # "style": None, \n' \
    '    # "light": None, \n' \
    '    # "dark": None, \n' \
    '    # "pane_fill": None, \n' \
    '    ## Bounds \n' \
    '    # "x_upper_bound": None, \n' \
    '    # "x_lower_bound": None, \n' \
    '    # "y_upper_bound": None, \n' \
    '    # "y_lower_bound": None, \n' \
    '    # "z_upper_bound": None, \n' \
    '    # "z_lower_bound": None, \n' \
    '    # "x_bounds": None, \n' \
    '    # "y_bounds": None, \n' \
    '    # "z_bounds": None, \n' \
    '    ## Pads \n' \
    '    # "demo_pad_plot": False, \n' \
    '    # "x_upper_resize_pad": 0, \n' \
    '    # "x_lower_resize_pad": 0, \n' \
    '    # "y_upper_resize_pad": 0, \n' \
    '    # "y_lower_resize_pad": 0, \n' \
    '    # "z_upper_resize_pad": 0, \n' \
    '    # "z_lower_resize_pad": 0, \n' \
    '    ## Axes \n' \
    '    # "show_axes": True, \n' \
    '    ## Grid \n' \
    '    # "grid": True, \n' \
    '    # "grid_color": "lightgrey", \n' \
    '    # "grid_lines": "-.", \n' \
    '    ## Color \n' \
    '    # "color": "darkred", \n' \
    '    # "cmap": "RdBu_r", \n' \
    '    # "alpha": 1, \n' \
    '    ## Title \n' \
    '    # "title": None, \n' \
    '    # "title_weight": "normal", \n' \
    '    # "title_size": 12, \n' \
    '    # "title_y": 1.025, \n' \
    '    # "title_color": None, \n' \
    '    # "title_font": None, \n' \
    '    ## Labels \n' \
    '    # "x_label": "x", \n' \
    '    # "x_label_weight": "normal", \n' \
    '    # "x_label_size": 12, \n' \
    '    # "x_label_pad": 7, \n' \
    '    # "x_label_rotation": None, \n' \
    '    # "y_label": "y", \n' \
    '    # "y_label_weight": "normal", \n' \
    '    # "y_label_size": 12, \n' \
    '    # "y_label_pad": 7, \n' \
    '    # "y_label_rotation": None, \n' \
    '    # "z_label": "z", \n' \
    '    # "z_label_weight": "normal", \n' \
    '    # "z_label_size": 12, \n' \
    '    # "z_label_pad": 7, \n' \
    '    # "z_label_rotation": None, \n' \
    '    ## Ticks \n' \
    '    # "x_tick_number": 5, \n' \
    '    # "x_tick_labels": None, \n' \
    '    # "x_custom_tick_labels": None, \n' \
    '    # "x_custom_tick_locations": None, \n' \
    '    # "y_tick_number": 5, \n' \
    '    # "y_tick_labels": None, \n' \
    '    # "y_custom_tick_labels": None, \n' \
    '    # "y_custom_tick_locations": None, \n' \
    '    # "z_tick_number": 5, \n' \
    '    # "z_tick_labels": None, \n' \
    '    # "z_custom_tick_labels": None, \n' \
    '    # "z_custom_tick_locations": None, \n' \
    '    # "x_tick_rotation": None, \n' \
    '    # "y_tick_rotation": None, \n' \
    '    # "z_tick_rotation": None, \n' \
    '    # "tick_color": None, \n' \
    '    # "tick_label_pad": 4, \n' \
    '    # "tick_ndecimals": 1, \n' \
    '    ## Tick labels \n' \
    '    # "tick_label_size": 8.5, \n' \
    '    # "x_tick_label_size": None, \n' \
    '    # "y_tick_label_size": None, \n' \
    '    # "z_tick_label_size": None, \n' \
    '    ## Color bar \n' \
    '    # "color_bar": False, \n' \
    '    # "extend": "neither", \n' \
    '    # "shrink": 0.75, \n' \
    '    # "cb_title": None, \n' \
    '    # "cb_axis_labelpad": 10, \n' \
    '    # "cb_tick_number": 5, \n' \
    '    # "cb_outline_width": None, \n' \
    '    # "cb_title_rotation": None, \n' \
    '    # "cb_title_style": "normal", \n' \
    '    # "cb_title_size": 10, \n' \
    '    # "cb_top_title_y": 1, \n' \
    '    # "cb_ytitle_labelpad": 10, \n' \
    '    # "cb_title_weight": "normal", \n' \
    '    # "cb_top_title": False, \n' \
    '    # "cb_y_title": False, \n' \
    '    # "cb_top_title_pad": None, \n' \
    '    # "x_cb_top_title": 0, \n' \
    '    # "cb_vmin": None, \n' \
    '    # "cb_vmax": None, \n' \
    '    # "cb_ticklabelsize": 10, \n' \
    '    ## Legend \n' \
    '    # "plot_label": None, \n' \
    '    # "legend": False, \n' \
    '    # "legend_loc": "upper right", \n' \
    '    # "legend_size": 13, \n' \
    '    # "legend_weight": "normal", \n' \
    '    # "legend_style": "normal", \n' \
    '    # "legend_handleheight": None, \n' \
    '    # "legend_ncol": 1, \n' \
    '    ## Subplots \n' \
    '    # "show": False, \n' \
    '    # "newplot": False, \n' \
    '    ## Save \n' \
    '    # "filename": None, \n' \
    '    # "dpi": None, \n' \
    '    ## Suppress output \n' \
    '    # "suppress": True, \n' \
    '}'

    if not disable_warning:
        if os.path.isfile(fname):
            ow = "The preset file will be overwritten. Change this by setting **overwrite=False** in the call.\n"
            no_ow = "The preset file will not be overwritten. Change this by setting **overwrite=True** in the call.\n"
            disable = "Disable this warning by setting **disable_warning=True** in the call.\n"
            print("WARNING: OVERWRITING CURRENT PRESET FILE?\n" + (ow if overwrite else no_ow) + disable)

    if os.path.isfile(fname):
        if overwrite:
            with open(fname, "w") as file:
                print(preset, file=file)
        else:
            pass
    else:
        with open(fname, "w") as file:
            print(preset, file=file)
