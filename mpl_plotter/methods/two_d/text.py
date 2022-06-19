# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Text
----
"""


import matplotlib as mpl


class text:

    def method_fonts(self):
        """
        Fonts
        
        Reference:

            - https://matplotlib.org/2.0.2/users/customizing.html
        
        Pyplot method:
            plt.rcParams['<category>.<item>'] = <>
        """
        mpl.rc('font', family=self.font)
        mpl.rc('font', serif="DejaVu Serif" if self.font == "serif" else self.font)
        self.plt.rcParams['font.sans-serif'] = "DejaVu Serif" if self.font == "serif" else self.font
        mpl.rc('font', cursive="Apple Chancery" if self.font == "serif" else self.font)
        mpl.rc('font', fantasy="Chicago" if self.font == "serif" else self.font)
        mpl.rc('font', monospace="Bitstream Vera Sans Mono" if self.font == "serif" else self.font)

        mpl.rc('mathtext', fontset=self.math_font)
        mpl.rc('text', color=self.font_color)

    def method_title(self):
        if self.title is not None:
            self.ax.set_title(self.title,
                              fontname=self.font if isinstance(self.title_font, type(None)) else self.title_font,
                              weight=self.title_weight,
                              color=self.title_color if self.title_color is not None
                                    else self.font_color if self.font_color is not None
                                    else self.workspace_color,
                              size=self.title_size + self.font_size_increase)
            self.ax.title.set_position((0.5, self.title_pos_y))

    def method_axis_labels(self):
        if self.label_x is not None:

            # Draw label
            self.ax.set_xlabel(self.label_x, fontname=self.font, weight=self.label_weight_x,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_x + self.font_size_increase, labelpad=self.label_pad_x,
                               rotation=self.label_rotation_x)

            # Custom coordinates if provided
            if self.label_coords_x is not None:
                self.ax.xaxis.set_label_coords(x=self.label_coords_x[0], y=self.label_coords_x[1])

        if self.label_y is not None:

            # y axis label rotation
            if isinstance(self.label_rotation_y, type(None)):
                latex_chars  = re.findall(r'\$\\(.*?)\$', self.label_y)
                label_length = len(self.label_y) - 2*len(latex_chars) - len(''.join(latex_chars).replace('//', '/'))
                self.label_rotation_y = 90 if label_length > 3 else 0

            # Draw label
            self.ax.set_ylabel(self.label_y, fontname=self.font, weight=self.label_weight_y,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_y + self.font_size_increase, labelpad=self.label_pad_y,
                               rotation=self.label_rotation_y)

            # Custom coordinates if provided
            if self.label_coords_y is not None:
                self.ax.yaxis.set_label_coords(x=self.label_coords_y[0], y=self.label_coords_y[1])

