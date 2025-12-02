"""
Advent of Code 2025 - Day 2: Gift Shop
"""

def is_invalid_id(num: int) -> bool:
    """
    Check if a number is invalid (made of some sequence repeated twice).
    
    Args:
        num: The product ID to check
        
    Returns:
        True if the ID is invalid (pattern repeated twice), False otherwise
    """
    num_str = str(num)
    length = len(num_str)
    
    # Must be even length to be repeatable
    if length % 2 != 0:
        return False
    
    # Check if first half equals second half
    mid = length // 2
    first_half = num_str[:mid]
    second_half = num_str[mid:]
    
    return first_half == second_half


def parse_ranges(input_line: str) -> list[tuple[int, int]]:
    """
    Parse comma-separated ranges into list of (start, end) tuples.
    
    Args:
        input_line: String like "11-22,95-115,998-1012"
        
    Returns:
        List of (start, end) tuples
    """
    ranges = []
    parts = input_line.strip().split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Find the position of the dash that separates the range
            # We need to handle cases like "78847-119454"
            dash_pos = part.find('-')
            # Check if there might be more dashes (negative numbers)
            # For this problem, we don't have negative numbers, so simple split works
            start_str, end_str = part.split('-', 1)
            start, end = int(start_str), int(end_str)
            ranges.append((start, end))
    
    return ranges


def find_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """
    Find all invalid IDs within a given range.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        
    Returns:
        List of invalid IDs in the range
    """
    invalid_ids = []
    
    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)
    
    return invalid_ids


def solve_part1(input_file: str) -> int:
    """Solve part 1 of the puzzle."""
    with open(input_file, 'r') as f:
        input_line = f.read().strip()
    
    ranges = parse_ranges(input_line)
    total = 0
    
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end)
        total += sum(invalid_ids)
    
    return total


def main():
    """Main entry point."""
    # Test with example
    example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    
    # Test individual cases
    assert is_invalid_id(11) == True, "11 should be invalid"
    assert is_invalid_id(22) == True, "22 should be invalid"
    assert is_invalid_id(99) == True, "99 should be invalid"
    assert is_invalid_id(1010) == True, "1010 should be invalid"
    assert is_invalid_id(123123) == True, "123123 should be invalid"
    assert is_invalid_id(101) == False, "101 should be valid"
    assert is_invalid_id(100) == False, "100 should be valid"
    
    # Test example
    ranges = parse_ranges(example)
    total = 0
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end)
        total += sum(invalid_ids)
    
    print(f"Example result: {total}")
    assert total == 1227775554, f"Expected 1227775554, got {total}"
    
    # Solve actual puzzle
    try:
        result = solve_part1('../data/day02.txt')
        print(f"Part 1 answer: {result}")
    except FileNotFoundError:
        print("Input file not found. Please add your puzzle input to ../data/day02.txt")


if __name__ == '__main__':
    main()
