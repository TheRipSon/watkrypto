import os

def generate_key(message_length):
    """Generate a random key of the same length as the message."""
    return os.urandom(message_length)

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
message = "HELLO OTP!"
key = generate_key(len(message))  # Generate a random key
print(f"Key: {key.hex()}")  # Display the key in hex format

encrypted_message = encrypt(message, key)
print(f"Encrypted: {encrypted_message.hex()}")  # Display the ciphertext

decrypted_message = decrypt(encrypted_message, key)
print(f"Decrypted: {decrypted_message}")


'''
Key: 373b523aed0bb0c32fa3
Encrypted: 7f7e1e76a22bff977f82
Decrypted: HELLO OTP!
'''