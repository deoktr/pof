#!/usr/bin/env python
import codecs

MOD = 256


def KSA(key):
    key_length = len(key)
    S = list(range(MOD))
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values
    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    S = KSA(key)
    return PRGA(S)


def encrypt_logic(key, text):
    # For plaintext key, use this
    key = [ord(c) for c in key]
    # If key is in hex:
    keystream = get_keystream(key)
    res = []
    for c in text:
        val = "%02X" % (c ^ next(keystream))  # XOR and taking hex
        res.append(val)
    return "".join(res)


def encrypt(key, plaintext):
    plaintext = [ord(c) for c in plaintext]
    return encrypt_logic(key, plaintext)


def decrypt(key, ciphertext):
    ciphertext = codecs.decode(ciphertext, "hex_codec")
    res = encrypt_logic(key, ciphertext)
    return codecs.decode(res, "hex_codec").decode("utf-8")
