# # Cryptanalysis Lab and McEliece Paper Summary for the course Cryptology (1DT075)

## Overview

This repository contains the solutions for the lab assignment "Cryptanalysis of the Modified Vigenère Cipher" from the Cryptology (1DT075) course at Uppsala University, Spring 2024. The lab assignment is divided into three parts, each focusing on different aspects of the cryptanalysis of a modified Vigenère cipher. Additionally, as part of the course workload, the summary of the paper "A Public-Key Cryptosystem Based On Algebraic Coding Theory" by R. J. Mceliece can be found in the repository.

## Structure for the Assignment "Cryptanalysis of the Modified Vigenère Cipher"

### Part A: Encryption
- **Objective:** Encryption of a Swedish text using the modified Vigenère cipher.
- **Details:** 
  - The cipher uses an extended alphabet of 29 characters (including the Swedish characters å, ä, ö) and operates modulo 29.
  - The text had to be between 200-600 characters long, and the key must be no longer than 16 characters.
- **Output:**
  - `vig_groupX.plain`: The original plaintext.
  - `vig_groupX.key`: The encryption key.
  - `vig_groupX.crypto`: The resulting ciphertext.

### Part B: Breaking the Cipher
- **Objective:** Break texts encrypted using the modified Vigenère cipher.
- **Details:** 
  - The ciphertexts are provided, and the task is to determine the key and recover the plaintext.
  - Techniques such as the Friedman test and frequency analysis (using the chi-square test) are employed.
- **Output:**
  - `b1.py`: Python script for breaking short key ciphertexts.
  - `b2.py`: Python script for breaking long key ciphertexts.
  - The reconstructed keys and decrypted plaintexts are included in the output.

### Part C: Reasoning about Ciphers
- **Objective:** Reflecting on the security and properties of various modified Vigenère ciphers.
- **Details:** 
  - Questions regarding the security implications of different cipher modifications are answered, including the impact of key length and language on cryptanalysis.
  - The security of proposed ciphers based on the Vigenère cipher is discussed.

## Files and Directories

- `ciphertexts (short key)/`: Contains the ciphertexts encrypted with short keys.
- `ciphertexts (long key)/`: Contains the ciphertexts encrypted with a long key.
- `b1.py`: Python script for breaking the short key ciphertexts.
- `b2.py`: Python script for breaking the long key ciphertexts.
- `report.pdf`: The lab report detailing the techniques used, frequency tables, and answers to the questions in Part C.
- `README.md`: This file.

## How to Run

### Prerequisites

- Python 3.x
- Required Python packages: `scipy`, `collections`

### Instructions

1. Install the required Python packages using your preferred package manager.
2. Run the `b1.py` script to break short key ciphertexts and `b2.py` for long key ciphertexts.

### Output

- The reconstructed keys and decrypted plaintexts will be displayed as output.

## Techniques Used

- **Friedman Test:** Used to estimate the key length based on the Index of Coincidence.
- **Frequency Analysis with Chi-Square Test:** Used to determine the key by analyzing letter frequencies and applying the chi-square test to compare observed and expected letter distributions.
