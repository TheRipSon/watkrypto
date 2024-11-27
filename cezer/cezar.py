import matplotlib.pyplot as plt
from collections import Counter

def caesar_cipher(text, shift, encrypt=True):
    """
    Apply Caesar Cipher to the given text.

    :param text: The input string to be encrypted/decrypted
    :param shift: The number of positions to shift
    :param encrypt: True for encryption, False for decryption
    :return: The encrypted/decrypted string
    """
    if not encrypt:
        shift = -shift  # Reverse shift for decryption

    result = []
    for char in text:
        if char.isprintable():
            # Shift character by converting to its Unicode code point
            new_char = chr((ord(char) + shift) % 1114112)  # Modulus for UTF-8 range
            result.append(new_char)
        else:
            # Append non-printable characters as is
            result.append(char)
    
    return ''.join(result)

def frequency_table(text):
    """
    Generate a frequency table for characters in the given text.

    :param text: The input string
    :return: A dictionary of character frequencies
    """
    return Counter(text)

def plot_histogram(freq_table, title):
    """
    Plot a histogram from the frequency table.

    :param freq_table: A dictionary of character frequencies
    :param title: The title of the histogram
    """
    characters = list(freq_table.keys())
    frequencies = list(freq_table.values())

    plt.figure(figsize=(12, 6))
    plt.bar(characters, frequencies, color='skyblue', edgecolor='black')
    plt.xlabel('Characters')
    plt.ylabel('Frequencies')
    plt.title(title)
    plt.xticks(rotation=45, fontsize=8)
    plt.tight_layout()
    plt.show()
    plt.savefig(title)

# Input message
message = ("En criptografía, el cifrado César, también conocido como cifrado por desplazamiento, "
           "código de César o desplazamiento de César, es una de las técnicas de cifrado más simples "
           "y más usadas. Es un tipo de cifrado por sustitución en el que una letra en el texto original "
           "es reemplazada por otra letra que se encuentra un número fijo de posiciones más adelante en el alfabeto. "
           "Por ejemplo, con un desplazamiento de 3, la A sería sustituida por la D (situada 3 lugares a la derecha de la A), "
           "la B sería reemplazada por la E, etc. Este método debe su nombre a Julio César, que lo usaba para comunicarse "
           "con sus generales.")

# Caesar Cipher shift value
shift_value = 3

# Frequency Table for Original Message
original_freq = frequency_table(message)

# Encrypt the message
encrypted = caesar_cipher(message, shift_value)

# Frequency Table for Encrypted Message
encrypted_freq = frequency_table(encrypted)

# Decrypt to verify
decrypted = caesar_cipher(encrypted, shift_value, encrypt=False)

# Print Results
print("Original Frequency Table:")
for char, freq in original_freq.items():
    print(f"'{char}': \t{freq} \t ORD value: {ord(char)}")

print("\nEncrypted Message:")
print(encrypted)

print("\nEncrypted Frequency Table:")
for char, freq in encrypted_freq.items():
    print(f"'{char}': \t{freq} \t ORD value: {ord(char)}")

print("\nDecrypted Message:")
print(decrypted)

# Plot Histograms
plot_histogram(original_freq, "Character Frequency in Original Message")
plot_histogram(encrypted_freq, "Character Frequency in Encrypted Message")
