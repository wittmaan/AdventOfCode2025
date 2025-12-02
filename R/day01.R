#!/usr/bin/env Rscript

# Advent of Code 2025 - Day 1: Secret Entrance (R, idiomatic)
# Implementation uses vectorized operations and minimal loops.

parse_input <- function(path = "data/day01.txt") {
  if (!file.exists(path)) {
    alt <- file.path("..", path)
    if (file.exists(alt)) path <- alt else stop("Input file not found: ", path)
  }
  txt <- paste(readLines(path, warn = FALSE), collapse = "\n")
  # split by any whitespace or newlines/commas to get instructions
  lines <- unlist(strsplit(txt, "[\r\n]+"))
  lines <- trimws(lines)
  # many inputs are a single long line with commas
  tokens <- unlist(strsplit(paste(lines, collapse = ","), ","))
  tokens[trimws(tokens) != ""]
}

parse_rotations_dt <- function(tokens) {
  # tokens like "L68" or "R48" -> data.frame with dir (+1/-1), dist, signed
  dirs <- substring(tokens, 1, 1)
  dists <- as.integer(substring(tokens, 2))
  dir_sign <- ifelse(dirs == "R", 1L, -1L)
  data.frame(token = tokens, dir = dirs, dist = dists, sign = dir_sign, stringsAsFactors = FALSE)
}

solve_part1_vec <- function(rot_df, start = 50L) {
  # vectorized positions after each rotation
  signed_d <- as.integer(rot_df$sign * rot_df$dist)
  csum <- cumsum(signed_d)
  end_pos <- (start + csum) %% 100L
  sum(end_pos == 0L)
}

solve_part2_vec <- function(rot_df, start = 50L) {
  signed_d <- as.integer(rot_df$sign * rot_df$dist)
  absd <- abs(signed_d)
  full <- absd %/% 100L
  rem <- absd %% 100L

  csum <- cumsum(signed_d)
  # starting positions for each rotation
  start_csum <- c(0L, head(csum, -1L))
  start_pos <- (start + start_csum) %% 100L

  # extra crossing in the final (partial) rotation
  extra <- integer(length(signed_d))
  # moving right (positive d): we cross 0 if remainder >= (100 - start_pos)
  right_idx <- which(signed_d > 0L)
  if (length(right_idx)) {
    extra[right_idx] <- as.integer(rem[right_idx] >= (100L - start_pos[right_idx]))
  }
  # moving left (negative d): we cross 0 if start_pos > 0 and remainder >= start_pos
  left_idx <- which(signed_d < 0L)
  if (length(left_idx)) {
    extra[left_idx] <- as.integer(start_pos[left_idx] > 0L & rem[left_idx] >= start_pos[left_idx])
  }

  sum(full + extra)
}

main <- function() {
  tokens <- parse_input("data/day01.txt")
  rot_df <- parse_rotations_dt(tokens)

  # validate with example
  example <- c('L68','L30','R48','L5','R60','L55','L1','L99','R14','L82')
  ex_df <- parse_rotations_dt(example)
  stopifnot(solve_part1_vec(ex_df) == 3L)
  stopifnot(solve_part2_vec(ex_df) == 6L)

  part1 <- solve_part1_vec(rot_df)
  part2 <- solve_part2_vec(rot_df)
  cat(sprintf("Part 1: %d\n", part1))
  cat(sprintf("Part 2: %d\n", part2))
}

if (identical(Sys.getenv("R_SCRIPT_RUNNING"), "TRUE") || (interactive() || (length(commandArgs(trailingOnly = TRUE)) >= 0))) {
  # Run main when executed as script
  main()
}
