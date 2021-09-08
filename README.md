# MPL Plotter 

![alt text](tests/coverage/coverage.svg ".coverage available in tests/coverage/")

<div style="text-align:center"><img align="right" width="135" height="135" src="_demo/gallery/showcase/logo.png" /></div>

MPL Plotter is a Matplotlib based Python plotting library built with the goal of achieving publication-quality plots 
in an efficient and comprehensive way. What follows is a user's manual of MPL Plotter. 
[The full Python API documentation is available here](https://mpl-plotter-docs.github.io/).

### Table of Contents

[ **1. Introduction** ](#1-introduction)

[ **2. Install**  ](#2-install)

[ **3. Map of the library** ](#3-map-of-the-library)

[ **4. Capabilities** ](#4-capabilities)

[ **5. Getting started** ](#5-getting-started)

[ _5.1 2D Lines_ ](#51-2d-lines)

[ _5.2 3D Lines_ ](#52-3d-lines)    

[ **6. Base methods: examples, status** ](#6-base-methods-examples-status)

[ _6.1 2D_ ](#61-2d)

[ _6.2 3D_ ](#62-3d)

[ _6.3 Plot combination examples_ ](#63-plot-combination-examples)

[ **7. Matplotlib compatibility** ](#7-matplotlib-compatibility)

[ _7.1 Retrieving axes, figures_ ](#71-retrieving-axes-figures)

[ _7.2 Using Matplotlib's axis tiling_ ](#72-using-matplotlibs-axis-tiling)

[ **8. Advanced: Presets and `custom_canvas`** ](#8-advanced-presets-and-custom_canvas)

[ _8.1 Custom presets_ ](#81-custom-presets)

[ _8.2 Standard presets_ ](#82-standard-presets)

[ _8.3_ `custom_canvas` ](#83-custom_canvas)

[ **9. Advanced: `comparison` and `panes`** ](#9-advanced-comparison-and-panes)

[ _9.1_ `comparison` ](#91-comparison)

[ _9.2_ `pane` ](#92-n_pane_single)

[ _9.4 Bunch of panes_ ](#94-bunch-of-panes)

# 1. Introduction 

Making plots for technical documents can be a time sink. At some point I decided I might as well rid myself of that overhead, and this is the result! It does the job for me and I expand it when it can't. It's somwehat opinionated, but it may still do the trick! 

Hope you find some use in it :)

---

The fundamental premise of MPL Plotter is to:
- Generate publication quality plots in a single function call
- Allow for any and all further customization with regular Matplotlib if needed

As a result, MPL Plotter is built with Matplotlib compatibility in mind: its capabilities expand 
when used in combination. Keep reading to see them in action!

---

There's three ways to use MPL Plotter:
- Calls to the 2D and 3D plotting classes. 
- Using presets, either those shipped with the library, or custom ones. 
- Calling the "decorator" `custom_canvas` class. This class won't plot anything, but rather allow 
you to create a customized canvas on which to plot using Matplotlib.
    
The first will be covered in Sections 4 and 5, from basic usage to in depth customization. The base 
output and API stability of all base methods can be seen in Section 6. The latter two, in Section 8.

Say goodbye to hours getting your plots in shape!

![alt text](_demo/gallery/showcase/subplot2grid_demo.png "Putting it all together")

# 2. Install

`pip install mpl_plotter`

All dependencies will be checked for and installed automatically. They can be found in `setup.py` 
under `install_requires`. 

[ PyPi ](https://pypi.org/project/mpl-plotter/)

_TROUBLESHOOTING: If you're upgrading to the latest version of MPL Plotter, please make sure to 
check your dependencies are up to date with the repo. To do so, download `requirements.txt` above, activate 
your virtual environment (if you work with one, otherwise ignore that), and_

`pip install -r requirements.txt`

## Linux

PyQt5 may fail to install in Linux, prompting the following error:

    FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pip-build-4d8suz7p/PyQt5/setup.py'
    
To solve this, make sure pip is up to date and install PyQt5 5.14.0. Check this 
[ StackOverflow answer ](https://stackoverflow.com/questions/59711301/install-pyqt5-5-14-1-on-linux) for further reference.

    pip3 install --upgrade pip
    pip3 install pyqt5==5.14.0

# 3. Map of the library

This is the map of the library. Mostly for import reference. 
**Bold**: package; `Code`: methods; Plain/: directories 

- **mpl_plotter**
    - `figure`
    - `get_available_fonts`
    - **two_d**
        - `line`
        - `scatter`
        - `heatmap`
        - `quiver`
        - `streamline`
        - `fill_area`
        - `floating_text`
        - comparison/
            - `comparison`
        - panes/
            - `n_pane_single`
            - `n_pane_comparison`
    - **three_d**
        - `line`
        - `scatter`
        - `surface`
        - `floating_text`
    - **canvas**
        - `custom_canvas`
    - **presets**
        - **publication**
            - `two_d`
            - `three_d`
        - **precision**
            - `two_d`
            - `three_d`
        - **custom**
            - `two_d`
            - `three_d`
            - `generate_preset_2d`
            - `generate_preset_3d`
        - data/
            - `publication`
            - `precision`
    - **color**
        - **schemes**
            - `colorscheme_one`
            - `custom`
        - **functions**
            - `hex_to_rgb`
            - `rgb_to_hex`
            - `complementary`
            - `delta`

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

In this section we'll go from the the most basic line plot to a fairly customized version in 2D, and similarly for 3D. 
The line demo scripts can be found in `_demo/scripts/line_demos/`. 

The MPL Plotter workflow is simple by design: the walkthrough below is sufficient to acquaint you with all functionality, 
for line plots as well as all others. 

The base output of all available 2D and 3D plot follow in Section 6. By then, you will be able to pick anyone up 
and do your thing.

## `5.1 2D Lines`

As follows from the map above, the import to use the 2D `line` class is:

    from mpl_plotter.two_d import line

And the following is the most basic MPL Plotter call, which will generate the image below (no input, and sin wave 
respectively).
    
| `line(show=True)` | `x = np.linspace(0, 2*np.pi, 100)`<br>`y = np.sin(x)`<br>`line(x=x, y=y, show=True)` |
| --- | :--- |
| ![alt text](_demo/gallery/2d/basic_line.png "Base output") | ![alt text](_demo/gallery/2d/line_input.png "sin wave") 

Two important features are apparent:
1. MPL Plotter provides mock plots for every plotting class, so you can get straight into action and see what each does
2. MPL Plotter is somewhat "opinionated" and sets up quite a few parameters by default. This is based purely on my 
preference. You may not agree and you're more than welcome to play around with them!

---

Two more examples (result in the table below):

1. We can add some customization to make our line look a bit better:

        line(show=True, demo_pad_plot=True, spines_removed=None)

    Our line has now some margins to breathe while the ticks are placed at the maximum and minimums of our curve, 
    and no spines are removed.

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

Much of the same follows for 3D plots. In this case however customization is somewhat more limited. 
This is due to the fact that 
1. 3D plots are less useful in general (in my experience, and thus I've spent less time on them) 
2. Matplotlib support for 3D plots is more limited

|Basic|Somewhat customized|Customization example|
|---|---|---|
|![alt text](_demo/gallery/3d/basic_line.png "Basic")|![alt text](_demo/gallery/3d/medium_line.png "Some customization")|![alt text](_demo/gallery/3d/custom_line.png "Showcase")|

# 6. Base methods: examples, status

Below can be seen the base output of all methods, their input variables, and an indication of how stable each method is. 
In `tests/test_minimal`, base calls (no arguments besides `show=True`) for all methods are available. 
For real-world reference, `tests/tests_2D` and `tests/tests_3D` contain an example using various parameters 
for every single method.

For method-specific customization options (say, the `line_width` or `point_size` attributes for lines and 
scatter plots respectively), please check each method's 
[ docstring ](#each-plot-has-specific-parameters-which-can-be-modified-plus-general-ones-which-apply-for-all-2d-and-3d-plots-respectively-the-specific-parameters-for-each-plotting-class-are-available-in-the-docstrings-of-their-__init__-methods-its-comfortable-to-access-them-from-the-interactive-python-terminal-eg).

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

Once more, all plots generated in `tests/test_minimal.py`. Wireframe is included: note it's not a method per se, 
but a setting of `surface` (hover over the image to see it). 

| Method | Status | Input |Base output | 
| --- | --- | --- | --- |
| `line` | Stable | `x`, `y`, `z`| ![alt text](_demo/gallery/3d/line.png "line(show=True)") |
| `scatter` | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/3d/scatter.png "scatter(show=True)") |
| `surface` | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/3d/surface.png "surface(show=True)") |
| Wireframe | Stable | `x`, `y`, `z` | ![alt text](_demo/gallery/3d/wireframe.png "surface(show=True, alpha=0, line_width>0)") |

## `6.3 Plot combination examples`

| ![alt text](_demo/gallery/2d/load_characteristic.png "Combination of lines, fills, plus Matplotlib tinkering (eg: extra axis)") |
| --- |


# 7. Matplotlib compatibility
## `7.1 Retrieving axes, figures`

The axis and figure on which each class draws are instance attributes. To retrieve them and continue modifications 
using standard Matplotlib:
    
    from mpl_plotter.two_d import line
    
    my_plot = line()
    ax, fig = my_plot.ax, my_plot.fig
    
With the axis and figure, most Matplotlib functions out there can be used to further modify your plots. 

## `7.2 Using Matplotlib's axis tiling`

Matplotlib allows for subplot composition using `subplot2grid`. This can be used in combination with MPL Plotter:

Importantly:
- The auxiliary function `figure` (`from mpl_plotter.setup import figure`) sets up a figure in a chosen backend. 
This is convenient, as if the figure is created with `plt.figure()`, only the default non-interactive Matplotlib 
backend will be available, unless `matplotlib.use(<backend>)` is specified before importing `pyplot`.

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
 
# 8. Advanced: Presets and `custom_canvas`

The following are alternative ways to use MPL Plotter. Presets are currently implemented for the 2D and 3D 
**line** and **scatter** plot classes. More might be implemented in the future. 

## `8.1 Custom presets`
Presets enable you to create plots without barely writing any code. An example workflow follows.

1. Use a preset creation function (`generate_preset_2d` or `generate_preset_3d`) to create a preset
    
        from mpl_plotter.presets.custom import generate_preset_2d
        
        generate_preset_2d(preset_dest="presets", preset_name="MYPRESET", disable_warning=True, overwrite=True)

   A `MYPRESET.py` file will be created in a new (or not) `presets/` directory within your project's root directory.
   
    - If no `preset_dest` is provided, `MYPRESET.py` will be saved in your root directory.
    - If no `preset_name` is provided, the preset will be saved as `preset_2d.py`.
    - By setting `disable_warning=True`, console output reminding you of the risk of rewriting your preset will be suppressed.
    - By setting `overwrite=True`, every time your run the preset creation function, it will overwrite the previously 
    created preset with the same name (rather inconvenient, but who knows when it can come in handy).

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

    The result of this example, its 3D version, and demos for all other available 2D and 3D plots can be seen in the 
    table below.
    
    | 2D | ![alt text](_demo/gallery/2d/preset_line.png "2D custom preset") | ![alt text](_demo/gallery/2d/preset_scatter.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_heatmap.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_quiver.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_streamline.png "2D custom preset")| ![alt text](_demo/gallery/2d/preset_fill.png "2D custom preset")|
    | --- | --- | --- | --- | --- | --- | --- |
    | **3D** | ![alt text](_demo/gallery/3d/preset_line.png "3D custom preset") | ![alt text](_demo/gallery/3d/preset_scatter.png "3D custom preset") | ![alt text](_demo/gallery/3d/preset_surface.png "3D custom preset") | ![alt text](_demo/gallery/3d/preset_surface_color.png "3D custom preset") | ![alt text](_demo/gallery/3d/preset_surface_lighting1.png "3D custom preset") |

    
    
5. Make as many plots as you need. Tiling is supported as well (see `panes` in Section 9)

## `8.2 Standard presets`

Standard presets are available to remove overhead. They're tailored for my needs and desires, but perhaps you find 
them useful too.

### _Publication_
It is a common mistake to make a figure for a paper with unreadable labels. This preset tries to solve that, 
generating plots optimized to be printed on a small format, in side-by-side plots or embedded in a column of text.

    from mpl_plotter.presets.precision import two_d
    from mpl_plotter.color.schemes import one           # Custom colorscheme

    x = np.linspace(0, 4, 1000)
    y = np.exp(x)
    z = abs(np.sin(x)*np.exp(x))
    
    two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)

### _Precision_

Made to plot functions large on the screen, with equal x and y scales to avoid skewing the variables, and 
many ticks to visually inspect a signal.

    from mpl_plotter.presets.precision import two_d
    
    two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)

| _Publication_ | _Precision_ |
| --- | --- |
| ![alt text](_demo/gallery/2d/preset_publication_line.png "Publication preset") | ![alt text](_demo/gallery/2d/preset_precision_line.png "Precision preset") |

And below, all remaining plots (_publication_ preset above, _precision_ below):

| ![alt text](_demo/gallery/2d/preset_publication_scatter.png "Publication preset")| ![alt text](_demo/gallery/2d/preset_publication_heatmap.png "Publication preset") | ![alt text](_demo/gallery/2d/preset_publication_quiver.png "Publication preset") | ![alt text](_demo/gallery/2d/preset_publication_streamline.png "Publication preset") | ![alt text](_demo/gallery/2d/preset_publication_fill.png "Publication preset") | ![alt text](_demo/gallery/3d/preset_publication_line.png "Publication preset") | ![alt text](_demo/gallery/3d/preset_publication_scatter.png "Publication preset") | ![alt text](_demo/gallery/3d/preset_publication_surface.png "Publication preset") |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ![alt text](_demo/gallery/2d/preset_precision_scatter.png "Precision preset")| ![alt text](_demo/gallery/2d/preset_precision_heatmap.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_quiver.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_streamline.png "Precision preset") | ![alt text](_demo/gallery/2d/preset_precision_fill.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_precision_line.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_precision_scatter.png "Precision preset") | ![alt text](_demo/gallery/3d/preset_precision_surface.png "Precision preset") | 

## `8.3 custom_canvas`

Lastly, MPL Plotter can be used to create a "custom canvas" on which to draw with Matplotlib.
    - `custom_canvas` creates a figure and **1**. By retrieving the figure, more axes may be created. 
    - If you wish `custom_canvas` to **resize your axes**, it must be given the `x` and `y` of (one) of your plots

_NOTE: functionality might not be at 100% yet when using `custom_canvas`+Matplotlib as compared to plotting with 
MPL Plotter directly._

    from mpl_plotter.setup import custom_canvas
    
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    
    c = custom_canvas(x=x, y=y, spines_removed=None, font_color="darkred")  # x and y provided: axes are resized
    ax, fig = c.ax, c.fig
    
    # Regular Matplotlib stuff
    
    plt.plot(x, y)
    
    plt.show()

| ![alt text](_demo/gallery/2d/custom_canvas.png "2D custom canvas example") | ![alt text](_demo/gallery/3d/custom_canvas.png "3D custom canvas example") |
| --- | --- |


# 9. Advanced: `comparison` and `panes`

Module map for reference.

- `mpl_plotter`
    - `two_d`
        - `comparison`
        - `panes`

            
## `9.1 comparison`

The `comparison` function facilitates including any number of curves in a single plot. The 
axis limits will be automatically set so no data lies outside.

    Lines().comparison([x, x, x],
                       [u, v, w],
                       plot_labels=["sin", "cos", "tan"],
                       x_custom_tick_labels=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                       show=show,
                       )
![alt text](_demo/gallery/2d/comparison.png "Curve comparison")

A plotting function of choice can be specified for each of the arrays to be plotted. This
is especially useful to easily combine lines with scatter plots, among other uses.
Below you can see an example in which:
1. Three plotting functions are defined making use of the MPL Plotter `line` and `scatter` 
plotting classes.
2. The plotting functions are input in a list in the `comparison` call

    
        from mpl_plotter.two_d import comparison, line, scatter
        
        
        def f(x, y, **kwargs):
            line(x, y,
                 line_width=2,
                 **kwargs)
        def g(x, y, **kwargs):
            scatter(x, y,
                    marker="D",
                    point_size=10,
                    **kwargs)
        def h(x, y, **kwargs):
            scatter(x, y,
                    marker="s",
                    point_size=5,
                    **kwargs)

        comparison([x, x, x],
                   [u, v, w],
                   [f, g, h],
                   plot_labels=["sin", "cos", "tan"],
                   zorders=[1, 2, 3],
                   colors=['C1', 'C2', 'C3'],
                   alphas=[0.5, 0.5, 1],
                   x_custom_tick_labels=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend
                   )
![alt text](_demo/gallery/2d/comparison_custom.png "Curve comparison")
 
## `9.2 panes`
 
The panes function allows for the plotting of a series of graphs in side-by-side panes.
It can take a number `n` of curves and generate an `n`-pane panel plot with them,
     
         panes(x,                   # Horizontal vector
               [u, v, y],           # List of curves to be plotted
               ["u", "v", "y"],     # List of vertical axis labels
               ["a", "b", "c"]      # List of legend labels 
               )  
 ![alt text](_demo/gallery/2d/pane_single.png "Single-curve panes")
 
As well as take a number `n` of **lists** of `m` curves (where `m`=2 in the example below), 
to be plotted in the same pane for comparison.
 
        panes(x,                               # Horizontal vector
              [[u, uu], [v, vv], [y, yy]],     # List of pairs of curves to be compared
              ["u", "v", "y"],                 # List of vertical axis labels
              ["a", "b"]                       # List of legend labels
              )
![alt text](_demo/gallery/2d/pane_comparison.png "Multiple-curve comparison panes")


## `9.3 Bunch of panes`

Cause why not.

![alt text](_demo/gallery/2d/pane_alot.png "There's a lot")

And same goes for _n_ panes with a number _m_ of curves in each!

![alt text](_demo/gallery/2d/pane_alot_comparison.png "There's a lot of lists of 3 curves")


