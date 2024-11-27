import os

def generate_key(key_length):
    """Generate a random key of the specified length."""
    return os.urandom(key_length)

def extend_key(key, message_length):
    """Extend or truncate the key to match the message length."""
    return (key * (message_length // len(key)) + key[:message_length % len(key)])

def encrypt(message, key, method='XOR'):
    """Encrypt the message using the key."""
    message_bytes = message.encode('utf-8')

    if method == 'XOR':
        encrypted_bytes = bytes([m ^ k for m, k in zip(message_bytes, key)])  # XOR operation
    elif method == 'ADD':
        encrypted_bytes = bytes([(m + k) % 256 for m, k in zip(message_bytes, key)])  # Addition with overflow handling
    else:
        return -1
    return encrypted_bytes

def decrypt(encrypted_message, key, method='XOR'):
    """Decrypt the encrypted message using the key."""
    key = extend_key(key, len(encrypted_message))  # Extend the key to match the message length
    if method == 'XOR':
        decrypted_bytes = bytes([e ^ k for e, k in zip(encrypted_message, key)])  # XOR operation
    elif method == 'ADD':
        decrypted_bytes = bytes([(e - k) % 256 for e, k in zip(encrypted_message, key)])  # Subtraction to reverse encryption
    else:
        return -1
    return decrypted_bytes.decode('utf-8')


# Example Usage
message = "HELLO OTP!"
short_key = generate_key(3)  # Generate a random key with a shorter length
print(f"Short Key: {short_key.hex()}")  # Display the short key in hex format

encrypted_message = encrypt(message, short_key)
print(f"Encrypted: {encrypted_message.hex()}")  # Display the ciphertext

decrypted_message = decrypt(encrypted_message, short_key)
print(f"Decrypted: {decrypted_message}")  # Display the decrypted message


'''
Short Key: 373b52
Encrypted: 7f7e1e76a22bff977f82
Decrypted: HELLO OTP!
'''
