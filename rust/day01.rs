// Advent of Code 2025 - Day 1: Secret Entrance

use std::fs;

fn parse_rotation(line: &str) -> (char, i32) {
    let direction = line.chars().next().unwrap();
    let distance: i32 = line[1..].parse().unwrap();
    (direction, distance)
}

fn apply_rotation(current_position: i32, direction: char, distance: i32) -> i32 {
    match direction {
        'L' => (current_position - distance).rem_euclid(100),
        'R' => (current_position + distance) % 100,
        _ => panic!("Invalid direction"),
    }
}

fn count_zeros_during_rotation(current_position: i32, direction: char, distance: i32) -> i32 {
    let mut zero_count = 0;

    match direction {
        'L' => {
            let full_rotations = distance / 100;
            zero_count += full_rotations;

            let remaining = distance % 100;
            if current_position > 0 && remaining >= current_position {
                zero_count += 1;
            }
        }
        'R' => {
            let full_rotations = distance / 100;
            zero_count += full_rotations;

            let remaining = distance % 100;
            if current_position < 100 && remaining >= (100 - current_position) {
                zero_count += 1;
            }
        }
        _ => panic!("Invalid direction"),
    }

    zero_count
}

fn count_zeros(rotations: &[String]) -> i32 {
    let mut position = 50;
    let mut zero_count = 0;

    for rotation in rotations {
        let (direction, distance) = parse_rotation(rotation);
        position = apply_rotation(position, direction, distance);

        if position == 0 {
            zero_count += 1;
        }
    }

    zero_count
}

fn count_all_zeros(rotations: &[String]) -> i32 {
    let mut position = 50;
    let mut zero_count = 0;

    for rotation in rotations {
        let (direction, distance) = parse_rotation(rotation);

        zero_count += count_zeros_during_rotation(position, direction, distance);

        position = apply_rotation(position, direction, distance);
    }

    zero_count
}

fn main() {
    // Test with example
    let example = vec![
        "L68".to_string(), "L30".to_string(), "R48".to_string(), "L5".to_string(), "R60".to_string(),
        "L55".to_string(), "L1".to_string(), "L99".to_string(), "R14".to_string(), "L82".to_string()
    ];

    let example_result_part1 = count_zeros(&example);
    println!("Example Part 1: {}", example_result_part1);
    assert_eq!(example_result_part1, 3);

    let example_result_part2 = count_all_zeros(&example);
    println!("Example Part 2: {}", example_result_part2);
    assert_eq!(example_result_part2, 6);

    // Solve actual puzzle
    let content = fs::read_to_string("../data/day01.txt").expect("Failed to read file");
    let rotations: Vec<String> = content.lines().map(|s| s.to_string()).collect();

    let result_part1 = count_zeros(&rotations);
    println!("\nPart 1 answer: {}", result_part1);

    let result_part2 = count_all_zeros(&rotations);
    println!("Part 2 answer: {}", result_part2);
}