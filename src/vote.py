from helpers import find_large_prime, modular_exponentiation


def blind_vote(m, e, n):
    # Generate blinding factor
    k = find_large_prime(32)
    bf = modular_exponentiation(k, e, n)
    print("Blinding factor:", bf)

    # Blinding the message
    m1 = (m * bf) % n
    print("Blinded message:", m1)

    # Signing the blinded message
    s1 = modular_exponentiation(m1, d, n)
    print("Signature on blinded message:", s1)
