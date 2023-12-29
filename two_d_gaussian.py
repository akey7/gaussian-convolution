import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import cm
from math import exp
import time


def two_d_gaussian(points = 100,
    min_x = -4.,
    min_y = -4.,
    max_x = 4.,
    max_y = 4.,
    x0 = 0.,
    y0 = 0.,
    var_x = 1.,
    var_y = 1.
):
    xs = np.linspace(min_x, max_x, points)
    ys = np.linspace(min_y, max_y, points)
    zs = np.zeros((points, points), np.float64)

    for ix, x in enumerate(xs):
        for iy, y in enumerate(ys):
            zs[ix, iy] = exp(-((x-x0)**2/2/var_x + (y-y0)**2/2/var_y))

    return xs, ys, zs


def main():
    dpi = 100
    width = 1080 / dpi
    height = 1920 / 2 / dpi
    seconds = 10
    frame_rate_ms = 33
    bgcolor = "#1E1E1E"
    line_color = "#73FBD3"
    axis_color = "#01BAEF"
    annotation_color = "#FFFFFF"
    # heading_text_color = "#FC7753"

    ms_per_frame = 33
    frames = 300
    x0_steps = np.concatenate([np.linspace(-4, 0, frames // 3), np.zeros(frames // 3), np.linspace(0, 4, frames // 3)])
    y0_steps = np.concatenate([np.linspace(-4, 0, frames // 3), np.zeros(frames // 3), np.linspace(0, 4, frames // 3)])

    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(width, height), dpi=dpi, subplot_kw={"projection": "3d"})

    def init_func():
        xs, ys, zs = two_d_gaussian(x0=x0_steps[0], y0=y0_steps[0])
        xs, ys = np.meshgrid(xs, ys)
        axs.set_xlabel("x", size=15)
        axs.set_ylabel("y", size=15)
        axs.set_zlabel("z", size=15)
        sfc = axs.plot_surface(ys, xs, zs, cmap=cm.plasma, linewidth=0, antialiased=True)
        return sfc,

    def update(frame):
        start_time = int(time.time() * 1000)
        xs, ys, zs = two_d_gaussian(x0=x0_steps[frame], y0=y0_steps[frame])
        sfc = axs.plot_surface(ys, xs, zs, cmap=cm.plasma, linewidth=0, antialiased=True)
        end_time = int(time.time() * 1000)
        print(f"Rendered frame {frame} in {end_time-start_time} ms")
        return sfc,

    ani = animation.FuncAnimation(fig=fig, func=update, init_func=init_func, frames=300, interval=ms_per_frame)
    ani.save(filename=os.path.join("output", "single_2d_gaussian.mp4"), writer="ffmpeg")


if __name__ == "__main__":
    main()