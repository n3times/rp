# Computes num_digits of e.
# The result is scaled up by 10**num_digits for digit precision.
def e(num_digits):
    # term starts as 10^num_digits to shift decimal precision
    term = 10 ** num_digits  # first term: 1 (scaled up)
    result = term
    k = 1
    while term > 0:
        term //= k           # move to next term: 1/k!
        result += term
        k += 1
    return result

# Compute a few digits extra to guard against truncation errors
num_digits = 116000
guard_digits = 10
print(e(num_digits + guard_digits) // 10 ** guard_digits)
