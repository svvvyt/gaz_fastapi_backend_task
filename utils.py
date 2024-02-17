def calculate_median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        middle1 = n // 2
        middle2 = middle1 - 1
        return (sorted_data[middle1] + sorted_data[middle2]) / 2
    else:
        middle = n // 2
        return sorted_data[middle]