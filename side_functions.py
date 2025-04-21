import decimal
from decimal import Decimal, getcontext

def load_pi_from_file(filename):
    with open(filename, 'r') as f:
        pi_string = f.read().replace("\n", "").replace(" ", "")
    return Decimal(pi_string)


# Confronto cifra per cifra
def count_matching_digits(approx_str, true_str):
    count = 0
    for s, t in zip(approx_str, true_str):
        if s == t:
            count += 1
        else:
            break
    return count

