"""
Advent of Code 2025 - Day 5: Cafeteria
"""


def parse_input(input_file: str) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Parse the input file into fresh ID ranges and available ingredient IDs.
    
    Args:
        input_file: Path to the input file
        
    Returns:
        Tuple of (fresh_ranges, available_ids)
        - fresh_ranges: List of (start, end) tuples for fresh ingredient ranges
        - available_ids: List of available ingredient IDs to check
    """
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f]
    
    # Find the blank line separating ranges from IDs
    blank_idx = lines.index('')
    
    # Parse ranges (format: "start-end")
    fresh_ranges = []
    for line in lines[:blank_idx]:
        start, end = line.split('-')
        fresh_ranges.append((int(start), int(end)))
    
    # Parse available IDs
    available_ids = [int(line) for line in lines[blank_idx + 1:] if line]
    
    return fresh_ranges, available_ids


def is_fresh(ingredient_id: int, fresh_ranges: list[tuple[int, int]]) -> bool:
    """
    Check if an ingredient ID is fresh (falls within any fresh range).
    
    Args:
        ingredient_id: The ingredient ID to check
        fresh_ranges: List of (start, end) tuples for fresh ingredient ranges
        
    Returns:
        True if the ingredient is fresh, False if spoiled
    """
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ingredients(fresh_ranges: list[tuple[int, int]], available_ids: list[int]) -> int:
    """
    Count how many of the available ingredient IDs are fresh.
    
    Args:
        fresh_ranges: List of (start, end) tuples for fresh ingredient ranges
        available_ids: List of available ingredient IDs to check
        
    Returns:
        Number of fresh ingredients
    """
    fresh_count = 0
    for ingredient_id in available_ids:
        if is_fresh(ingredient_id, fresh_ranges):
            fresh_count += 1
    return fresh_count


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping ranges into non-overlapping ranges.
    
    Args:
        ranges: List of (start, end) tuples
        
    Returns:
        List of merged non-overlapping (start, end) tuples
    """
    if not ranges:
        return []
    
    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # Check if current range overlaps or is adjacent to the last merged range
        if current_start <= last_end + 1:
            # Merge by extending the end if necessary
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as separate range
            merged.append((current_start, current_end))
    
    return merged


def count_all_fresh_ids(fresh_ranges: list[tuple[int, int]]) -> int:
    """
    Count the total number of ingredient IDs that are considered fresh
    according to the fresh ingredient ID ranges.
    
    Args:
        fresh_ranges: List of (start, end) tuples for fresh ingredient ranges
        
    Returns:
        Total count of fresh ingredient IDs
    """
    # Merge overlapping ranges to avoid double-counting
    merged = merge_ranges(fresh_ranges)
    
    # Count total IDs in all merged ranges
    total_count = 0
    for start, end in merged:
        total_count += end - start + 1
    
    return total_count


def solve_part1(input_file: str) -> int:
    """Solve part 1 of the puzzle."""
    fresh_ranges, available_ids = parse_input(input_file)
    return count_fresh_ingredients(fresh_ranges, available_ids)


def solve_part2(input_file: str) -> int:
    """Solve part 2 of the puzzle."""
    fresh_ranges, _ = parse_input(input_file)
    return count_all_fresh_ids(fresh_ranges)


def main():
    """Main entry point."""
    # Test with example
    example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    
    # Create temporary file for example
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(example_input)
        example_file = f.name
    
    try:
        example_result = solve_part1(example_file)
        print(f"Example Part 1: {example_result}")
        assert example_result == 3, f"Expected 3, got {example_result}"
        
        example_result_part2 = solve_part2(example_file)
        print(f"Example Part 2: {example_result_part2}")
        assert example_result_part2 == 14, f"Expected 14, got {example_result_part2}"
        
        # Solve actual puzzle
        try:
            result_part1 = solve_part1('../data/day05.txt')
            print(f"\nPart 1 answer: {result_part1}")
            
            result_part2 = solve_part2('../data/day05.txt')
            print(f"Part 2 answer: {result_part2}")
        except FileNotFoundError:
            print("Input file not found. Please add your puzzle input to ../data/day05.txt")
    finally:
        import os
        os.unlink(example_file)


if __name__ == '__main__':
    main()
