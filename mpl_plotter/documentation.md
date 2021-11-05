Welcome to the MPL Plotter documentation!

# Introduction

Making plots for technical documents can be a time sink. MPL Plotter aims to 
reduce that overhead by allowing you to effortlessly and concisely
- Generate publication quality plots with a single call
- Plot curve comparisons
- Create figures with many plots

It is opinionated but built with flexibility in mind, which means that
- No default can't be changed
- Any and all further customization with Matplotlib is compatible. From ticks to legends to extra axes to whatever suits your needs

There's two ways to use MPL Plotter (plus any Matplotlib before or after):
- Calls to the 2D and 3D plotting classes
- Using presets, either those shipped with the library, or custom ones

It does the job for me and I expand it when it can't. Hope you find some use in it!

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
