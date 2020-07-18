def floating_text2d(ax, text, font, x, y, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, text, size=size, weight=weight, fontdict=font)