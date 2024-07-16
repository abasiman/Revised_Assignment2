import sys

# Read cylinder requests from a file


def read_requests(file_name):
    try:
        with open(file_name, 'r') as f:
            return [int(line.strip()) for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)
    except ValueError:
        print("Error: File contains non-integer values.")
        sys.exit(1)

# Calculate total head movements


def calculate_movements(cylinders, start_position):
    total_moves = 0
    current_position = start_position
    for cylinder in cylinders:
        total_moves += abs(cylinder - current_position)
        current_position = cylinder
    return total_moves

# FCFS algorithm


def fcfs(cylinders, start_position):
    return calculate_movements(cylinders, start_position)

# SCAN algorithm


def scan(cylinders, start_position):
    cylinders.sort()
    left = [c for c in cylinders if c <= start_position]
    right = [c for c in cylinders if c > start_position]

    total_moves = calculate_movements(left[::-1], start_position)
    if right:
        total_moves += abs(left[0] - right[0])
        total_moves += calculate_movements(right, right[0])
    return total_moves

# C-SCAN algorithm


def c_scan(cylinders, start_position):
    cylinders.sort()
    left = [c for c in cylinders if c <= start_position]
    right = [c for c in cylinders if c > start_position]

    total_moves = calculate_movements(left[::-1], start_position)
    if right:
        total_moves += abs(left[0] - 0)  # Jump to the beginning of the disk
        total_moves += abs(4999 - 0)     # Move to the end of the disk
        total_moves += calculate_movements(right, 0)
    return total_moves

# Optimized FCFS (consider removing if FCFS is strictly first-come)


def optimized_fcfs(cylinders, start_position):
    # Note: FCFS should ideally not be optimized by sorting
    cylinders.sort()
    return calculate_movements(cylinders, start_position)

# Optimized SCAN


def optimized_scan(cylinders, start_position):
    lower_cylinders = [c for c in cylinders if c <= start_position]
    upper_cylinders = [c for c in cylinders if c > start_position]

    total_moves = 0
    if lower_cylinders:
        lower_cylinders.sort(reverse=True)
        total_moves += calculate_movements(lower_cylinders, start_position)

    if upper_cylinders:
        upper_cylinders.sort()
        if lower_cylinders:
            total_moves += abs(lower_cylinders[0] - upper_cylinders[0])
        total_moves += calculate_movements(upper_cylinders, upper_cylinders[0])
    else:
        if lower_cylinders:
            total_moves += calculate_movements(upper_cylinders, start_position)
    return total_moves

# Optimized C-SCAN


def optimized_cscan(cylinders, start_position):
    cylinders.sort()
    left = [c for c in cylinders if c < start_position]
    right = [c for c in cylinders if c >= start_position]

    total_moves = 0
    if right:
        total_moves += calculate_movements(right, start_position)
        if left:
            optimal_jump = min(left, key=lambda x: abs(4999 - x))
            total_moves += abs(right[-1] - optimal_jump)
            total_moves += calculate_movements(left, optimal_jump)
    else:
        if left:
            optimal_jump = min(left, key=lambda x: abs(4999 - x))
            total_moves += abs(start_position - optimal_jump)
            total_moves += calculate_movements(left, optimal_jump)

    return total_moves


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python DiskScheduling.py <start_position> <requests_file>")
        sys.exit(1)

    try:
        start_position = int(sys.argv[1])
    except ValueError:
        print("Error: <start_position> should be an integer.")
        sys.exit(1)

    file_name = sys.argv[2]
    requests = read_requests(file_name)

    print("FCFS Total Movements (Original):", fcfs(requests, start_position))
    print("SCAN Total Movements (Original):", scan(requests, start_position))
    print("C-SCAN Total Movements (Original):",
          c_scan(requests, start_position))

    print("Optimized FCFS Total Movements:",
          optimized_fcfs(requests, start_position))
    print("Optimized SCAN Total Movements:",
          optimized_scan(requests, start_position))
    print("Optimized C-SCAN Total Movements:",
          optimized_cscan(requests, start_position))
