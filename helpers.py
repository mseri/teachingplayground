import numpy as np
import matplotlib.patches as patches
import matplotlib.lines as lines


def double_arrow(ax, left, right, *, text=None, delta=(0,0), size="xx-large", head_width=0.035, head_length=0.15, length_includes_head=True):
    dx, dy = delta
    lx, ly = left
    rx, ry = right
    midx, midy = (lx+rx)/2, (ly+ry)/2
    ax.arrow(midx, midy, (midx-lx), (midy-ly), head_width=head_width, head_length=head_length, length_includes_head=length_includes_head)
    ax.arrow(midx, midy, (midx-rx), (midy-ry), head_width=head_width, head_length=head_length, length_includes_head=length_includes_head)
    if text is not None:
        ax.text(midx+dx, midy+dy, text, size=size)


def cartesian_axes(ax, *, xticks, yticks, x='x', y='y', xprop={"labelpad":-16, "x":1.03}, yprop={"labelpad":-7, "y":1.03}):
    ax.spines[["left", "bottom"]].set_position("zero")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel(x, size="xx-large", labelpad=xprop["labelpad"], x=xprop["x"])
    ax.set_ylabel(y, size="xx-large", labelpad=yprop["labelpad"], y=yprop["y"], rotation=0)
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.set_xticks(xticks)
    ax.set_yticks(yticks)

    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    

def add_arrow_to_line2D(
    axes, line, arrow_locs=[0.2, 0.4, 0.6, 0.8],
    arrowstyle='-|>', arrowsize=1, transform=None,
    color=None):
    """
    Add arrows to a matplotlib.lines.Line2D at selected locations.

    Parameters:
    -----------
    axes: 
    line: Line2D object as returned by plot command
    arrow_locs: list of locations where to insert arrows, % of total length
    arrowstyle: style of the arrow
    arrowsize: size of the arrow
    transform: a matplotlib transform instance, default to data coordinates

    Returns:
    --------
    arrows: list of arrows
    """
    if not isinstance(line, lines.Line2D):
        raise ValueError("expected a matplotlib.lines.Line2D object")
    x, y = line.get_xdata(), line.get_ydata()

    arrow_kw = {
        "arrowstyle": arrowstyle,
        "mutation_scale": 10 * arrowsize,
    }

    if color is None:
        color = line.get_color()
        use_multicolor_lines = isinstance(color, np.ndarray)
        if use_multicolor_lines:
            raise NotImplementedError("multicolor lines not supported")
    
    arrow_kw['color'] = color
    
    linewidth = line.get_linewidth()
    if isinstance(linewidth, np.ndarray):
        raise NotImplementedError("multiwidth lines not supported")
    else:
        arrow_kw['linewidth'] = linewidth

    if transform is None:
        transform = axes.transData

    arrows = []
    for loc in arrow_locs:
        s = np.cumsum(np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2))
        n = np.searchsorted(s, s[-1] * loc)
        arrow_tail = (x[n], y[n])
        arrow_head = (np.mean(x[n:n + 2]), np.mean(y[n:n + 2]))
        p = patches.FancyArrowPatch(
            arrow_tail, arrow_head, transform=transform,
            **arrow_kw)
        axes.add_patch(p)
        arrows.append(p)
    return arrows