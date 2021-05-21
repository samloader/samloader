# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 nlscc

""" Build FUS XML requests. """

import xml.etree.ElementTree as ET

def getlogiccheck(inp: str, nonce: str) -> str:
    """ Calculate the request checksum for a given input and nonce. """
    if len(inp) < 16:
        raise Exception("getlogiccheck() input too short")
    out = ""
    for c in nonce:
        out += inp[ord(c) & 0xf]
    return out

def build_reqhdr(fusmsg: ET.Element):
    """ Build the FUSHdr of an XML message. """
    fushdr = ET.SubElement(fusmsg, "FUSHdr")
    ET.SubElement(fushdr, "ProtoVer").text = "1.0"

def build_reqbody(fusmsg: ET.Element, params: dict):
    """ Build the FUSBody of an XML message. """
    fusbody = ET.SubElement(fusmsg, "FUSBody")
    fput = ET.SubElement(fusbody, "Put")
    for tag, value in params.items():
        setag = ET.SubElement(fput, tag)
        sedata = ET.SubElement(setag, "Data")
        sedata.text = str(value)

def binaryinform(fwv: str, model: str, region: str, nonce: str) -> str:
    """ Build a BinaryInform request. """
    fusmsg = ET.Element("FUSMsg")
    build_reqhdr(fusmsg)
    build_reqbody(fusmsg, {
        "ACCESS_MODE": 2,
        "BINARY_NATURE": 1,
        "CLIENT_PRODUCT": "Smart Switch",
        "DEVICE_FW_VERSION": fwv,
        "DEVICE_LOCAL_CODE": region,
        "DEVICE_MODEL_NAME": model,
        "LOGIC_CHECK": getlogiccheck(fwv, nonce)
    })
    return ET.tostring(fusmsg)

def binaryinit(filename: str, nonce: str) -> str:
    """ Build a BinaryInit request. """
    fusmsg = ET.Element("FUSMsg")
    build_reqhdr(fusmsg)
    checkinp = filename.split(".")[0][-16:]
    build_reqbody(fusmsg, {
        "BINARY_FILE_NAME": filename,
        "LOGIC_CHECK": getlogiccheck(checkinp, nonce)
    })
    return ET.tostring(fusmsg)
