# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 Nayil Mukhametshin

# Calculate keys and decrypt encrypted firmware packages.

import hashlib
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
from clint.textui import progress

from . import request
from . import fusclient
from . import versionfetch

unpad = lambda d: d[:-d[-1]]

def getv4key(version, model, region):
    client = fusclient.FUSClient()
    req = request.binaryinform(version, region, model, client.nonce)
    resp = client.makereq("NF_DownloadBinaryInform.do", req)
    root = ET.fromstring(resp)
    logicval = root.find("./FUSBody/Put/LOGIC_VALUE_FACTORY/Data").text
    deckey = request.getlogiccheck(version, logicval)
    return hashlib.md5(deckey.encode()).digest()

def getv2key(version, model, region):
    deckey = region + ":" + model + ":" + version
    return hashlib.md5(deckey.encode()).digest()

def decrypt_progress(inf, outf, key, length):
    cipher = AES.new(key, AES.MODE_ECB)
    assert length % 16 == 0
    chunks = length//4096+1
    for i in progress.bar(range(chunks)):
        block = inf.read(4096)
        if not block:
            break
        decblock = cipher.decrypt(block)
        if i == chunks - 1:
            outf.write(unpad(decblock))
        else:
            outf.write(decblock)
