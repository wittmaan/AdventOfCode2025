"""
Advent of Code 2025 - Day 3: Lobby
"""


def remove_k_digits(num_str: str, k: int) -> str:
    """
    Remove k digits from the string to maximize the resulting number.
    
    Args:
        num_str: String of digits
        k: Number of digits to remove
        
    Returns:
        The resulting string after removing k digits to maximize the number
    """
    stack = []
    for digit in num_str:
        while stack and stack[-1] < digit and k > 0:
            stack.pop()
            k -= 1
        stack.append(digit)
    
    # Remove remaining k from end
    while k > 0:
        stack.pop()
        k -= 1
    
    return ''.join(stack)


def find_max_joltage(bank: str, num_batteries: int = 2) -> int:
    """
    Find the maximum joltage possible from a single bank of batteries.
    
    Args:
        bank: String of digits representing the batteries
        num_batteries: Number of batteries to turn on (2 for part 1, 12 for part 2)
        
    Returns:
        The maximum number formed by the selected batteries
    """
    if num_batteries == 2:
        max_val = 0
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)):
                val = 10 * int(bank[i]) + int(bank[j])
                if val > max_val:
                    max_val = val
        return max_val
    elif num_batteries == 12:
        k = len(bank) - 12
        if k < 0:
            raise ValueError(f"Bank too short: {len(bank)} digits, need at least 12")
        remaining = remove_k_digits(bank, k)
        return int(remaining)
    else:
        raise ValueError(f"Unsupported num_batteries: {num_batteries}")


def solve_part1(input_file: str) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        input_file: Path to the input file
        
    Returns:
        The total output joltage for part 1
    """
    with open(input_file) as f:
        lines = f.read().strip().split('\n')
    
    total = 0
    for line in lines:
        total += find_max_joltage(line, num_batteries=2)
    
    return total


def solve_part2(input_file: str) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        input_file: Path to the input file
        
    Returns:
        The total output joltage for part 2
    """
    with open(input_file) as f:
        lines = f.read().strip().split('\n')
    
    total = 0
    for line in lines:
        total += find_max_joltage(line, num_batteries=12)
    
    return total


def main():
    """Main entry point."""
    # Test with example from problem description
    example_banks = [
        "987654321111111",
        "811111111111119", 
        "234234234234278",
        "818181911112111"
    ]
    
    # Part 1 tests
    expected_maxes_p1 = [98, 89, 78, 92]
    expected_total_p1 = 357
    
    for bank, expected in zip(example_banks, expected_maxes_p1):
        result = find_max_joltage(bank, num_batteries=2)
        assert result == expected, f"Part 1: Expected {expected} for {bank}, got {result}"
    
    total_p1 = sum(find_max_joltage(bank, 2) for bank in example_banks)
    assert total_p1 == expected_total_p1, f"Part 1: Expected {expected_total_p1}, got {total_p1}"
    
    print(f"Example Part 1 total: {total_p1}")
    
    # Part 2 tests
    expected_maxes_p2 = [987654321111, 811111111119, 434234234278, 888911112111]
    expected_total_p2 = 3121910778619
    
    for bank, expected in zip(example_banks, expected_maxes_p2):
        result = find_max_joltage(bank, num_batteries=12)
        assert result == expected, f"Part 2: Expected {expected} for {bank}, got {result}"
    
    total_p2 = sum(find_max_joltage(bank, 12) for bank in example_banks)
    assert total_p2 == expected_total_p2, f"Part 2: Expected {expected_total_p2}, got {total_p2}"
    
    print(f"Example Part 2 total: {total_p2}")
    
    # Solve actual puzzle
    try:
        result_p1 = solve_part1('../data/day03.txt')
        print(f"\nPart 1 answer: {result_p1}")
        
        result_p2 = solve_part2('../data/day03.txt')
        print(f"Part 2 answer: {result_p2}")
    except FileNotFoundError:
        print("Input file not found. Please ensure ../data/day03.txt exists")


if __name__ == '__main__':
    main()