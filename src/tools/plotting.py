import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray
import imageio
import matplotlib.pyplot as plt
import os


def create_gif(figures: list[plt.Figure], filename: str) -> str:
    # Initialize list to store images
    images = []

    # Loop through each figure in the list
    for fig in figures:
        # Save the figure as a PNG image
        fig.savefig("temp.png")

        # Append the PNG image to the list of images
        images.append(imageio.imread("temp.png"))

    # Remove the file if it already exists
    if os.path.exists(filename):
        os.remove(filename)

    # Save the list of images as a GIF
    imageio.mimsave(filename, images, fps=5)

    # Remove the temporary files
    for f in os.listdir("."):
        if f.startswith("temp") and f.endswith(".png"):
            os.remove(f)

    print(f"GIF generated at: {filename}")

    # Return the file path of the saved GIF
    return os.path.abspath(filename)


def generate_empty_grid(n_half: int):
    node_xyz = []
    color_xyz = []
    for x in range(0, n_half * 2 + 1):
        for y in range(0, n_half * 2 + 1):
            for z in range(0, n_half * 2 + 1):
                node_xyz.append([x, y, z])
                color_xyz.append("white")

    return plot_3d_grid(np.array(node_xyz), np.array(color_xyz))


def plot_3d_grid(
    node_xyz: list | NDArray,
    color_xyz: list | NDArray,
    edge_xyz: list | NDArray = None,
) -> plt.Figure:
    if isinstance(node_xyz, list):
        node_xyz = np.array(node_xyz)
    if isinstance(color_xyz, list):
        color_xyz = np.array(color_xyz)
    if isinstance(edge_xyz, list):
        edge_xyz = np.array(edge_xyz)

    # Convert node_xyz to a 2D array
    node_xyz = node_xyz.reshape(-1, 3)

    # Create the 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot the nodes - alpha is scaled by "depth" automatically
    ax.scatter(*node_xyz.T, s=100, c=color_xyz, edgecolors="black", linewidth=1)

    # Plot the edges
    if edge_xyz is not None:
        for vizedge in edge_xyz:
            ax.plot(*vizedge.T, color="tab:gray")

    # Turn gridlines off
    ax.grid(True)
    # Suppress tick labels
    for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
        dim.set_ticks([])
    # Set axes labels
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    fig.tight_layout()
    # fig.show()
    plt.close(fig)

    return fig


if __name__ == "__main__":
    # g = generate_empty_grid(1)
    # g.savefig("empty_1", format="svg")
    new_grid = GridBuilder.generate(half_size=1)
    # new_grid.plot.show()
    current_node_state = new_grid.local_state(new_grid.current_point)
    current_node_state.plot.savefig("local_state", format="svg")
