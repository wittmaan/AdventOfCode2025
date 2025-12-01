"""
Advent of Code 2025 - Day 1: Secret Entrance
"""

def parse_rotation(line: str) -> tuple[str, int]:
    """Parse a rotation instruction into direction and distance."""
    direction = line[0]
    distance = int(line[1:])
    return direction, distance


def apply_rotation(current_position: int, direction: str, distance: int) -> int:
    """
    Apply a rotation to the current dial position.
    
    Args:
        current_position: Current position on the dial (0-99)
        direction: 'L' for left (toward lower numbers) or 'R' for right
        distance: Number of clicks to rotate
        
    Returns:
        New position on the dial (0-99)
    """
    if direction == 'L':
        new_position = (current_position - distance) % 100
    else:  # direction == 'R'
        new_position = (current_position + distance) % 100
    
    return new_position


def count_zeros_during_rotation(current_position: int, direction: str, distance: int) -> int:
    """
    Count how many times the dial points at 0 during a rotation (including the endpoint).
    
    Args:
        current_position: Current position on the dial (0-99)
        direction: 'L' for left or 'R' for right
        distance: Number of clicks to rotate
        
    Returns:
        Number of times the dial points at 0 during the rotation
    """
    zero_count = 0
    
    if direction == 'L':
        # Moving left (decreasing)
        # Calculate how many times we hit 0
        # We hit 0 every 100 clicks, plus once if we cross it in the remainder
        full_rotations = distance // 100
        zero_count += full_rotations
        
        # Check if we hit 0 in the partial rotation
        # Starting at current_position, going left by (distance % 100)
        remaining = distance % 100
        # We hit 0 if: current_position - i = 0 (mod 100) for some i in [1, remaining]
        # This means i = current_position (if current_position <= remaining)
        if current_position > 0 and remaining >= current_position:
            zero_count += 1
            
    else:  # direction == 'R'
        # Moving right (increasing)
        full_rotations = distance // 100
        zero_count += full_rotations
        
        # Check if we hit 0 in the partial rotation
        remaining = distance % 100
        # We hit 0 if: current_position + i = 0 (mod 100) for some i in [1, remaining]
        # This means i = 100 - current_position (if 100 - current_position <= remaining)
        if current_position < 100 and remaining >= (100 - current_position):
            zero_count += 1
    
    return zero_count


def count_zeros(rotations: list[str]) -> int:
    """
    Count how many times the dial points at 0 after any rotation.
    
    Args:
        rotations: List of rotation instructions (e.g., ['L68', 'R48'])
        
    Returns:
        Number of times the dial points at 0
    """
    position = 50  # Starting position
    zero_count = 0
    
    for rotation in rotations:
        direction, distance = parse_rotation(rotation)
        position = apply_rotation(position, direction, distance)
        
        if position == 0:
            zero_count += 1
    
    return zero_count


def count_all_zeros(rotations: list[str]) -> int:
    """
    Count how many times the dial points at 0 during or after any rotation.
    
    Args:
        rotations: List of rotation instructions (e.g., ['L68', 'R48'])
        
    Returns:
        Total number of times the dial points at 0
    """
    position = 50  # Starting position
    zero_count = 0
    
    for rotation in rotations:
        direction, distance = parse_rotation(rotation)
        
        # Count zeros during the rotation
        zero_count += count_zeros_during_rotation(position, direction, distance)
        
        # Apply the rotation
        position = apply_rotation(position, direction, distance)
    
    return zero_count


def solve_part1(input_file: str) -> int:
    """Solve part 1 of the puzzle."""
    with open(input_file, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    return count_zeros(rotations)


def solve_part2(input_file: str) -> int:
    """Solve part 2 of the puzzle."""
    with open(input_file, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    return count_all_zeros(rotations)


def main():
    """Main entry point."""
    # Test with example
    example = [
        'L68', 'L30', 'R48', 'L5', 'R60',
        'L55', 'L1', 'L99', 'R14', 'L82'
    ]
    
    example_result_part1 = count_zeros(example)
    print(f"Example Part 1: {example_result_part1}")
    assert example_result_part1 == 3, f"Expected 3, got {example_result_part1}"
    
    example_result_part2 = count_all_zeros(example)
    print(f"Example Part 2: {example_result_part2}")
    assert example_result_part2 == 6, f"Expected 6, got {example_result_part2}"
    
    # Solve actual puzzle
    try:
        result_part1 = solve_part1('../data/day01.txt')
        print(f"\nPart 1 answer: {result_part1}")
        
        result_part2 = solve_part2('../data/day01.txt')
        print(f"Part 2 answer: {result_part2}")
    except FileNotFoundError:
        print("Input file not found. Please add your puzzle input to ../data/day01.txt")


if __name__ == '__main__':
    main()
