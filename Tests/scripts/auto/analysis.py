import math

def compute_average(execution_times):
    return sum(execution_times) / len(execution_times)

def compute_std_dev(execution_times, average_time):
    return math.sqrt(sum((x - average_time) ** 2 for x in execution_times) / len(execution_times))


def compute_medium(execution_times):
    # Compute median
    sorted_times = sorted(execution_times)
    n = len(sorted_times)
    if n % 2 == 1:
        return sorted_times[n // 2]
    else:
        return (sorted_times[n // 2 - 1] + sorted_times[n // 2]) / 2
    

def run_analysis(execution_times, title):
    average_time = compute_average(execution_times)
    std_div_time = compute_std_dev(execution_times, average_time)
    medium_time = compute_medium(execution_times)

    # Print results
    print(f"Average execution time for {title}: {average_time:.6f} seconds")
    print(f"Standard deviation of execution time: {std_div_time:.6f} seconds")
    print(f"Median execution time: {medium_time:.6f} seconds\n")
    