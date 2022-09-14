# MPL Plotter 

![.coverage available in tests/coverage/](tests/coverage/coverage.svg) [![Monthly downloads](https://pepy.tech/badge/mpl-plotter/month)](https://pepy.tech/project/mpl_plotter)

MPL Plotter is a Python plotting library built on top of Matplotlib with the goal of delivering publication-quality plots 
concisely. [The full API documentation is available here](https://mpl-plotter-docs.github.io/). Read on to get started.

[![Putting it all together.](demo/gallery/showcase/demo.png)](https://github.com/alopezrivera/mpl_plotter/blob/master/demo/scripts/demo.py)

### Table of Contents

[ **1. Introduction** ](#1-introduction)

[ **2. Install**  ](#2-install)

[ **3. Map of the library** ](#3-map-of-the-library)

[ **4. Getting started** ](#4-getting-started)

[ 4.1 2D ](#41-2d)

[ 4.2 3D ](#42-3d)    

[ **5. Comparisons and side by side plots** ](#5-curve-comparisons-and-multiple-pane-plots)

[ _5.1_ `comparison` ](#51-comparison)

[ _5.2_ `panes` ](#52-panes)

[ **6. Presets** ](#6-presets)

[ 6.1 Standard presets ](#61-standard-presets)

[ 6.2 Custom presets ](#62-custom-presets)

[ **7. Matplotlib** ](#7-matplotlib)

[ 7.1 Retrieving axes, figures ](#71-retrieving-axes-figures)

[ 7.2 Using Matplotlib's axis tiling ](#72-using-matplotlibs-axis-tiling)

# 1. Introduction 

Making plots for technical documents can be a time sink. MPL Plotter aims to 
reduce that overhead by allowing you to effortlessly and concisely
- Generate publication quality plots with a single call
- Plot curve [comparisons](#51-comparison)
- Create figures with [many plots](#52-panes)

It is opinionated but built with flexibility in mind, which means that
- No default can't be changed
- Any and all further customization with Matplotlib is compatible. From ticks to legends to extra axes to whatever suits your needs

There's two ways to use MPL Plotter (plus any Matplotlib before or after):
- Calls to the 2D and 3D [plotting methods](#4-getting-started)
- Using [presets](#6-presets), either those shipped with the library, or custom ones

It does the job for me and I expand it when it can't. Hope you find some use in it!

# 2. Install

`pip install mpl_plotter`

All dependencies will be checked for and installed automatically. They can be found in `setup.py` 
under `install_requires`.

# 3. Map of the library

This is the map of the library for import reference. 

| module | class | function |
| --- | --- | --- |
| **module** | `class` | function |

- **mpl_plotter**
    - figure
    - get_available_fonts
    - `markers`
    - **two_d**
        - `line`
        - `scatter`
        - `heatmap`
        - `quiver`
        - `streamline`
        - `fill_area`
        - `comparison`
        - `panes`
    - **three_d**
        - `line`
        - `scatter`
        - `surface`
    - **presets**
        - **publication**
            - `two_d`
            - `three_d`
        - **precision**
            - `two_d`
            - `three_d`
        - **preset**
	        - `preset`
            - `two_d`
            - `three_d`
    - **color**
        - **schemes**
            - colorscheme_one
	    - **functions**
           - complementary
           - delta
	    - **maps**
	        - custom
           - mapstack

# 4. Getting started

In this section we'll go from the the most basic plot to a fairly customized version in 2 and 3 dimensions. 
The line demo scripts can be found in `demo/scripts/line_demos/`.

### 4.1 2D

For this example I'll use the 2D `line` class. Except for plot-specific arguments (line width etc. in this case), 
you can use the same inputs in this example with any of the other 2D plotting classes. Check the [API reference](https://mpl-plotter-docs.github.io/)
for all general and specific arguments, or call `help(<plotting class>)` in your shell to access the docstrings. 

As follows from the map above, the import to use the 2D `line` class is:

    from mpl_plotter.two_d import line

And the following is the most basic MPL Plotter call, which will generate the image below (no input, and sin wave 
respectively).
    
| `line(show=True)` | `x = np.linspace(0, 2*np.pi, 100)`<br>`y = np.sin(x)`<br>`line(x=x, y=y, show=True)` |
| --- | :--- |
| ![alt text](demo/gallery/2d/basic_line.png "Base output") | ![alt text](demo/gallery/2d/line_input.png "sin wave") 

Two important features are apparent:
1. MPL Plotter provides mock plots for every plotting class, so you can get straight into action and see what each does
2. MPL Plotter is somewhat "opinionated" and sets up quite a few parameters by default. This is based purely on my 
preference. You may not agree and you're more than welcome to play around with them!

---

Two more examples (results in the table below):

1. We can add some customization to make our line look a bit better:

        line(show=True, pad_demo=True, spines_removed=None)

    Our line has now some margins to breathe while the ticks are placed at the maximum and minimums of our curve, 
    and no spines are removed.

2. Lastly, an example using some of the parameters you can change:

        line(norm=True, line_width=4,
         
             title="Custom Line", title_font="Pump Triline", title_size=40, title_color="orange",
 
             label_x="x", label_y="$\Psi$",
             label_size_x=30, label_size_y=20,
             label_pad_x=-0.05, label_pad_y=10,
             label_rotation_y=0,
 
             aspect=1,
             pad_demo=True,
             workspace_color="darkred",
             grid=True, grid_color="grey",
             
             tick_color="darkgrey", tick_decimals=4,
             tick_number_x=12, tick_number_y=12,
             tick_rotation_x=35,
 
             color_bar=True, cb_tick_number=5, cb_pad=0.05,
 
             show=True)

| [1](https://github.com/alopezrivera/mpl_plotter/blob/master/demo/scripts/line2.py#L13) | [2](https://github.com/alopezrivera/mpl_plotter/blob/master/demo/scripts/line2.py#L21) |
| --- | --- |
| ![alt text](demo/gallery/2d/medium_line.png "Some customization") | ![alt text](demo/gallery/2d/custom_line.png "Showcase") |

### 4.2 3D

Same applies in 3D.

| [0](https://github.com/alopezrivera/mpl_plotter/blob/master/demo/scripts/line3.py#L5) | [1](https://github.com/alopezrivera/mpl_plotter/blob/master/demo/scripts/line3.py#L15) | [2](https://github.com/alopezrivera/mpl_plotter/blob/master/demo/scripts/line3.py#L31) |
|---|---|---|
|![alt text](demo/gallery/3d/basic_line.png "Basic")|![alt text](demo/gallery/3d/medium_line.png "Some customization")|![alt text](demo/gallery/3d/custom_line.png "Showcase")|

# 5. Curve comparisons and multiple pane plots

`from mpl_plotter.two_d import comparison, panes`

### 5.1 `comparison`

Plot any number of curves in a single plot. Axis limits will be set to the maximum and minimum of all your curves. 
No data will be left out, among other niceties.

#### Data input

Inputs must match (2 `x`s and 3 `y`s won't work), BUT the following inputs are all valid:
|   x                      |   y                       |  result  |  notes               |
|  ---                     |  ---                      |  ---     |  ---                 |
|  array                   |  array                    |  1       |                      |
|  array                   |  [array, array]           |  2       |  Both `y`s share `x` |
|  [array, array]          |  [array, array]           |  2       |  Each `y` has an `x` |
|  [n*[array]]             |  [n*[array]]              |  n       |  Each `y` has an `x` |

#### Plotting methods

You can specify **different plotting methods for each curve in the plot**, a custom one for all curves, 
or not specify any (defaulting to lines). How? Check the code block below. 

This is nice as it allows you to crisply combine lines, scatter plots and any other of the MPL Plotter
plotting methods.

#### Other arguments

As to any and all other arguments:
- **Singular arguments**: the regular MPL Plotter plotting class arguments. Apply to all curves in the plot.
- **Plural arguments**: pass a list of arguments, one for each curve. The result is as you'd imagine.

```
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
```

![alt text](demo/gallery/2d/comparison_custom.png "Curve comparison")
 

### 5.2 `panes`
 
The panes function allows for the plotting of a series of graphs in side-by-side panes. As to data input, the table below applies. 
It uses the `comparison`, function under the hood so the same input guidelines apply for all other inputs.

|   x                              |   y                               |  result  |  notes                                          |
|  ---                             |  ---                              |  ---     |  ---                                            |
|  array                           |  array                            |  11      |                                                 |
|  array                           |  [array, array]                   |  12      |  Both `y`s share `x`                            |
|  [n*[array]]                     |  [n*[array]]                      |  1n      |  Each `y` has an `x`                            |
|  array                           |  [array, array]                   |  21      |  Both `y`s share `x`                            |
|  [array, array]                  |  [array, array]                   |  21      |  Each `y` has an `x`                            |
|  array                           |  [n*[array], n*[array]]           |  2n      |  All curves in all (2) panes share a single `x` |
|  [array, array]                  |  [n*[array], n*[array]]           |  2n      |  All curves in each pane share an `x`           |
|  [n*[array], n*[array]]          |  [n*[array], n*[array]]           |  2n      |  All curves in all (2) panes have their own `x` |
|  [n*[array], ... up to m]        |  [n*[array], ... up to m]         |  mn      |  All curves in all panes have their own `x`     |

### Code

The following plots one curve per pane (3 in total):
     
```
panes(x,                   # Horizontal vector
      [u, v, y],           # List of curves to be plotted
      ["u", "v", "y"],     # List of vertical axis labels
      ["a", "b", "c"]      # List of legend labels 
      )
```

![alt text](demo/gallery/2d/pane_single.png "Single-curve panes")

And the following plots an arbitrary number of curves per pane. As you can see, you just need to input 
`n` **lists** of `m` curves (where `m`=2 in the example below), and you will get a plot with `n` panes, with `m`
curves in each.

```
panes(x,                               # Horizontal vector
      [[u, uu], [v, vv], [y, yy]],     # List of pairs of curves to be compared
      ["u", "v", "y"],                 # List of vertical axis labels
      ["a", "b"]                       # List of legend labels
      )
```

![alt text](demo/gallery/2d/pane_comparison.png "Multiple-curve comparison panes")

### Demo

Preposterous demonstration to illustrate the **n** panes, **m** curves concept. The code for these is
available in `tests/test_panes.py`.

![alt text](demo/gallery/2d/pane_alot.png "There's a lot")

![alt text](demo/gallery/2d/pane_alot_comparison.png "Lots of triplets") 

# 6. Presets

TL;DR: Take a parameter `toml` and forget about function inputs.

### 6.1 Standard presets

Standard presets are available to remove overhead. They're tailored for my use cases but you may find them useful anyway.

| ![alt text](demo/gallery/2d/preset_publication_scatter.png "Publication preset")| ![alt text](demo/gallery/2d/preset_publication_heatmap.png "Publication preset") | ![alt text](demo/gallery/2d/preset_publication_quiver.png "Publication preset") | ![alt text](demo/gallery/2d/preset_publication_streamline.png "Publication preset") | ![alt text](demo/gallery/2d/preset_publication_fill.png "Publication preset") | ![alt text](demo/gallery/3d/preset_publication_line.png "Publication preset") | ![alt text](demo/gallery/3d/preset_publication_scatter.png "Publication preset") | ![alt text](demo/gallery/3d/preset_publication_surface.png "Publication preset") |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ![alt text](demo/gallery/2d/preset_precision_scatter.png "Precision preset")| ![alt text](demo/gallery/2d/preset_precision_heatmap.png "Precision preset") | ![alt text](demo/gallery/2d/preset_precision_quiver.png "Precision preset") | ![alt text](demo/gallery/2d/preset_precision_streamline.png "Precision preset") | ![alt text](demo/gallery/2d/preset_precision_fill.png "Precision preset") | ![alt text](demo/gallery/3d/preset_precision_line.png "Precision preset") | ![alt text](demo/gallery/3d/preset_precision_scatter.png "Precision preset") | ![alt text](demo/gallery/3d/preset_precision_surface.png "Precision preset") | 

#### _Publication_
It is a common mistake to make a figure for a paper with unreadable labels. This preset tries to solve that, 
generating plots optimized to be printed on a small format, in side-by-side plots or embedded in a column of text.

    from mpl_plotter.presets.precision import two_d
    from mpl_plotter.color.schemes import one           # Custom colorscheme

    x = np.linspace(0, 4, 1000)
    y = np.exp(x)
    z = abs(np.sin(x)*np.exp(x))
    
    two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)
    
![alt text](demo/gallery/2d/preset_publication_line.png "Publication preset")

#### _Precision_

Made to plot functions large on the screen, with equal x and y scales to avoid skewing the variables, and 
many ticks to visually inspect a signal.

    from mpl_plotter.presets.precision import two_d
    
    two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)

![alt text](demo/gallery/2d/preset_precision_line.png "Precision preset")

### 6.2 Custom presets

Example workflow follows. For further reference check [the preset tests](https://github.com/alopezrivera/mpl_plotter/blob/master/tests/test_presets.py).

1. Import the preset creation function
      ```
      from mpl_plotter.presets import preset
      ```

2. Create a preset, either from a plotter,
      ```
      from mpl_plotter.two_d import line

      _preset = preset(line)
      ```
   
   or from a dimension. In this case, the preset will contain all common parameters to all plots
   in 2 or 3 dimensions.
      ```
      _preset = preset(dim=2)
      ```
	
   The preset is a dictionary. You can edit its parameters as you would expect. However, it is more convenient to

3. Save your preset in a `toml` file. This will yield you a `toml` file containing all parameters for your plot or dimension, allowing you to easily inspect defaults and tailor settings to your liking. You may edit this file as you please, as long as you do not infringe on its syntax.
      ```
      _preset.save('tests/presets/test.toml')
      ```

4. Load the file in the same -or a different session.
      ```
      from mpl_plotter.presets import preset

      _preset = preset.load('tests/presets/test.toml')
      ```

5. Import an MPL Plotter preset plotter and load it with your preset
      ```
      from mpl_plotter.presets import two_d

      _two_d = two_d(preset=_preset)
      ```

6. Plot as you wish
      ```
      _two_d.line(show=True)
      _two_d.scatter(show=True)
      _two_d.<...>
      ```

# 7. Matplotlib
### 7.1 Retrieving axes, figures

The axis and figure on which each class draws are instance attributes. To retrieve them and continue modifications 
using standard Matplotlib:
    
    from mpl_plotter.two_d import line
    
    my_plot = line()
    ax, fig = my_plot.ax, my_plot.fig
    
With the axis and figure, most Matplotlib functions out there can be used to further modify your plots. 

### 7.2 Using Matplotlib's axis tiling

Matplotlib allows for subplot composition using `subplot2grid`. This can be used in combination with MPL Plotter:

Importantly:
- The auxiliary function `figure` (`from mpl_plotter figure`) sets up a figure in a chosen backend. 
This is convenient, as if the figure is created with `plt.figure()`, only the default non-interactive Matplotlib 
backend will be available, unless `matplotlib.use(<backend>)` is specified before importing `pyplot`.

```
from mpl_plotter import figure
from mpl_plotter.two_d import line, quiver, streamline, fill_area

backend = "Qt5Agg"  # None -> regular non-interactive matplotlib output

figure(figsize=(10, 10), backend=backend)

ax0 = plt.subplot2grid((2, 2), (0, 0), rowspan=1)
ax1 = plt.subplot2grid((2, 2), (1, 0), rowspan=1)
ax2 = plt.subplot2grid((2, 2), (0, 1), rowspan=1)
ax3 = plt.subplot2grid((2, 2), (1, 1), rowspan=1)

axes = [ax0, ax1, ax2, ax3]
plots = [line, quiver, streamline, fill_area]

for i in range(len(plots)):
    plots[i](ax=axes[i])

plt.show()
```

![alt text](demo/gallery/2d/grid.png "Grid sample")       

---

[Back to top](#mpl-plotter)
