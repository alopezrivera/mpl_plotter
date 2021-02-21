class two_d:

    def floating_text(self, ax, text, font="serif", x=0.5, y=0.5, size=20, weight='normal', color='darkred'):
        # Font
        font = {'family': font,
                'color': color,
                'weight': weight,
                'size': size,
                }
        # Floating text
        ax.text(x, y, text, size=size, weight=weight, fontdict=font)


class three_d:

    def floating_text(self, ax, text, font, x, y, z, size=20, weight='normal', color='darkred'):
        # Font
        font = {'family': font,
                'color': color,
                'weight': weight,
                'size': size,
                }
        # Floating text
        ax.text(x, y, z, text, size=size, weight=weight, fontdict=font)
