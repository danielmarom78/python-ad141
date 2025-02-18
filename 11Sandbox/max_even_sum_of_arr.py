def max_even_sum(arr, k):
    """Problem Statement
    Given an array of integers, select exactly k elements such that their sum is maximum and even.

    Approach
    Sort the array in descending order – This helps in selecting the largest possible k elements to maximize the sum.
    Check if the sum of the top k elements is even:
    If yes, return it.
    If no, try adjusting the sum to make it even.
    To make an odd sum even, we either:
    Remove the smallest odd number from our selection and add the largest even number (if available).
    Remove the smallest even number and add the largest odd number (if available).
    Return the best possible even sum."""

    arr.sort(reverse=True)  # Sort array in descending order
    total = sum(arr[:k])  # Get the sum of the largest k elements

    if total % 2 == 0:
        return total  # If already even, return the sum

    # Finding the smallest odd and even numbers in the first k elements
    odd_min_inside = next((x for x in reversed(arr[:k]) if x % 2 != 0), float('inf'))
    even_min_inside = next((x for x in reversed(arr[:k]) if x % 2 == 0), float('inf'))

    # Finding the largest odd and even numbers outside the first k elements
    odd_max_outside = next((x for x in arr[k:] if x % 2 != 0), float('-inf'))
    even_max_outside = next((x for x in arr[k:] if x % 2 == 0), float('-inf'))

    # Try swapping one element to make sum even
    replace_even = total - even_min_inside + odd_max_outside if even_min_inside < float(
        'inf') and odd_max_outside > float('-inf') else float('-inf')
    replace_odd = total - odd_min_inside + even_max_outside if odd_min_inside < float(
        'inf') and even_max_outside > float('-inf') else float('-inf')

    # Return the best valid even sum, or -1 if no valid sum exists
    max_sum = max(replace_even, replace_odd)
    return max_sum if max_sum != float('-inf') else -1

# Example usage:
arr = [4, 2, 1, -1, -7]
k = 3
print(max_even_sum(arr, k))