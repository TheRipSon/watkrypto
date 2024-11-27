import matplotlib.pyplot as plt
from collections import Counter

# Spanish letter probabilities
# https://www.sttmedia.com/characterfrequency-spanish
spanish_frequencies = {
    'A': 11.72, 'Á': 0.44, 'B': 1.49, 'C': 3.87, 'D': 4.67, 'E': 13.72, 
    'É': 0.36, 'F': 0.69, 'G': 1.00, 'H': 1.18, 'I': 5.28, 'Í': 0.70, 
    'J': 0.52, 'K': 0.11, 'L': 5.24, 'M': 3.08, 'N': 6.83, 'Ñ': 0.17, 
    'O': 8.44, 'Ó': 0.76, 'P': 2.89, 'Q': 1.11, 'R': 6.41, 'S': 7.20, 
    'T': 4.60, 'U': 4.55, 'Ü': 0.02, 'Ú': 0.12, 'V': 1.05, 'W': 0.04, 
    'X': 0.14, 'Y': 1.09, 'Z': 0.47
}

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
    Generate a frequency table for characters in the given text,
    removing the most frequent character (likely a space).
    
    :param text: The input string
    :return: A dictionary of character frequencies with the most frequent character removed
    """
    freq = Counter(text)
    # Identify the most frequent character
    most_frequent = freq.most_common(1)[0][0]  # Get the most common  (its space my spanish_frequencies dosnt have it)
    # Remove the most frequent character
    if most_frequent in freq:
        del freq[most_frequent]
    return freq


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
message = '''
En criptografía, el cifrado César, también conocido como cifrado por desplazamiento, código de César o desplazamiento de César, es una de las técnicas de cifrado más simples y más usadas. Es un tipo de cifrado por sustitución en el que una letra en el texto original es reemplazada por otra letra que se encuentra un número fijo de posiciones más adelante en el alfabeto. Por ejemplo, con un desplazamiento de 3, la A sería sustituida por la D (situada 3 lugares a la derecha de la A), la B sería reemplazada por la E, etc. Este método debe su nombre a Julio César, que lo usaba para comunicarse con sus generales.

El cifrado César muchas veces puede formar parte de sistemas más complejos de codificación, como el cifrado Vigenère, e incluso tiene aplicación en el sistema ROT13. Como todos los cifrados de sustitución alfabética simple, el cifrado César se descifra con facilidad y en la práctica no ofrece mucha seguridad en la comunicación. 
'''


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
plot_histogram(encrypted_freq, "Character Frequency in Encrypted Message")
plot_histogram(spanish_frequencies, "Spanish Letter Probabilities")

'''
Result images shows shitft 2 most freq letters in spanish are E and A in histogram of message when we get rid of space are D and H so:
D-A=3
H-E=3
so shift is 3
'''