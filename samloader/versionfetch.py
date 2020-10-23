# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 nlscc

# Get the latest firmware version for a device.

import xml.etree.ElementTree as ET
import requests


def get_latest_ver(model: str, region: str):
    model = model.upper()
    region = region.upper()
    r = requests.get("https://fota-cloud-dn.ospserver.net/firmware/" + region + "/" + model + "/version.xml")
    r.raise_for_status()
    root = ET.fromstring(r.text)
    vercode = root.find("./firmware/version/latest").text
    if vercode is None:
        raise ValueError("No latest firmware found")

    vc = vercode.split("/")
    if len(vc) == 3:
        vc.append(vc[0])
    if vc[2] == "":
        vc[2] = vc[0]
    return "/".join(vc)
