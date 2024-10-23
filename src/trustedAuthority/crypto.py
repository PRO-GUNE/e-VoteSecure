from utils.helpers import find_large_prime, modular_exponentiation, gcd, extended_gcd

# Generate two large prime numbers p and q
p = find_large_prime(32)
q = find_large_prime(32)
e = 65537

# Calculate n = p * q
n = p * q
# Euler totient function of n
phi_n = (p - 1) * (q - 1)

# Ensure e and phi_n are coprime and e is less than phi_n
assert gcd(phi_n, e) == 1 and e < phi_n, "e and phi_n are not coprime"

# Find the modular multiplicative inverse of e mod phi_n
d = extended_gcd(e, phi_n)[1] % phi_n

# Public key: (e, n)
public_key = (e, n)


# Encrypt the message
def encrypt_message(m):
    # Encrypting the message
    c = modular_exponentiation(m, e, n)
    print("Encrypted message:", c)
    return c


# Decrypt the message
def decrypt_message(c):
    # Decrypting the message
    m = modular_exponentiation(c, d, n)
    print("Decrypted message:", m)
    return m


def blind_sign(m1):
    # Signing the blinded message
    s1 = modular_exponentiation(m1, d, n)
    print("Signature on blinded message:", s1)
    return s1


def decrypt_signature(s1):
    # Decrypting the signature
    s = modular_exponentiation(s1, e, n)
    print("Decrypted signature:", s)
    return s
