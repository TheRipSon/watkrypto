import os

def generate_key(length):
    """Generate a random key of the given length."""
    return os.urandom(length)

def encrypt_utf8(message, key):
    """Encrypt a UTF-8 encoded message safely."""
    message_bytes = message.encode('utf-8')
    if len(key) < len(message_bytes):
        raise ValueError("Key must be at least as long as the message.")
    encrypted = bytes([m ^ k for m, k in zip(message_bytes, key)])
    return encrypted

def decrypt_utf8(ciphertext, key):
    """Decrypt the ciphertext and ensure valid UTF-8 output."""
    if len(key) < len(ciphertext):
        raise ValueError("Key must be at least as long as the ciphertext.")
    decrypted_bytes = bytes([c ^ k for c, k in zip(ciphertext, key)])
    return decrypted_bytes.decode('utf-8')

# Example Usage
message = "Hello, UTF-8 OTP!"  # Regular UTF-8 string
key = generate_key(len(message.encode('utf-8')))

ciphertext = encrypt_utf8(message, key)
print("Ciphertext:", ciphertext)

decrypted_message = decrypt_utf8(ciphertext, key)
print("Decrypted:", decrypted_message)
