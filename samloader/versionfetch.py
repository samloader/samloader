# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 Nayil Mukhametshin

# Get the latest firmware version for a device.

import xml.etree.ElementTree as ET
import requests

def getlatestver(region, model):
    r = requests.get("http://fota-cloud-dn.ospserver.net/firmware/" + region + "/" + model + "/version.xml")
    root = ET.fromstring(r.text)
    vercode = root.find("./firmware/version/latest").text
    vc = vercode.split("/")
    if len(vc) == 4:
        return vercode
    else:
        return vercode + "/" + vc[0]
