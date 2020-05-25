# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 Nayil Mukhametshin

# FUS authentication functions (decrypting nonce, calculating auth token)

from Crypto.Cipher import AES
import base64
import requests

KEY_1 = "hqzdurufm2c8mf6bsjezu1qgveouv7c7"
KEY_2 = "w13r4cvf4hctaujv"

unpad = lambda d: d[:-d[-1]]
pad = lambda d: d + bytes([16 - (len(d) % 16)]) * (16 - (len(d) % 16))

def aes_encrypt(inp, key):
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    return cipher.encrypt(pad(inp))

def aes_decrypt(inp, key):
    cipher = AES.new(key, AES.MODE_CBC, key[:16])
    return unpad(cipher.decrypt(inp))

def getfkey(inp):
    key = ""
    for i in range(16):
        key += KEY_1[inp[i]]
    key += KEY_2
    return key.encode()

def getauth(nonce):
    keydata = [ord(c) % 16 for c in nonce]
    fkey = getfkey(keydata)
    return base64.b64encode(aes_encrypt(nonce.encode(), fkey)).decode()

def decryptnonce(inp):
    nonce = aes_decrypt(base64.b64decode(inp), KEY_1.encode()).decode()
    return nonce
