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

'''


'''
(venv) user@user-HP-EliteBook-845-14-inch-G9-Notebook-PC:~/code/watKrypto/otp-vigenere$ python opt-vigenere.py 
Key: 765d68c147ade3e9b5e374dc262d9d93298ebadad5f65a9e2e
(venv) user@user-HP-EliteBook-845-14-inch-G9-Notebook-PC:~/code/watKrypto/otp-vigenere$ python cryptoanalysis.py 
Key Length Estimation using Index of Coincidence:
Key Length: 1, Average IC: 0.0068
Key Length: 2, Average IC: 0.0067
Key Length: 3, Average IC: 0.0068
Key Length: 4, Average IC: 0.0065
Key Length: 5, Average IC: 0.0165
Key Length: 6, Average IC: 0.0065
Key Length: 7, Average IC: 0.0061
Key Length: 8, Average IC: 0.0065
Key Length: 9, Average IC: 0.0066
Key Length: 10, Average IC: 0.0162
Key Length: 11, Average IC: 0.0063
Key Length: 12, Average IC: 0.0060
Key Length: 13, Average IC: 0.0065
Key Length: 14, Average IC: 0.0054
Key Length: 15, Average IC: 0.0163
Key Length: 16, Average IC: 0.0061
Key Length: 17, Average IC: 0.0067
Key Length: 18, Average IC: 0.0063
Key Length: 19, Average IC: 0.0059
Key Length: 20, Average IC: 0.0158
Key Length: 21, Average IC: 0.0055
Key Length: 22, Average IC: 0.0058
Key Length: 23, Average IC: 0.0059
Key Length: 24, Average IC: 0.0059
Key Length: 25, Average IC: 0.0765
Key Length: 26, Average IC: 0.0063
Key Length: 27, Average IC: 0.0061
Key Length: 28, Average IC: 0.0050
Key Length: 29, Average IC: 0.0054
Key Length: 30, Average IC: 0.0151
Key Length: 31, Average IC: 0.0055
Key Length: 32, Average IC: 0.0052
Key Length: 33, Average IC: 0.0051
Key Length: 34, Average IC: 0.0060
Key Length: 35, Average IC: 0.0143
Key Length: 36, Average IC: 0.0055
Key Length: 37, Average IC: 0.0054
Key Length: 38, Average IC: 0.0055
Key Length: 39, Average IC: 0.0054
Key Length: 40, Average IC: 0.0150
Key Length: 41, Average IC: 0.0054
Key Length: 42, Average IC: 0.0043
Key Length: 43, Average IC: 0.0050
Key Length: 44, Average IC: 0.0050
Key Length: 45, Average IC: 0.0153
Key Length: 46, Average IC: 0.0051
Key Length: 47, Average IC: 0.0050
Key Length: 48, Average IC: 0.0047
Key Length: 49, Average IC: 0.0044
Key Length: 50, Average IC: 0.0756
Key Length: 51, Average IC: 0.0061
Key Length: 52, Average IC: 0.0057
Key Length: 53, Average IC: 0.0042
Key Length: 54, Average IC: 0.0054
Key Length: 55, Average IC: 0.0149
Key Length: 56, Average IC: 0.0040
Key Length: 57, Average IC: 0.0038
Key Length: 58, Average IC: 0.0047
Key Length: 59, Average IC: 0.0046
Key Length: 60, Average IC: 0.0138

Most likely key length: 25
Recovering key of length 25...
Recovered Key (hex): 565d68c1678de3e995e354fc062dbd93098ebadaf5f65a9e2e

Decrypted Message:
*As THeyrOUNdEda bEnd iN thEpaThTHaT Ran BesidE thEriVeR
                                                        LArA reCogniZed THe SiLHOuEtTe oF a fIg tREe AtOPanEarbY hilL. THE wEaTHErwAs hOt anD thEdaYsWErE Long ThefigTreE WAS InfulL leaF, bUT nOtYEtbEariNg frUit.*sooN lARasPottEd otHer LAndMaRKS⠔An oUtcroPpinGoflIMEsToNe bEsidethePatH THAthAd asilhOuetTE lIkEA MaN's Face,a mARshY SPOtbEsidE therivER wHeREtHewatErfowL weRE eAsILY StArtlEd, atalLtrEeTHaT LookEd liKe aManwITH HiS arMs upRaisED. thEYwErE drAwingneaRtotHEpLaCe wHere TherEwaS ANiSlAnd In thE riVEr.THEiSlAnd Was agooDspOtTO MaKe cAmp. theyWouLdSLeEpon The iSlanDtoNiGHT.*LAra Had bEen BAckaNDfOrTh aLong The RIveR PAThmAny Timesin HEr ShORT LiFe. her pEoplEhaD NOT CrEateD thepatH�ItHAdaLwayS beeN thERe,lIKE ThE riVer‴butTheIrDEeRsKin-Shod FeetAndtHEwOoDen WheelS ofTheIrHAnDcArtskeptthePatH WELlwOrn.Laras pEOplE WEResAlt TradeRs, ANd ThEIR LiVeliHood TookTheM ONacOntiNual JourNEy.*ATThE MoutH of The RIveR,THelIttlE groUp oFhaLfAdOzEn iNtermInglED fAmILIeS GathEred SaltFroM THE GrEat Salt BedsBesIdEThE Sea.TheygroOMedaNDsIfTed The sAlt ANd LoADEdiT inTo haNdcaRTs.WHEN ThE caRts wEre FUll
      MOStoF thE groUp wOUldsTAY BeHind
                                        takIng SHelTeRAmIdrocKs anD siMPlelEAN-ToS, wHile A baND oF FIFtEeN orso oF thEheArTIErmEmbeRs seT ouTontHEpAtH thAt raN alONgsIdEThE RiveR.
WiTh tHEirpRECiOuS caRgo oF saLT, ThETrAvElerS croSsedThecOAStAllowLandsandTraVeLED ToWardthe MounTAinS.bUtLAra'S peoPle NEveR REAcHeD thE mouNtaiNTopS;THeY TravEled OnlyAs FaRAstHe fOoth
'''