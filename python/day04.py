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


def remove_all_accessible_rolls(grid):
    """
    Iteratively remove accessible rolls until no more can be removed.
    Returns the total number of rolls removed.
    """
    # Convert grid to a mutable list of lists
    grid = [list(row) for row in grid]
    total_removed = 0
    
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
    
    example_result_part2 = remove_all_accessible_rolls(example)
    print(f"Part 2 - Total removed (expected 43): {example_result_part2}")
    
    # Read the actual input file
    with open('../data/day04.txt', 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    # Part 1: Count accessible rolls
    result_part1 = count_accessible_rolls(grid)
    print(f"Part 1 - Number of rolls accessible by forklift: {result_part1}")
    
    # Part 2: Total rolls that can be removed
    result_part2 = remove_all_accessible_rolls(grid)
    print(f"Part 2 - Total rolls that can be removed: {result_part2}")


if __name__ == "__main__":
    main()
