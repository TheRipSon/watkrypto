def generate_vigenere_key(seed_key, message_length):
    """Generate a Vigenère key that matches the length of the message."""
    key = seed_key
    while len(key) < message_length:
        key += seed_key  # Repeat the seed key until it matches the message length
    return key[:message_length]  # Cut the key to the exact length of the message

def vigenere_encrypt(message, key):
    """Encrypt a message using the Vigenère cipher."""
    message = message.lower()  # Convert to lowercase for simplicity
    key = key.lower()

    encrypted_message = []
    key_index = 0

    for char in message:
        if char.isalpha():
            message_index = ord(char) - ord('a')
            key_index = ord(key[key_index % len(key)]) - ord('a')
            encrypted_char = chr((message_index + key_index) % 26 + ord('a'))
            encrypted_message.append(encrypted_char)
            key_index += 1
        else:
            encrypted_message.append(char)

    return ''.join(encrypted_message)

def vigenere_decrypt(encrypted_message, key):
    """Decrypt a message using the Vigenère cipher."""
    encrypted_message = encrypted_message.lower()
    key = key.lower()

    decrypted_message = []
    key_index = 0

    for char in encrypted_message:
        if char.isalpha():
            encrypted_index = ord(char) - ord('a')
            key_index = ord(key[key_index % len(key)]) - ord('a')
            decrypted_char = chr((encrypted_index - key_index + 26) % 26 + ord('a'))
            decrypted_message.append(decrypted_char)
            key_index += 1
        else:
            decrypted_message.append(char)

    return ''.join(decrypted_message)

# Example Usage
message = "HELLO OTP!"
seed_key = "abc"  # The key used to generate the Vigenère cipher key

# Generate the Vigenère key based on the seed key and message length
generated_key = generate_vigenere_key(seed_key, len(message))

# Encrypting the message using the generated key
encrypted_message = vigenere_encrypt(message, generated_key)
print(f"Generated Key: {generated_key}")  # The generated key for the message
print(f"Encrypted: {encrypted_message}")

# Decrypting the message back to the original
decrypted_message = vigenere_decrypt(encrypted_message, generated_key)
print(f"Decrypted: {decrypted_message}")
