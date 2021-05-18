

# MPL Plotter 

![alt text](tests/coverage/coverage.svg ".coverage available in tests/coverage/")

<div style="text-align:center"><img align="right" width="135" height="135" src="_demo/gallery/showcase/logo.png" /></div>
Making plots for technical documents can be a time sink. At some point, I decided I might as well rid myself of that overhead, and learn some Python along the way!
This library is the result of that. It does the job for me and I expand it when it can't. Some parts of the API are unstable (in those cases, you'll be warned in the section where the method is discussed) and the defaults might not be your cup of tea, but it might still do the trick! Hope you find some use in it.


`Antonio Lopez Rivera, 2020`

## Table of Contents

### [ **1. Introduction** ](#1-introduction)

### [ **2. Install**  ](#2-install)

### [ **3. Map of the library** ](#3-map-of-the-library)

### [ **4. Capabilities** ](#4-capabilities)

### [ **5. Getting started** ](#5-getting-started)

[ _5.1 2D Lines_ ](#51-2d-lines)

[ _5.2 3D Lines_ ](#52-3d-lines)    

### [ **6. Base methods: examples, status** ](#6-base-methods-examples-status)

[ _6.1 2D_ ](#61-2d)

[ _6.2 3D_ ](#62-3d)

[ _6.3 Plot combination examples_ ](#63-plot-combination-examples)

### [ **7. Matplotlib compatibility** ](#7-matplotlib-compatibility)

[ _7.1 Retrieving axes, figures_ ](#71-retrieving-axes-figures)

[ _7.2 Using Matplotlib's axis tiling_ ](#72-using-matplotlibs-axis-tiling)

### [ **8. Advanced plotting: Presets and `custom_canvas`** ](#8-advanced-plotting-presets-and-custom_canvas)

[ _8.1 Custom presets_ ](#81-custom-presets)

[ _8.2 Standard presets_ ](#82-standard-presets)

[ _8.3_ `custom_canvas` ](#83-custom_canvas)

### [ **9. Unstable functionality: `panes`** ](#9-unstable-functionality-panes)

[ _9.1_ `n_pane_single` ](#91-n_pane_single)

[ _9.2_ `n_pane_comparison` ](#92-n_pane_comparison)

[ _9.3 Bunch of panes_ ](#93-bunch-of-panes)

### [ **10. Contributing** ](#10-contributing)

### [ **11. All modifiable parameters** ](#11-all-modifiable-parameters)

# 1. Introduction 

MPL Plotter is a Matplotlib based Python plotting library built with the goals of achieving publication-quality plots in an efficient and comprehensive way. 

---

The fundamental premise of MPL Plotter is to:
- Generate publication quality plots in a single function call
- Allow for any and all further customization with regular Matplotlib if needed

As a result, MPL Plotter is built with Matplotlib compatibility in mind: its capabilities expand when used in combination. Keep reading to see them in action!

---

There's three ways to use MPL Plotter:
- Calls to the 2D and 3D plotting classes. 
- Using presets, either those shipped with the library, or custom ones. 
- Calling the "decorator" `custom_canvas` class. This class won't plot anything, but rather allow you to create a customized canvas on which to plot using Matplotlib.
    
The first will be covered in Sections 4 and 5, from basic usage to in depth customization. The base output and API stability of all base methods can be seen in Section 6. The latter two, in Section 8.

Say goodbye to hours getting your plots in shape!

![alt text](_demo/gallery/showcase/subplot2grid_demo.png "Putting it all together")

# 2. Install

`pip install mpl_plotter`

All dependencies will be checked for and installed automatically. They can be found in `setup.py` under `install_requires`. 

[ PyPi ](https://pypi.org/project/mpl-plotter/)

_TROUBLESHOOTING: If you're upgrading to the latest version of MPL Plotter, please make sure to check your dependencies are up to date with the repo. To do so, download `requirements.txt` above, activate your virtual environment (if you work with one, otherwise ignore that), and_

`pip install -r requirements.txt`

# 3. Map of the library


This is the map of the library. Mostly for import reference. 

Entries in the map are in order of relevance (and in which they will be discussed).  

- mpl_plotter
    - `two_d`
        - `line`
        - `scatter`
        - `heatmap`
        - `quiver`
        - `streamline`
        - `fill_area`
        - `floating_text`
    - `three_d`
        - `line`
        - `scatter`
        - `surface`
        - `floating_text`
    - `setup`
        - `figure`
        - `custom_canvas`
    - `utilities`
        - `get_available_fonts`
    - presets/
        - `publication`
            - `two_d`
            - `three_d`
        - `precision`
            - `two_d`
            - `three_d`
        - `custom`
            - `two_d`
            - `three_d`
            - `generate_preset_2d`
            - `generate_preset_3d`
        - `panes`
            - `Lines`
                - `n_pane_single`
                - `n_pane_comparison`
        - standard/
            - `publication`
            - `precision`
    - color/
        - `maps`
        - `schemes`

# 4. Capabilities

With a single call, you can generate the following plots:

- 2D
  - Line plots
  - Scatter plots
  - Heatmaps
  - Quiver plots
  - Streamline plots
  - Area fills
  - Floating text
- 3D
  - Line plots
  - Scatter plots
  - Surface plots
  - Floating text

Furthermore, MPL Plotter also allows to:

- Use a `custom_canvas` function to define a cusomized figure and axis on which to draw using Matplotlib
- Generate, customize and use 2D and 3D presets in one or many function calls
- Use the pre-made `publication` and `precision` presets to immediately obtain valuable plots
- Easily create custom linear segmented colormaps, so you can use any sequence of colors you fancy
- Custom colorschemes (currently only 1, as it's enough to fit my needs, perhaps more in the future)

---

#### Each plot has specific parameters which can be modified, plus general ones which apply for all 2D and 3D plots respectively. The specific parameters for each plotting class are available in the **docstrings** of their `__init__` methods. It's comfortable to access them from the interactive Python terminal. Eg:

    >>> from mpl_plotter.two_d import line
    >>> help(line)

In Section 11 at the end of this README, all general parameters for 2D and 3D plots can be seen.

# 5. Getting started

In this section we'll go from the the most basic line plot to a fairly customized version in 2D, and similarly for 3D. The line demo scripts can be found in `_demo/scripts/line_demos/`. 

The MPL Plotter workflow is simple by design: the walkthrough below is sufficient to acquaint you with all functionality, for line plots as well as all others. 

The base output of all available 2D and 3D plot follow in Section 6. By then, you will be able to pick anyone up and do your thing.

## `5.1 2D Lines`

As follows from the map above, the import to use the 2D `line` class is:

    from mpl_plotter.two_d import line

And the following is the most basic MPL Plotter call, which will generate the image below (no input, and sin wave respectively).
    
| `line(show=True)` | `x = np.linspace(0, 2*np.pi, 100)`<br>`y = np.sin(x)`<br>`line(x=x, y=y, show=True)` |
| --- | :--- |
| ![alt text](_demo/gallery/2d/basic_line.png "Base output") | ![alt text](_demo/gallery/2d/line_input.png "sin wave") 

Two important features are apparent:
1. MPL Plotter provides mock plots for every plotting class, so you can get straight into action and see what each does
2. MPL Plotter is somewhat "opinionated" and sets up quite a few parameters by default. This is based purely on my preference. You may not agree and you're more than welcome to play around with them!

---

Two more examples (result in the table below):

1. We can add some customization to make our line look a bit better:

        line(show=True, demo_pad_plot=True, spines_removed=None)

    Our line has now some margins to breathe while the ticks are placed at the maximum and minimums of our curve, and no spines are removed.

2. Lastly, an example using some of the parameters you can change:

        line(norm=True, line_width=4,
             aspect=1,
             show=True, demo_pad_plot=True,
             x_label="x", x_label_size=30, x_label_pad=-0.05,
             y_label="$\Psi$", y_label_size=30, y_label_rotation=0, y_label_pad=20,
             title="Custom Line", title_font="Pump Triline", title_size=40, title_color="orange",
             tick_color="darkgrey", workspace_color="darkred", tick_ndecimals=4,
             x_tick_number=12, y_tick_number=12,
             x_tick_rotation=35,
             color_bar=True, cb_tick_number=5, cb_pad=0.05,
             grid=True, grid_color="grey")

| 1. Somewhat customized | 2. Customization example |
| --- | --- |
| ![alt text](_demo/gallery/2d/medium_line.png "Some customization") | ![alt text](_demo/gallery/2d/custom_line.png "Showcase") |

---

## `5.2 3D Lines`

Much of the same follows for 3D plots. In this case however customization is somewhat more limited. This is due to the fact that 1. 3D plots are less useful in general (in my experience, and thus I've spent less time on them) 2. Matplotlib support for 3D plots is more limited

|Basic|Somewhat customized|Customization example|
|---|---|---|
|![alt text](_demo/gallery/3d/basic_line.png "Basic")|![alt text](_demo/gallery/3d/medium_line.png "Some customization")|![alt text](_demo/gallery/3d/custom_line.png "Showcase")|

# 6. Base methods: examples, status

Below can be seen the base output of all methods, their input variables, and an indication of how stable each method is. In `tests/test_minimal`, base calls (no arguments besides `show=True`) for all methods are available. For real-world reference, `tests/tests_2D` and `tests/tests_3D` contain an example using various parameters for every single method.

For method-specific customization options (say, the `line_width` or `point_size` attributes for lines and scatter plots respectively), please check each method's [ docstring ](#each-plot-has-specific-parameters-which-can-be-modified-plus-general-ones-which-apply-for-all-2d-and-3d-plots-respectively-the-specific-parameters-for-each-plotting-class-are-available-in-the-docstrings-of-their-__init__-methods-its-comfortable-to-access-them-from-the-interactive-python-terminal-eg).

## `6.1 2D`

All plots generated in `tests/test_minimal.py`.

| Method | Status | Input |Base output |
| --- | --- | --- | --- |
| `line` | Stable | `x`, `y` | ![alt text](_demo/gallery/2d/basic_line.png "line(show=True)") |
| `scatter` | Stable | `x`, `y` | ![alt text](_demo/gallery/2d/scatter.png "scatter(show=True)") |
| `heatmap` | Stable | `x`, `y`, `z`| ![alt text](_demo/gallery/2d/heatmap.png "heatmap(show=True)") |
| `quiver` | Stable | `x`, `y`, `u`, `v` | ![alt text](_demo/gallery/2d/quiver.png "quiver(show=True)") |
| `streamline` | Stable | `x`, `y`, `u`, `v` | ![alt text](_demo/gallery/2d/streamline.png "streamline(show=True)") |
| `fill` | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/2d/fill.png "fill_area(show=True)") |

## `6.2 3D`

Once more, all plots generated in `tests/test_minimal.py`. Wireframe is included: note it's not a method per se, but a setting of `surface` (hover over the image to see it). 

| Method | Status | Input |Base output | 
| --- | --- | --- | --- |
| `line` | Stable | `x`, `y`, `z`| ![alt text](_demo/gallery/3d/line.png "line(show=True)") |
| `scatter` | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/3d/scatter.png "scatter(show=True)") |
| `surface` | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/3d/surface.png "surface(show=True)") |
| Wireframe | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/3d/wireframe.png "surface(show=True, alpha=0, line_width>0)") |

## `6.3 Plot combination examples`

|  |
| --- |
| ![alt text](_demo/gallery/2d/load_characteristic.png "Combination of lines, fills, plus Matplotlib tinkering (eg: extra axis)") |

# 7. Matplotlib compatibility
## `7.1 Retrieving axes, figures`

The axis and figure on which each class draws are instance attributes. To retrieve them and continue modifications using standard Matplotlib:
    
    from mpl_plotter.two_d import line
    
    my_plot = line()
    ax, fig = my_plot.ax, my_plot.fig
    
With the axis and figure, most Matplotlib functions out there can be used to further modify your plots. 

## `7.2 Using Matplotlib's axis tiling`

Matplotlib allows for subplot composition using `subplot2grid`. This can be used in combination with MPL Plotter:

Importantly:
- The auxiliary function `figure` (`from mpl_plotter.setup import figure`) sets up a figure in a chosen backend. This is convenient, as if the figure is created with `plt.figure()`, only the default non-interactive Matplotlib backend will be available, unless `matplotlib.use(<backend>)` is specified before importing `pyplot`.

        backend = "Qt5Agg"  # None -> regular non-interactive matplotlib output
        
        fig = figure(figsize=(10, 10), backend=backend)
        
        ax0 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, aspect=1, fig=fig)
        ax1 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, aspect=1, fig=fig)
        ax2 = plt.subplot2grid((2, 2), (0, 1), rowspan=1, aspect=1, fig=fig)
        ax3 = plt.subplot2grid((2, 2), (1, 1), rowspan=1, aspect=12, fig=fig)
        
        axes = [ax0, ax1, ax2, ax3]
        plots = [line, quiver, streamline, fill_area]
        
        for i in range(len(plots)):
            plots[i](fig=fig, ax=axes[i],
                     backend=backend
                     )
        
        plt.show()
        
![alt text](_demo/gallery/2d/grid.png "Grid sample")       
 
# 8. Advanced plotting: Presets and `custom_canvas`

The following are alternative ways to use MPL Plotter. Presets are currently implemented for the 2D and 3D **line** and **scatter** plot classes. More might be implemented in the future. 

## `8.1 Custom presets`
Presets enable you to create plots without barely writing any code. An example workflow follows.

1. Use a preset creation function (`generate_preset_2d` or `generate_preset_3d`) to create a preset
    
        from mpl_plotter.presets.custom import generate_preset_2d
        
        generate_preset_2d(preset_dest="presets", preset_name="MYPRESET", disable_warning=True, overwrite=True)

   A `MYPRESET.py` file will be created in a new (or not) `presets/` directory within your project's root directory.
   
    - If no `preset_dest` is provided, `MYPRESET.py` will be saved in your root directory.
    - If no `preset_name` is provided, the preset will be saved as `preset_2d.py`.
    - By setting `disable_warning=True`, console output reminding you of the risk of rewriting your preset will be suppressed.
    - By setting `overwrite=True`, every time your run the preset creation function, it will overwrite the previously created preset with the same name (rather inconvenient, but who knows when it can come in handy).

   This file has a `preset` dictionary inside, with all editable parameters inside it, and commented out. Eg:
    
        preset = { 
            ## Basic 
            # "plot_label": None, 
            ## Backend 
            # "backend": "Qt5Agg", 
            ## Fonts 
            # "font": "serif",
            ...
        }

   By uncommenting certain lines, those parameters will be read and used to shape your plots.

2. Modify `MYPRESET.py` according to your needs.

3. Import `mpl_plotter.presets.custom.two_d` (or `three_d` if working with a 3D preset) and initiate it with `MYPRESET`
    
        from mpl_plotter.presets.custom import two_d
        
        my_preset_plot_family = two_d(preset_dir="presets", preset_name="MYPRESET")
        
        my_preset_line = my_plot_family.line
        
        # You can create further plotting classes spawning from my_preset_plot_family:
        # Eg        --->        my_preset_scatter = my_plot_family.scatter
    
4. Call a plotting function child of `two_d`, setting any extra parameters appropriately (plot title, etc.)

        my_preset_line(show=True, demo_pad_plot=True, color="blue", title="TITLE", title_size=200, aspect=1)

    The result of this example plus the 3D version and those for all other available plots can be seen in the table below.
    
    | | | | | | | |
    | --- | --- | --- | --- | --- | --- | --- |
    | 2D | ![alt text](_demo/gallery/2d/preset_line.png "2D custom preset") | ![alt text](_demo/gallery/2d/preset_scatter.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_heatmap.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_quiver.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_streamline.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_fill.png "2D custom preset")|
    | 3D | ![alt text](_demo/gallery/3d/preset_line.png "3D custom preset") | ![alt text](_demo/gallery/3d/preset_scatter.png "2D custom preset") | ![alt text](_demo/gallery/3d/preset_surface.png "2D custom preset") | ![alt text](_demo/gallery/3d/preset_surface_color.png "2D custom preset") | ![alt text](_demo/gallery/3d/preset_surface_lighting1.png "2D custom preset") |

    
    
5. Make as many plots as you need. Tiling is supported as well (see `panes` in Section 9)

## `8.2 Standard presets`

Standard presets are available to remove overhead. They're tailored for my needs and desires, but perhaps you find them useful too.

### _Publication_
It is a common mistake to make a figure for a paper with unreadable labels. This preset tries to solve that, generating plots optimized to be printed on a small format, in side-by-side plots or embedded in a column of text.

    from mpl_plotter.presets.precision import two_d
    from mpl_plotter.color.schemes import one           # Custom colorscheme

    x = np.linspace(0, 4, 1000)
    y = np.exp(x)
    z = abs(np.sin(x)*np.exp(x))
    
    two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)

### _Precision_

Made to plot functions large on the screen, with equal x and y scales to avoid skewing the variables, and many ticks to visually inspect a signal.

    from mpl_plotter.presets.precision import two_d
    
    two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)

| _Publication_ | _Precision_ |
| --- | --- |
| ![alt text](_demo/gallery/2d/preset_publication_line.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_line.png "Precision preset") |

And below, all remaining plots (_publication_ preset above, _precision_ below):

| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ![alt text](_demo/gallery/2d/preset_publication_scatter.png "Precision preset")| ![alt text](_demo/gallery/2d/preset_publication_heatmap.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_publication_quiver.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_publication_streamline.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_publication_fill.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_publication_line.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_publication_scatter.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_publication_surface.png "Precision preset") | 
| ![alt text](_demo/gallery/2d/preset_precision_scatter.png "Precision preset")| ![alt text](_demo/gallery/2d/preset_precision_heatmap.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_quiver.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_streamline.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_fill.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_precision_line.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_precision_scatter.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_precision_surface.png "Precision preset") | 

## `8.3 custom_canvas`

Lastly, MPL Plotter can be used to create a "custom canvas" on which to draw with Matplotlib.
    - `custom_canvas` creates a figure and **1**. By retrieving the figure, more axes may be created. 
    - If you wish `custom_canvas` to **resize your axes**, it must be given the `x` and `y` of (one) of your plots

_NOTE: functionality might not be at 100% yet when using `custom_canvas`+Matplotlib as compared to plotting with MPL Plotter directly._

    from mpl_plotter.setup import custom_canvas
    
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    
    c = custom_canvas(x=x, y=y, spines_removed=None, font_color="darkred")  # x and y provided: axes are resized
    ax, fig = c.ax, c.fig
    
    # Regular Matplotlib stuff
    
    plt.plot(x, y)
    
    plt.show()
    
![alt text](_demo/gallery/2d/custom_canvas.png "Custom canvas sample")

# 9. Unstable functionality: `panes`

_Disclaimer: The following are utilities which combine presets and axis tiling to create `n`-pane plots. 
The API is very volatile, and flexibility must be improved.
In any case, I find them practical from time to time, perhaps you too._

MPL Plotter includes a `panes` package for line plots, via the `Lines` class.
The method "map" is as follows:

- `mpl_plotter`
    - `panes`
        - `Lines`
            - `n_pane_single`
            - `n_pane_comparison`
 
## `9.1 n_pane_single`
 
 This function takes in a number `n` of curves, and generates an `n`-pane panel plot with them.
 
     Lines(preset=preset).n_pane_single(x,                   # Horizontal vector
                                        [u, v, y],           # List of curves to be plotted
                                        ["u", "v", "y"],     # List of vertical axis labels
                                        ["a", "b", "c"]      # List of legend labels 
                                        )  
 ![alt text](_demo/gallery/2d/pane_single.png "Grid sample")
  
## `9.2 n_pane_comparison`
 
 In turn, this function takes in a number `n` of **lists** of `m` curves (where `m`=2 in the example below), to be plotted in the same pane for comparison.
 
    Lines(preset=preset).n_pane_comparison(x,                               # Horizontal vector
                                           [[u, uu], [v, vv], [y, yy]],     # List of pairs of curves to be compared
                                           ["u", "v", "y"],                 # List of vertical axis labels
                                           ["a", "b"]                       # List of legend labels
                                           )
                                       
![alt text](_demo/gallery/2d/pane_comparison.png "Grid sample")

## `9.3 Bunch of panes`

Cause why would you believe me otherwise.

![alt text](_demo/gallery/2d/pane_alot.png "There's a lot")

And same for the `n` `m`-curve comparisons.

![alt text](_demo/gallery/2d/pane_alot_comparison.png "There's a lot of lists of 3 curves")

# 10. Contributing

There's much to be done yet. Feature suggestions or bug finds are welcome! 

## Backlog

### `Bugs`
- 2D
    - Combination with python-control plots
        - Axis limits not working
- 3D
    - z label rotation not working

### `Documentation`
- Color
- More examples
- Description of all parameters
- readthedocs?

### `Functionality`
- 2D
    - Presets
        - Math - eg:
            ![image](https://user-images.githubusercontent.com/47611105/117718931-139ee000-b1dd-11eb-9f13-cb09c5e6d923.png)
    - New plots
        - Financial
            - Bar charts
- 3D
    - New plots
        - tricontour
        - projections

# 11. All modifiable parameters

`2D`
---
| Parameter            | Default | Description  |
| ---------     | ----| -----:| 
| backend | Qt5Agg | - |
| font | serif | - |
| math_font | dejavuserif | - |
| font_color | black | - |
| font_size_increase |  0 | - |
| fig | None | - |
| ax | None | - |
| figsize | (6, 6) | - |
| shape_and_position | 111 | - |
| prune | None | - |
| resize_axes | True | - |
| aspect | None | - |
| workspace_color | None | - |
| workspace_color2 | None | - |
| background_color_figure | white | - |
| background_color_plot | white | - |
| background_alpha | 1 | - |
| style | None | - |
| light | None | - |
| dark | None | - |
| spine_color | None | - |
| spines_removed | (0, 0, 1, 1) | - |
| x_upper_bound | None | - |
| x_lower_bound | None | - |
| y_upper_bound | None | - |
| y_lower_bound | None | - |
| x_bounds | None | - |
| y_bounds | None | - |
| demo_pad_plot | True | - |
| x_upper_resize_pad | 0 | - |
| x_lower_resize_pad | 0 | - |
| y_upper_resize_pad | 0 | - |
| y_lower_resize_pad | 0 | - |
| grid | True | - |
| grid_color | lightgrey | - |
| grid_lines | -. | - |
| color | darkred | - |
| cmap | RdBu_r | - |
| alpha | None | - |
| norm | None | - |
| title | None | - |
| title_size | 12 | - |
| title_y | 1.025 | - |
| title_weight | None | - |
| title_font | None | - |
| title_color | None | - |
| x_label | None | - |
| x_label_size | 20 | - |
| x_label_pad | 10 | - |
| x_label_rotation | None | - |
| x_label_weight | None | - |
| y_label | None | - |
| y_label_size | 20 | - |
| y_label_pad | 10 | - |
| y_label_rotation | None | - |
| y_label_weight | None | - |
| x_tick_number | 3 | - |
| x_tick_labels | None | - |
| y_tick_number | 3 | - |
| y_tick_labels | None | - |
| x_label_coords | None | - |
| y_label_coords | None | - |
| tick_color | None | - |
| tick_label_pad | 5 | - |
| ticks_where | (1, 1, 0, 0) | - |
| tick_label_size | None | - |
| x_tick_label_size | 15 | - |
| y_tick_label_size | 15 | - |
| x_custom_tick_locations | None | - |
| y_custom_tick_locations | None | - |
| fine_tick_locations | True | - |
| x_custom_tick_labels | None | - |
| y_custom_tick_labels | None | - |
| x_date_tick_labels | False | - |
| date_format | %Y-%m-%d | - |
| tick_ndecimals | 1 | - |
| x_tick_ndecimals | None | - |
| y_tick_ndecimals | 3 | - |
| x_tick_rotation | None | - |
| y_tick_rotation | None | - |
| tick_labels_where | (1, 1, 0, 0) | - |
| color_bar | False | - |
| cb_pad | 0.2 | - |
| cb_axis_labelpad | 10 | - |
| shrink | 0.75 | - |
| extend | neither | - |
| cb_title | None | - |
| cb_orientation | vertical | - |
| cb_title_rotation | None | - |
| cb_title_style | normal | - |
| cb_title_size | 10 | - |
| cb_top_title_y | 1 | - |
| cb_ytitle_labelpad | 10 | - |
| cb_title_weight | normal | - |
| cb_top_title | False | - |
| cb_y_title | False | - |
| cb_top_title_pad | None | - |
| x_cb_top_title | 0 | - |
| cb_vmin | None | - |
| cb_vmax | None | - |
| cb_hard_bounds | False | - |
| cb_outline_width | None | - |
| cb_tick_number | 5 | - |
| cb_ticklabelsize | 10 | - |
| tick_ndecimals_cb | None | - |
| plot_label | None | - |
| legend | False | - |
| legend_loc | upper right | - |
| legend_bbox_to_anchor | None | - |
| legend_size | 15 | - |
| legend_weight | normal | - |
| legend_style | normal | - |
| legend_handleheight | None | - |
| legend_ncol | 1 | - |
| show | False | - |
| zorder | None | - |
| filename | None | - |
| dpi | None | - |
| suppress | True | - |

`3D`
---
| Parameter            | Default  |  Description |
| :---------     | -------- | -----:|
| x_scale |  1 | - |
| y_scale |  1 | - |
| z_scale |  1 | - |
| backend |  Qt5Agg | - |
| font |  serif | - |
| math_font |  dejavuserif | - |
| font_color |  black | - |
| font_size_increase |  0 | - |
| fig |  None | - |
| ax |  None | - |
| figsize |  None | - |
| shape_and_position |  111 | - |
| azim |  -137 | - |
| elev |  26 | - |
| prune |  None | - |
| resize_axes |  True | - |
| aspect |  1 | - |
| box_to_plot_pad |  10 | - |
| spines_juggled |  (1,0,2) | - |
| spine_color |  None | - |
| blend_edges |  False | - |
| workspace_color |  None | - |
| workspace_color2 |  None | - |
| background_color_figure |  white | - |
| background_color_plot |  white | - |
| background_alpha |  1 | - |
| style |  None | - |
| light |  None | - |
| dark |  None | - |
| pane_fill |  None | - |
| x_upper_bound |  None | - |
| x_lower_bound |  None | - |
| y_upper_bound |  None | - |
| y_lower_bound |  None | - |
| z_upper_bound |  None | - |
| z_lower_bound |  None | - |
| x_bounds |  None | - |
| y_bounds |  None | - |
| z_bounds |  None | - |
| demo_pad_plot |  False | - |
| x_upper_resize_pad |  0 | - |
| x_lower_resize_pad |  0 | - |
| y_upper_resize_pad |  0 | - |
| y_lower_resize_pad |  0 | - |
| z_upper_resize_pad |  0 | - |
| z_lower_resize_pad |  0 | - |
| show_axes |  True | - |
| grid |  True | - |
| grid_color |  lightgrey | - |
| grid_lines |  -. | - |
| color |  darkred | - |
| cmap |  RdBu_r | - |
| alpha |  1 | - |
| title |  None | - |
| title_weight |  normal | - |
| title_size |  12 | - |
| title_y |  1.025 | - |
| title_color |  None | - |
| title_font |  None | - |
| x_label |  x | - |
| x_label_weight |  normal | - |
| x_label_size |  12 | - |
| x_label_pad |  7 | - |
| x_label_rotation |  None | - |
| y_label |  y | - |
| y_label_weight |  normal | - |
| y_label_size |  12 | - |
| y_label_pad |  7 | - |
| y_label_rotation |  None | - |
| z_label |  z | - |
| z_label_weight |  normal | - |
| z_label_size |  12 | - |
| z_label_pad |  7 | - |
| z_label_rotation |  None | - |
| x_tick_number |  5 | - |
| x_tick_labels |  None | - |
| x_custom_tick_labels |  None | - |
| x_custom_tick_locations |  None | - |
| y_tick_number |  5 | - |
| y_tick_labels |  None | - |
| y_custom_tick_labels |  None | - |
| y_custom_tick_locations |  None | - |
| z_tick_number |  5 | - |
| z_tick_labels |  None | - |
| z_custom_tick_labels |  None | - |
| z_custom_tick_locations |  None | - |
| x_tick_rotation |  None | - |
| y_tick_rotation |  None | - |
| z_tick_rotation |  None | - |
| tick_color |  None | - |
| tick_label_pad |  4 | - |
| tick_ndecimals |  1 | - |
| tick_label_size |  8.5 | - |
| x_tick_label_size |  None | - |
| y_tick_label_size |  None | - |
| z_tick_label_size |  None | - |
| color_bar |  False | - |
| extend |  neither | - |
| shrink |  0.75 | - |
| cb_title |  None | - |
| cb_axis_labelpad |  10 | - |
| cb_tick_number |  5 | - |
| cb_outline_width |  None | - |
| cb_title_rotation |  None | - |
| cb_title_style |  normal | - |
| cb_title_size |  10 | - |
| cb_top_title_y |  1 | - |
| cb_ytitle_labelpad |  10 | - |
| cb_title_weight |  normal | - |
| cb_top_title |  False | - |
| cb_y_title |  False | - |
| cb_top_title_pad |  None | - |
| x_cb_top_title |  0 | - |
| cb_vmin |  None | - |
| cb_vmax |  None | - |
| cb_ticklabelsize |  10 | - |
| plot_label |  None | - |
| legend |  False | - |
| legend_loc |  upper right | - |
| legend_size |  13 | - |
| legend_weight |  normal | - |
| legend_style |  normal | - |
| legend_handleheight |  None | - |
| legend_ncol |  1 | - |
| show |  False | - |
| newplot |  False | - |
| filename |  None | - |
| dpi |  None | - |
| suppress |  True | - |
