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
        self.plt.rcParams['font.sans-serif'] ="DejaVu Serif" if self.font == "serif" else self.font
        mpl.rc('font', cursive="Apple Chancery" if self.font == "serif" else self.font)
        mpl.rc('font', fantasy="Chicago" if self.font == "serif" else self.font)
        mpl.rc('font', monospace="Bitstream Vera Sans Mono" if self.font == "serif" else self.font)

        mpl.rc('mathtext', fontset=self.math_font)

        mpl.rc('text', color=self.font_color)
        mpl.rc('xtick', color=self.font_color)
        mpl.rc('ytick', color=self.font_color)
        mpl.rc('axes', labelcolor=self.font_color)

    def method_title(self):
        if self.title is not None:

            self.ax.set_title(self.title,
                              y=self.title_y,
                              fontname=self.font if self.title_font is None else self.title_font,
                              weight=self.title_weight,
                              color=self.workspace_color if self.title_color is None else self.title_color,
                              size=self.title_size+self.font_size_increase)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if self.label_x is not None:
            self.ax.set_xlabel(self.label_x, fontname=self.font, weight=self.label_weight_x,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_x+self.font_size_increase, labelpad=self.label_pad_x,
                               rotation=self.label_rotation_x)

        if self.label_y is not None:
            self.ax.set_ylabel(self.label_y, fontname=self.font, weight=self.label_weight_y,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_y+self.font_size_increase, labelpad=self.label_pad_y,
                               rotation=self.label_rotation_y)

        if self.label_z is not None:
            self.ax.set_zlabel(self.label_z, fontname=self.font, weight=self.label_weight_z,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_z+self.font_size_increase, labelpad=self.label_pad_z,
                               rotation=self.label_rotation_z)
