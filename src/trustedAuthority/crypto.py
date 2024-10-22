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

print("------------ Prime Numbers ------------")
print("p:", p)
print("q:", q)
print("---------------------------------------")
print("Prime composite (n)                  :", n)
print("Euler totient function of n (phi_n)  :", phi_n)
print("---------------------------------------")
print("Secret key (d)                       :", d)
print(f"Public key (e,n)                     : {e}, {n}")


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
