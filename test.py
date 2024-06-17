def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def calculate_primes(n):
    primes = []
    for number in range(2, n + 1):
        if is_prime(number):
            primes.append(number)
    return primes

def sum_natural_numbers(n):
    total = 0
    for i in range(1, n + 1):
        total += i  
    return total

print(calculate_primes(1000))  # This will be slow for larger values of n




def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))





def fibonacci(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence

print(fibonacci(10))



def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))



def sum_of_squares(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

print(sum_of_squares(10))




def merge_lists(list1, list2):
    merged_list = []
    while list1 and list2:
        if list1[0] < list2[0]:
            merged_list.append(list1.pop(0))
        else:
            merged_list.append(list2.pop(0))
    merged_list.extend(list1 or list2)
    return merged_list

print(merge_lists([1, 3, 5], [2, 4, 6]))
