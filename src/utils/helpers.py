import random


# Function to perform Miller-Rabin primality test
def miller_rabin_test(n, k=5):
    # If n is 2 or 3, it's prime
    if n == 2 or n == 3:
        return True
    # If n is less than 2 or even, it's not prime
    if n <= 1 or n % 2 == 0:
        return False

    # Write n-1 as d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Perform k rounds of Miller-Rabin test
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Function to find a large prime number using Miller-Rabin
def find_large_prime(bits):
    while True:
        # Generate a random number with the specified bit length
        p = random.getrandbits(bits)
        # Ensure p is odd
        p |= (1 << bits - 1) | 1
        # Check if p is prime using Miller-Rabin test
        if miller_rabin_test(p):
            return p


# Function for modular exponentiation
def modular_exponentiation(g, s, p):
    result = 1

    # Update g to be within the modulus
    g = g % p

    while s > 0:
        # If s is odd, multiply g with the result
        if s % 2 == 1:
            result = (result * g) % p

        # s must be even now
        s = s // 2
        g = (g * g) % p  # Square g
    return result


# Function to get the greatest common divisor of two numbers
def gcd(a, b):
    if (a < 0) or (b < 0) or (a < b):
        print("Invalid input")
        return

    while b != 0:
        r = a % b
        a = b
        b = r

    return a


# Function for the extended Euclidean algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - y * (a // b)
    
#generate key-pairs
def generate_keypair(bits=32):
    # Generate two large prime numbers p and q
    p = find_large_prime(bits)
    q = find_large_prime(bits)
    e = 65537

    # Calculate n = p * q
    n = p * q
    # Euler's totient function of n
    phi_n = (p - 1) * (q - 1)

    # Ensure e and phi_n are coprime and e is less than phi_n
    assert gcd(phi_n, e) == 1 and e < phi_n, "e and phi_n are not coprime"

    # Find the modular multiplicative inverse of e mod phi_n
    d = extended_gcd(e, phi_n)[1] % phi_n
    private_key = (d, n)  # private key (d, n)
    public_key = (e, n)   # public key (e, n)
    
    return private_key, public_key
