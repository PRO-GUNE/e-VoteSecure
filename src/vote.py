from helpers import find_large_prime, modular_exponentiation, gcd, extended_gcd

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

print("------------ Prime Numbers ------------")
print("p:", p)
print("q:", q)
print("---------------------------------------")
print("Prime composite (n)                  :", n)
print("Euler totient function of n (phi_n)  :", phi_n)
print("---------------------------------------")
print("Secret key (d)                       :", d)
print(f"Public key (e,n)                     : {e}, {n}")


def blind_vote(k, m):
    # Generate blinding factor
    bf = modular_exponentiation(k, e, n)
    print("Blinding factor:", bf)

    # Blinding the message
    m1 = (m * bf) % n
    print("Blinded message:", m1)
    return m1


def blind_sign(m1):
    # Signing the blinded message
    s1 = modular_exponentiation(m1, d, n)
    print("Signature on blinded message:", s1)
    return s1


def decode_vote(s, k):
    # Unblind the message
    m2 = (s * extended_gcd(k, n)[1]) % n
    print("Unblinded message:", m2)

    # Decrypt the unblinded message
    m = modular_exponentiation(m2, e, n)
    print("Decrypted signature:", m)

    return m
