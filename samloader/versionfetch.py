# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 nlscc

""" Get the latest firmware version for a device. """

import xml.etree.ElementTree as ET
import requests

def normalizevercode(vercode: str) -> str:
    """ Normalize a version code to four-part form. """
    ver = vercode.split("/")
    if len(ver) == 3:
        ver.append(ver[0])
    if ver[2] == "":
        ver[2] = ver[0]
    return "/".join(ver)

def getlatestver(model: str, region: str) -> str:
    """ Get the latest firmware version code for a model and region. """
    req = requests.get("https://fota-cloud-dn.ospserver.net/firmware/" \
        + region + "/" + model + "/version.xml")
    req.raise_for_status()
    root = ET.fromstring(req.text)
    vercode = root.find("./firmware/version/latest").text
    if vercode is None:
        raise Exception("No latest firmware found")
    return normalizevercode(vercode)
