import collections

def read_encrypted_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def calculate_ic(text):
    """Calculate the Index of Coincidence for a given text."""
    N = len(text)
    frequency = collections.Counter(text)
    ic = 0.0
    for count in frequency.values():
        ic += count * (count - 1)
    if N <= 1:
        return 0
    else:
        return ic / (N * (N - 1))

def estimate_key_length(encrypted_text, max_key_length):
    """Estimate the key length using the Index of Coincidence."""
    ics = []
    for key_length in range(1, max_key_length + 1):
        ic_total = 0.0
        for i in range(key_length):
            # Extract every key_length-th byte starting from position i
            subtext = encrypted_text[i::key_length]
            ic = calculate_ic(subtext)
            ic_total += ic
        average_ic = ic_total / key_length
        ics.append((key_length, average_ic))
    return ics

def chi_squared_statistic(observed_freq, expected_freq, total_count):
    """Calculates the chi-squared statistic."""
    chi_squared = 0.0
    for char in expected_freq:
        observed = observed_freq.get(char, 0)
        expected = expected_freq[char] * total_count / 100
        chi_squared += ((observed - expected) ** 2) / expected if expected > 0 else 0
    return chi_squared

def get_english_letter_frequency():
    """Returns a dictionary with English letter frequencies."""
    frequency = {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253,
        'e': 12.702,'f': 2.228, 'g': 2.015, 'h': 6.094,
        'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025,
        'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929,
        'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
        'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
        'y': 1.974, 'z': 0.074, ' ': 13.000 
    }
    return frequency

def frequency_analysis(block):
    """Performs frequency analysis on a block to find the most probable key byte."""
    english_freq = get_english_letter_frequency()
    min_chi_squared = None
    likely_key_byte = None

    for key_candidate in range(256):
        decrypted_block = bytes([b ^ key_candidate for b in block])
        decrypted_text = ''.join([chr(b) if 32 <= b <= 126 else ' ' for b in decrypted_block])
        decrypted_text = decrypted_text.lower()
        total_chars = len(decrypted_text)
        if total_chars == 0:
            continue

        # Count frequency of each character
        observed_freq = collections.Counter(decrypted_text)

        # Calculate chi-squared statistic
        chi_squared = chi_squared_statistic(observed_freq, english_freq, total_chars)

        if min_chi_squared is None or chi_squared < min_chi_squared:
            min_chi_squared = chi_squared
            likely_key_byte = key_candidate

    return likely_key_byte

def recover_key(encrypted_text, key_length):
    """Recovers the key used to encrypt the text."""
    key = bytearray()
    for i in range(key_length):
        block = encrypted_text[i::key_length]
        key_byte = frequency_analysis(block)
        key.append(key_byte)
    return bytes(key)

def decrypt_with_key(encrypted_text, key):
    """Decrypts the encrypted text using the recovered key."""
    extended_key = (key * (len(encrypted_text) // len(key))) + key[:len(encrypted_text) % len(key)]
    decrypted_bytes = bytes([e ^ k for e, k in zip(encrypted_text, extended_key)])
    return decrypted_bytes.decode('utf-8', errors='replace')


def main():
    encrypted_text = read_encrypted_file('encrypted.bin')
    max_key_length = 60  # Adjust based on expected key length range
    ics = estimate_key_length(encrypted_text, max_key_length)
    print("Key Length Estimation using Index of Coincidence:")
    for key_length, ic in ics:
        print(f"Key Length: {key_length}, Average IC: {ic:.4f}")

    # Identify the key length with the highest average IC
    likely_key_length = max(ics, key=lambda x: x[1])[0]
    print(f"\nMost likely key length: {likely_key_length}")

    key_length = likely_key_length

    print(f"Recovering key of length {key_length}...")
    recovered_key = recover_key(encrypted_text, key_length)
    print(f"Recovered Key (hex): {recovered_key.hex()}")

    decrypted_message = decrypt_with_key(encrypted_text, recovered_key)
    print("\nDecrypted Message:")
    print(decrypted_message)


if __name__ == "__main__":
    main()

'''
Estimated key is very close to orginal.
Incresing message size give better results.
'''


'''
(venv) user@user-HP-EliteBook-845-14-inch-G9-Notebook-PC:~/code/watKrypto/otp-vigenere$ python opt-vigenere.py 
Key: aa06b3a6425d91c77f2cf94567e70d323aa200dfd714d9b660
(venv) user@user-HP-EliteBook-845-14-inch-G9-Notebook-PC:~/code/watKrypto/otp-vigenere$ python cryptoanalysis.py 
Key Length Estimation using Index of Coincidence:
Key Length: 1, Average IC: 0.0064
Key Length: 2, Average IC: 0.0064
Key Length: 3, Average IC: 0.0063
Key Length: 4, Average IC: 0.0063
Key Length: 5, Average IC: 0.0178
Key Length: 6, Average IC: 0.0062
Key Length: 7, Average IC: 0.0062
Key Length: 8, Average IC: 0.0063
Key Length: 9, Average IC: 0.0064
Key Length: 10, Average IC: 0.0175
Key Length: 11, Average IC: 0.0062
Key Length: 12, Average IC: 0.0059
Key Length: 13, Average IC: 0.0064
Key Length: 14, Average IC: 0.0059
Key Length: 15, Average IC: 0.0175
Key Length: 16, Average IC: 0.0061
Key Length: 17, Average IC: 0.0060
Key Length: 18, Average IC: 0.0059
Key Length: 19, Average IC: 0.0061
Key Length: 20, Average IC: 0.0172
Key Length: 21, Average IC: 0.0059
Key Length: 22, Average IC: 0.0061
Key Length: 23, Average IC: 0.0062
Key Length: 24, Average IC: 0.0059
Key Length: 25, Average IC: 0.0752
Key Length: 26, Average IC: 0.0061
Key Length: 27, Average IC: 0.0063
Key Length: 28, Average IC: 0.0057
Key Length: 29, Average IC: 0.0057
Key Length: 30, Average IC: 0.0169
Key Length: 31, Average IC: 0.0056
Key Length: 32, Average IC: 0.0058
Key Length: 33, Average IC: 0.0058
Key Length: 34, Average IC: 0.0056
Key Length: 35, Average IC: 0.0169
Key Length: 36, Average IC: 0.0056
Key Length: 37, Average IC: 0.0056
Key Length: 38, Average IC: 0.0058
Key Length: 39, Average IC: 0.0057
Key Length: 40, Average IC: 0.0173
Key Length: 41, Average IC: 0.0058
Key Length: 42, Average IC: 0.0053
Key Length: 43, Average IC: 0.0054
Key Length: 44, Average IC: 0.0057
Key Length: 45, Average IC: 0.0176
Key Length: 46, Average IC: 0.0058
Key Length: 47, Average IC: 0.0056
Key Length: 48, Average IC: 0.0052
Key Length: 49, Average IC: 0.0058
Key Length: 50, Average IC: 0.0740
Key Length: 51, Average IC: 0.0055
Key Length: 52, Average IC: 0.0055
Key Length: 53, Average IC: 0.0061
Key Length: 54, Average IC: 0.0055
Key Length: 55, Average IC: 0.0167
Key Length: 56, Average IC: 0.0053
Key Length: 57, Average IC: 0.0051
Key Length: 58, Average IC: 0.0050
Key Length: 59, Average IC: 0.0051
Key Length: 60, Average IC: 0.0161

Most likely key length: 25
Recovering key of length 25...
Recovered Key (hex): aa06b3a6425d91c75f2cf94567e70d323aa200dfd714d9b640

Decrypted Message:

As theyrounded a bend In the paTh that ran besiDe the riVer, Lara recognIzed the Silhouette of a Fig tree Atop a nearby hiLl. The wEather was hot aNd the daYs were long. ThE fig treE was in full leAf, but nOt yet bearing fRuit.
SooN Lara spotted oTher landMarks—an outcrOpping oflimestone besidE the patH that had a silHouette lIke a man's face
a marshY spot beside thE river wHere the waterfoWl were eAsily startled, A tall trEe that looked lIke a manwith his arms uPraised. they were drawinG near tothe place wherethere waS an island in tHe river.The island was A good spOt to make camp.They wouLd sleep on the Island toNight.
Lara had Been backand forth alongthe riveR path many timeS in her Short life. Her People haD not created thE path—It had always beEn there,like the river⠔but theIr deerskin-shodfeet andthe wooden wheeLs of theIr handcarts kepT the patH well worn. LarA's peoplE were salt tradErs, and Their livelihoodtook theM on a continualjourney.*At the mouth ofthe riveR, the little grOup of haLf a dozen interMingled fAmilies gatheredsalt froM the great saltbeds besIde the sea. TheY groomedand sifted the Salt and Loaded it into hAndcarts.When the carts Were full
                                                                                                                                          most of the grOup wouldstay behind, taKing shelTer amid rocks aNd simplelean-tos, whilea band oF fifteen or so Of the heArtier members sEt out onthe path that rAn alongsIde the river.
WIth theirprecious cargo Of salt, The travelers crOssed thecoastal lowlandS and traVeled toward themountainS. But Lara's peOple neveR reached the moUntaintopS; they traveledonly as Far as the foothIlls. ManY people lived iN the forEsts and grassy Meadows oF the foothills,gatheredin small villagEs. In reTurn for salt, tHese peopLe would give LaRa's peopLe dried meat, aNimal skiNs, cloth spun fRom wool,clay pots, needLes and sCraping tools caRved frombone, and littlE toys maDe of wood.
TheiR barteriNg done, Lara anD her peoPle would travelback dowN the river pathto the sEa. The cycle woUld beginagain.
It had aLways beeN like this. LarA knew noother life. Shetraveledback and forth,up and dOwn the river paTh. No siNgle place was hOme. She Liked the seasidE, where There was alwaysfish to Eat, and the genTle lappiNg of the waves Lulled heR to sleep at niGht. She Was less fond ofthe footHills, where thepath greW steep, the nigHts couldbe cold, and viEws of grEat distances maDe her diZzy. She felt unEasy in tHe villages, andwas ofteN shy around strAngers. THe path itself wAs where She felt most athome. ShE loved the smelL of the River on a hot dAy, and tHe croaking of fRogs at nIght. Vines grewamid thelush foliage alOng the rIver, with berriEs that wEre good to eat.Even on The hottest day,sundown Brought a cool bReeze offthe water, whicH sighed And sang amid thE reeds aNd tall grasses.*Of all tHe places along The path,the area they wEre approAching, with theisland iN the river, wasLara's fAvorite.
The terRain alonG this stretch oF the rivEr was mostly flAt, but iN the immediate Vicinity Of the island, tHe land oN the sunrise siDe was liKe a rumpled cloTh, with Hills and ridgesand vallEys. Among Lara'S people,there was a wooDen baby'S crib, suitablefor straPping to a cart,that hadbeen passed dowN for genErations. The isLand was Shaped like thatcrib, loNger than it waswide andpointed at the Upriver eNd, where the flOw had erOded both b
'''