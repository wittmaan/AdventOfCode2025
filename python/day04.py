import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import os
import copy

def count_adjacent_rolls(grid, row, col):
    """Count how many adjacent positions contain paper rolls."""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
        (0, -1),           (0, 1),    # left, right
        (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
    ]
    
    rows = len(grid)
    cols = len(grid[0])
    adjacent_rolls = 0
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                adjacent_rolls += 1
    
    return adjacent_rolls


def count_accessible_rolls(grid):
    """
    Count how many paper rolls (@) can be accessed by a forklift.
    A roll can be accessed if it has fewer than 4 adjacent @ symbols.
    """
    rows = len(grid)
    cols = len(grid[0])
    accessible_count = 0
    
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                if count_adjacent_rolls(grid, row, col) < 4:
                    accessible_count += 1
    
    return accessible_count


def print_grid(grid, step=None):
    """Print the grid with optional step information."""
    if step is not None:
        print(f"\nStep {step}:")
    for row in grid:
        print(''.join(row))


def remove_all_accessible_rolls(grid, visualize=False):
    """
    Iteratively remove accessible rolls until no more can be removed.
    Returns the total number of rolls removed.
    """
    # Convert grid to a mutable list of lists
    grid = [list(row) for row in grid]
    total_removed = 0
    step = 0
    
    if visualize:
        print("Initial state:")
        print_grid(grid)
    
    while True:
        # Find all accessible rolls in current state
        accessible_positions = []
        rows = len(grid)
        cols = len(grid[0])
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '@':
                    if count_adjacent_rolls(grid, row, col) < 4:
                        accessible_positions.append((row, col))
        
        # If no accessible rolls, we're done
        if not accessible_positions:
            if visualize:
                print(f"\nNo more accessible rolls. Total removed: {total_removed}")
            break
        
        # Remove all accessible rolls
        for row, col in accessible_positions:
            grid[row][col] = '.'
        
        total_removed += len(accessible_positions)
        step += 1
        
        if visualize:
            print(f"\nRemoved {len(accessible_positions)} rolls (total: {total_removed})")
            print_grid(grid, step)
    
    return total_removed


def create_grid_image(grid, step, filename):
    """Create an image of the grid for GIF creation."""
    rows = len(grid)
    cols = len(grid[0])
    
    # Create a binary matrix (1 for @, 0 for .)
    matrix = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@':
                matrix[i][j] = 1
    
    # Create figure with fixed size for consistent GIF frames
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(matrix, cmap='Blues', interpolation='nearest')
    
    # Add grid lines
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', size=0)
    
    # Remove axis labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Add title
    if step == 0:
        ax.set_title(f'Initial State', fontsize=14, pad=10)
    else:
        ax.set_title(f'Step {step}', fontsize=14, pad=10)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()


def create_gif_from_grids(grid_states, output_filename='paper_rolls_removal.gif'):
    """Create a GIF from a list of grid states."""
    filenames = []
    
    # Create directory for temporary images
    os.makedirs('temp_images', exist_ok=True)
    
    # Create image for each step
    for i, (grid, step) in enumerate(grid_states):
        filename = f'temp_images/step_{i:02d}.png'
        create_grid_image(grid, step, filename)
        filenames.append(filename)
    
    # Create GIF
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    
    # Save GIF with slower frame rate for better viewing
    imageio.mimsave(output_filename, images, duration=1.0, loop=0)
    
    # Clean up temporary images
    for filename in filenames:
        os.remove(filename)
    os.rmdir('temp_images')
    
    print(f"GIF saved as {output_filename}")


def remove_all_accessible_rolls_with_gif(grid, create_gif=False):
    """
    Iteratively remove accessible rolls until no more can be removed.
    Optionally creates a GIF of the process.
    Returns the total number of rolls removed.
    """
    # Convert grid to a mutable list of lists
    grid = [list(row) for row in grid]
    total_removed = 0
    step = 0
    grid_states = []
    
    # Save initial state
    if create_gif:
        grid_states.append((copy.deepcopy(grid), 0))
    
    while True:
        # Find all accessible rolls in current state
        accessible_positions = []
        rows = len(grid)
        cols = len(grid[0])
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '@':
                    if count_adjacent_rolls(grid, row, col) < 4:
                        accessible_positions.append((row, col))
        
        # If no accessible rolls, we're done
        if not accessible_positions:
            break
        
        # Remove all accessible rolls
        for row, col in accessible_positions:
            grid[row][col] = '.'
        
        total_removed += len(accessible_positions)
        step += 1
        
        # Save state for GIF
        if create_gif:
            grid_states.append((copy.deepcopy(grid), step))
    
    # Create GIF if requested
    if create_gif:
        create_gif_from_grids(grid_states)
    
    return total_removed


def main():
    # Test with the example first
    example = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@."
    ]
    
    example_result_part1 = count_accessible_rolls(example)
    print(f"Part 1 - Accessible rolls (expected 13): {example_result_part1}")
    
    example_result_part2 = remove_all_accessible_rolls_with_gif(example, create_gif=False)
    print(f"Part 2 - Total removed (expected 43): {example_result_part2}")
    
    # Read the actual input file
    with open('../data/day04.txt', 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    # Part 1: Count accessible rolls
    result_part1 = count_accessible_rolls(grid)
    print(f"Part 1 - Number of rolls accessible by forklift: {result_part1}")
    
    # Part 2: Total rolls that can be removed (without visualization for large grid)
    result_part2 = remove_all_accessible_rolls_with_gif(grid, create_gif=False)
    print(f"Part 2 - Total rolls that can be removed: {result_part2}")


if __name__ == "__main__":
    main()
