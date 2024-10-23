import random
from utils.helpers import generate_keypair

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

# Mix server function: decrypts and shuffles votes
def mix_server(encrypted_votes, private_key):
    decrypted_votes = [decrypt_vote(vote, private_key) for vote in encrypted_votes]
    random.shuffle(decrypted_votes)  # Shuffle the votes
    return decrypted_votes

# Example usage of the mixnet with 3 mix servers
def mixnet(votes):
    # Generate RSA key pairs for 3 mix servers
    private_key_1, public_key_1 = generate_keypair()
    private_key_2, public_key_2 = generate_keypair()
    private_key_3, public_key_3 = generate_keypair()

    #Encrypt votes with all mix server public keys (layered encryption)
    encrypted_votes = [encrypt_vote(vote, public_key_1) for vote in votes]
    encrypted_votes = [encrypt_vote(vote, public_key_2) for vote in encrypted_votes]
    encrypted_votes = [encrypt_vote(vote, public_key_3) for vote in encrypted_votes]

    #Mix server 1 decrypts with its private key and shuffles the votes
    partially_decrypted_votes = mix_server(encrypted_votes, private_key_3)

    #Mix server 2 decrypts and shuffles the votes
    partially_decrypted_votes = mix_server(partially_decrypted_votes, private_key_2)

    # Mix server 3 decrypts and shuffles the votes
    final_votes = mix_server(partially_decrypted_votes, private_key_1)

    return final_votes

# # Example 
# if __name__ == "__main__":
#     votes = [1312321312312312, 22312312312312312, 33131231241341231]
#     print("Original votes:", votes)

#     # Process votes through mixnet
#     anonymized_votes = mixnet(votes)

#     print("\nAnonymized (shuffled) votes:", anonymized_votes)
