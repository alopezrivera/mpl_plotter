Welcome to the MPL Plotter API documentation!

# Introduction

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

# Map of the library

- **Bold**: package
- `Code`: methods
- Plain/: directories 

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
        - **maps**
            - `custom`
        - **schemes**
            - `one`
