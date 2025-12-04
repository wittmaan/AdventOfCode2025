def count_accessible_rolls(grid):
    """
    Count how many paper rolls (@) can be accessed by a forklift.
    A roll can be accessed if it has fewer than 4 adjacent @ symbols.
    """
    rows = len(grid)
    cols = len(grid[0])
    accessible_count = 0
    
    # Define the 8 adjacent positions (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
        (0, -1),           (0, 1),    # left, right
        (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
    ]
    
    # Check each position in the grid
    for row in range(rows):
        for col in range(cols):
            # Only check if current position has a paper roll
            if grid[row][col] == '@':
                # Count adjacent paper rolls
                adjacent_rolls = 0
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    # Check if position is within bounds
                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        if grid[new_row][new_col] == '@':
                            adjacent_rolls += 1
                
                # A roll can be accessed if fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    accessible_count += 1
    
    return accessible_count


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
    
    example_result = count_accessible_rolls(example)
    print(f"Example result (expected 13): {example_result}")
    
    # Read the actual input file
    with open('../data/day04.txt', 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    # Count accessible rolls
    result = count_accessible_rolls(grid)
    
    print(f"Number of rolls accessible by forklift: {result}")


if __name__ == "__main__":
    main()
