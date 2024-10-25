import random
from helpers import generate_keypair

# Function to encrypt a vote using the public key
def encrypt_vote(vote, public_key):
    e, n = public_key
    encrypted_vote = pow(vote, e, n)  # RSA encryption: c = m^e mod n
    return encrypted_vote

# Function to decrypt a vote using the private key
def decrypt_vote(encrypted_vote, private_key):
    d, n = private_key
    decrypted_vote = pow(encrypted_vote, d, n)  # RSA decryption: m = c^d mod n
    return decrypted_vote

# Mix server function: decrypts and shuffles votes while keeping the vote's ID
def mix_server(encrypted_votes, private_key):
    # Decrypt only the votes, keep the IDs
    decrypted_votes_with_ids = [(vote_id, decrypt_vote(vote, private_key)) for vote_id, vote in encrypted_votes]
    random.shuffle(decrypted_votes_with_ids)  # Shuffle the votes
    return decrypted_votes_with_ids

# Mixnet function processes votes from the vote pool
def mixnet(vote_pool):
    
    votes = [(vote['id'], int(vote['signed_vote']), int(vote['counted'])) for vote in vote_pool]

    # Generate RSA key pairs for 3 mix servers (adjust key size to 2048 bits for real use)
    private_key_1, public_key_1 = generate_keypair()
    private_key_2, public_key_2 = generate_keypair()
    private_key_3, public_key_3 = generate_keypair()

    # Encrypt votes with all mix server public keys (layered encryption)
    encrypted_votes = [(vote_id, encrypt_vote(vote, public_key_1)) for vote_id, vote in votes]
    encrypted_votes = [(vote_id, encrypt_vote(vote, public_key_2)) for vote_id, vote in encrypted_votes]
    encrypted_votes = [(vote_id, encrypt_vote(vote, public_key_3)) for vote_id, vote in encrypted_votes]

    # Mix server 1 decrypts with its private key and shuffles the votes
    partially_decrypted_votes = mix_server(encrypted_votes, private_key_3)

    # Mix server 2 decrypts and shuffles the votes
    partially_decrypted_votes = mix_server(partially_decrypted_votes, private_key_2)

    # Mix server 3 decrypts and shuffles the votes
    final_votes_with_ids = mix_server(partially_decrypted_votes, private_key_1)

    return final_votes_with_ids

# Example test
def test_mixnet():
   
    vote_pool = [
        {'id': 1, 'signed_vote': str(32317006), 'counted': False},
        {'id': 2, 'signed_vote': str(43516384), 'counted': False},
        {'id': 3, 'signed_vote': str(95886922), 'counted': False},
        {'id': 4, 'signed_vote': str(63425595), 'counted': True}
    ]

    print("Original vote pool:")
    for vote in vote_pool:
        print(f"Vote ID: {vote['id']}, Signed Vote: {vote['signed_vote']}, Counted: {vote['counted']}")

    # Run the mixnet
    mixed_votes = mixnet(vote_pool)

    print("\nMixed and Decrypted votes:")
    for vote_id, decrypted_vote in mixed_votes:
        print(f"Vote ID: {vote_id}, Decrypted Vote: {decrypted_vote}, Counted: {vote['counted']}")

# Run the test
test_mixnet()
