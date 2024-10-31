import webbrowser
from os import path
from typing import Iterable, Tuple

import click
import numpy as np
from PIL import Image

# Reference: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# For fun, google "Conway's Game of Life". Google will show the game of life running in the background of the page.


def update(old_grid: np.ndarray) -> np.ndarray:
    new_grid = old_grid.copy()
    rows, cols = old_grid.shape

    cell_targets = set()
    live_cells = np.column_stack(np.nonzero(new_grid))
    for cell in live_cells:
        x, y = cell
        cell_targets.add((int(x), int(y)))
        for x_neighbor in range(max(x - 1, 0), min(x + 2, rows)):
            for y_neighor in range(max(y - 1, 0), min(y + 2, cols)):
                cell_targets.add((x_neighbor, y_neighor))

    for x, y in cell_targets:
        neighborhood = old_grid[
            max(x - 1, 0) : min(x + 2, rows), max(y - 1, 0) : min(y + 2, cols)
        ]
        if np.sum(neighborhood) == 3:
            new_grid[x, y] = 1
        elif np.sum(neighborhood) == 4:
            new_grid[x, y] = old_grid[x, y]
        else:
            new_grid[x, y] = 0
    return new_grid


def expand_array_by_factor(grid: np.ndarray, factor: int) -> np.ndarray:
    rows, cols = grid.shape
    expanded = np.zeros((rows * factor, cols * factor), dtype=np.uint8)
    for x in range(rows):
        for y in range(cols):
            if grid[x, y] == 1:
                expanded[
                    x * factor : (x + 1) * factor, y * factor : (y + 1) * factor
                ] = 1
    return expanded


def generate_image(grid: np.ndarray, idx: int, expansion: int = 50) -> Image:
    expanded_grid = expand_array_by_factor(grid, expansion)
    return Image.fromarray(expanded_grid * 255)


def play(h: int, w: int, seed: Iterable[Tuple[int, int]], steps: int) -> None:
    # TODO: show interactive b&w grid so that user can visually create a seed
    if max(map(lambda t: t[0], seed)) >= w:
        raise Exception("Seed exceeds range of grid in x")

    if max(map(lambda t: t[1], seed)) >= h:
        raise Exception("Seed exceeds range of grid in y")

    frames = []
    grid = np.zeros((h, w)).astype(np.uint8)
    for x, y in seed:
        grid[x][y] = 1

    frames.append(generate_image(grid, 0))

    for s in range(steps):
        grid = update(grid)
        frames.append(generate_image(grid, s + 1))

    frames[0].save(
        "output.gif",
        save_all=True,
        append_images=frames[1:],
        duration=steps * 3,
        loop=0,
    )


def choose_seed():
    space_ship_seed = [(1, 1), (2, 2), (2, 3), (3, 1), (3, 2)]

    # stop black from putting each tuple on its own line
    # fmt: off
    oscillator_seed = [
        (5, 4), (5, 5), (5, 6), (6, 4), (6, 6), (7, 4), (7, 5), 
        (7, 6), (8, 4), (8, 5), (8, 6), (9, 4), (9, 5), (9, 6), 
        (10, 4), (10, 5), (10, 6), (11, 4), (11, 6), (12, 4), 
        (12, 5), (12, 6),
    ]

    prompt = "\n".join(
        [
            "Welcome to the Game of Life!",
            "Please select a number for a pre-configured seed",
            "1) Spaceship",
            "2) Oscillator",
            "->",
        ]
    )
    
    try:
        seed = click.prompt(prompt, prompt_suffix="", type=click.IntRange(min=1, max=2))

        match seed:
            case 1:
                play(20, 20, space_ship_seed, 30)
            case 2:
                play(20, 20, oscillator_seed, 30)

        click.echo("Done!")

        open_chrome = click.prompt("Open gif? Uses Chrome. (y/n)", type=click.BOOL)
        if not open_chrome:
            return

        try:
            browser = webbrowser.get("chrome")
        except webbrowser.Error:
            click.echo("Chrome not found, open manually or install Chrome")
            return

        browser.open(f"file://{path.abspath('output.gif')}")

    except click.Abort:
        click.echo("\nGoodbye!")


if __name__ == "__main__":
    choose_seed()
