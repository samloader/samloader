# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 nlscc

# Build FUS XML requests.

import xml.etree.ElementTree as ET

def getlogiccheck(inp, nonce):
    if len(inp) < 16:
        raise Exception("getlogiccheck() input too short")
    out = ""
    for c in nonce:
        out += inp[ord(c) & 0xf]
    return out

def binaryinform(fw, model, region, nonce):
    fusmsg = ET.Element("FUSMsg")
    fushdr = ET.SubElement(fusmsg, "FUSHdr")
    ET.SubElement(fushdr, "ProtoVer").text = "1.0"
    fusbody = ET.SubElement(fusmsg, "FUSBody")
    fput = ET.SubElement(fusbody, "Put")
    ET.SubElement(ET.SubElement(fput, "ACCESS_MODE"), "Data").text = "2"
    ET.SubElement(ET.SubElement(fput, "BINARY_NATURE"), "Data").text = "1"
    ET.SubElement(ET.SubElement(fput, "CLIENT_PRODUCT"), "Data").text = "Smart Switch"
    ET.SubElement(ET.SubElement(fput, "DEVICE_FW_VERSION"), "Data").text = fw
    ET.SubElement(ET.SubElement(fput, "DEVICE_LOCAL_CODE"), "Data").text = region
    ET.SubElement(ET.SubElement(fput, "DEVICE_MODEL_NAME"), "Data").text = model
    ET.SubElement(ET.SubElement(fput, "LOGIC_CHECK"), "Data").text = getlogiccheck(fw, nonce)
    return ET.tostring(fusmsg)

def binaryinit(filename, nonce):
    fusmsg = ET.Element("FUSMsg")
    fushdr = ET.SubElement(fusmsg, "FUSHdr")
    ET.SubElement(fushdr, "ProtoVer").text = "1.0"
    fusbody = ET.SubElement(fusmsg, "FUSBody")
    fput = ET.SubElement(fusbody, "Put")
    ET.SubElement(ET.SubElement(fput, "BINARY_FILE_NAME"), "Data").text = filename
    checkinp = filename.split(".")[0][-16:]
    ET.SubElement(ET.SubElement(fput, "LOGIC_CHECK"), "Data").text = getlogiccheck(checkinp, nonce)
    return ET.tostring(fusmsg)
