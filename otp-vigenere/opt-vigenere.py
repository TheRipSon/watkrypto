import os

def generate_key(message_length):
    """Generate a random key of the same length as the message."""
    return os.urandom(message_length)

def extend_key(key, message_length):
    """Extend or truncate the key to match the message length."""
    return (key * (message_length // len(key)) + key[:message_length % len(key)])

def encrypt(message, key, method='XOR'):
    """Encrypt the message using the key."""
    message_bytes = message.encode('utf-8')
    if method == 'XOR':
        encrypted_bytes = bytes([m ^ k for m, k in zip(message_bytes, key)]) # XOR operation
    elif method == 'ADD':
        encrypted_bytes = bytes([(m + k) % 256 for m, k in zip(message_bytes, key)])  # Addition with overflow handling
    else:
        return -1
    return encrypted_bytes

def decrypt(encrypted_message, key, method='XOR'):
    """Decrypt the encrypted message using the key."""
    if method == 'XOR':
        decrypted_bytes = bytes([e ^ k for e, k in zip(encrypted_message, key)]) # XOR operation
    elif method == 'ADD':
        decrypted_bytes = bytes([(e - k) % 256 for e, k in zip(encrypted_message, key)])  # Subtraction to reverse encryption
    else:
        return -1
    return decrypted_bytes.decode('utf-8')

# Example Usage
message = """
As they rounded a bend in the path that ran beside the river, Lara recognized the silhouette of a fig tree atop a nearby hill. The weather was hot and the days were long. The fig tree was in full leaf, but not yet bearing fruit.
Soon Lara spotted other landmarks—an outcropping of limestone beside the path that had a silhouette like a man's face, a marshy spot beside the river where the waterfowl were easily startled, a tall tree that looked like a man with his arms upraised. They were drawing near to the place where there was an island in the river. The island was a good spot to make camp. They would sleep on the island tonight.
Lara had been back and forth along the river path many times in her short life. Her people had not created the path—it had always been there, like the river—but their deerskin-shod feet and the wooden wheels of their handcarts kept the path well worn. Lara's people were salt traders, and their livelihood took them on a continual journey.
At the mouth of the river, the little group of half a dozen intermingled families gathered salt from the great salt beds beside the sea. They groomed and sifted the salt and loaded it into handcarts. When the carts were full, most of the group would stay behind, taking shelter amid rocks and simple lean-tos, while a band of fifteen or so of the heartier members set out on the path that ran alongside the river.
With their precious cargo of salt, the travelers crossed the coastal lowlands and traveled toward the mountains. But Lara's people never reached the mountaintops; they traveled only as far as the foothills.
"""

key = generate_key(25)  # Generate a random key
print(f"Key: {key.hex()}")  # Display the key in hex format

extended_key = extend_key(key,len(message))

encrypted_message = encrypt(message, extended_key)

decrypted_message = decrypt(encrypted_message, extended_key)

with open('encrypted.bin', 'wb') as file:
    file.write(encrypted_message)