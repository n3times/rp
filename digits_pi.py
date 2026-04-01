# Computes the arctan of 1/n, where n is an integer.
def arctan_inverse(n, num_digits):
    result = 0
    term = 10 ** num_digits // n  # first term: 1/n
    sign = 1
    k = 1
    while term != 0:
        result += sign * term // k
        term //= n * n           # move to next term: x^(2k+1)
        sign = -sign
        k += 2
    return result

# A Machin-like formula for pi, easy to derive
def pi(num_digits):
    return 4 * (arctan_inverse(2, num_digits) + 
                arctan_inverse(3, num_digits))

# Compute a few digits extra to guard against truncation errors
num_digits = 1000
guard_digits = 10
print(pi(num_digits + guard_digits) // 10 ** guard_digits)
