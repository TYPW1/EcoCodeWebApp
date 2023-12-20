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


print(calculate_primes(1000))  # This will be slow for larger values of n




def sum_natural_numbers(n):
total = 0
for i in range(1, n + 1):
total += i
return total