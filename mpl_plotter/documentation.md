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

Module: `module`

Method: _method_

Directory: dir/

- `mpl_plotter`
    - _figure_
    - _get_available_fonts_
    - `two_d`
        - _line_
        - _scatter_
        - _heatmap_
        - _quiver_
        - _streamline_
        - _fill_area_
        - _comparison_
        - _panes_
        - _floating_text_
    - `three_d`
        - _line_
        - _scatter_
        - _surface_
        - _floating_text_
    - `canvas`
        - _custom_canvas_
    - `presets`
        - `publication`
            - _two_d_
            - _three_d_
        - `precision`
            - _two_d_
            - _three_d_
        - `custom`
            - _two_d_
            - _three_d_
            - _generate_preset_2d_
            - _generate_preset_3d_
        - data/
            - _publication_
            - _precision_
    - `color`
        - `schemes`
            - _colorscheme_one_
            - _custom_
        - `functions`
            - _complementary_
            - _delta_
            - _mapstack_