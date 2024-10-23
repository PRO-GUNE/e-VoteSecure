from utils.helpers import modular_exponentiation, extended_gcd
from client.config import trusted_authority_public_key_url
import requests

# Get the public key from the trusted authority
response = requests.get(trusted_authority_public_key_url)
if response.status_code == 200:
    public_key = response.json()["public_key"]
    e, n = public_key
else:
    print("Error getting public key from trusted authority")
    exit(1)


def blind_vote(k, m):
    # Generate blinding factor
    bf = modular_exponentiation(k, e, n)
    print("Blinding factor:", bf)

    # Blinding the message
    m1 = (m * bf) % n
    print("Blinded message:", m1)
    return m1


def unblind_signature(s, k):
    # Unblind the signature
    s2 = (s * extended_gcd(k, n)[1]) % n
    print("Unblinded signature:", s2)
    return s2
