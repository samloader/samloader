# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 nlscc

import argparse
import os
import base64
import xml.etree.ElementTree as ET
from tqdm import tqdm

from . import request
from . import crypt
from . import fusclient
from . import versionfetch

def main():
    parser = argparse.ArgumentParser(description="Download and query firmware for Samsung devices.")
    parser.add_argument("-m", "--dev-model", help="device model", required=True)
    parser.add_argument("-r", "--dev-region", help="device region code", required=True)
    subparsers = parser.add_subparsers(dest="command")
    dload = subparsers.add_parser("download", help="download a firmware")
    dload.add_argument("-v", "--fw-ver", help="firmware version to download", required=True)
    dload.add_argument("-R", "--resume", help="resume an unfinished download", action="store_true")
    dload.add_argument("-M", "--show-md5", help="print the expected MD5 hash of the downloaded file", action="store_true")
    dload.add_argument("-D", "--do-decrypt", help="auto-decrypt the downloaded file after downloading", action="store_true")
    dload_out = dload.add_mutually_exclusive_group(required=True)
    dload_out.add_argument("-O", "--out-dir", help="output the server filename to the specified directory")
    dload_out.add_argument("-o", "--out-file", help="output to the specified file")
    chkupd = subparsers.add_parser("checkupdate", help="check for the latest available firmware version")
    decrypt = subparsers.add_parser("decrypt", help="decrypt an encrypted firmware")
    decrypt.add_argument("-v", "--fw-ver", help="encrypted firmware version", required=True)
    decrypt.add_argument("-V", "--enc-ver", type=int, choices=[2, 4], default=4, help="encryption version (default 4)")
    decrypt.add_argument("-i", "--in-file", help="encrypted firmware file input", required=True)
    decrypt.add_argument("-o", "--out-file", help="decrypted firmware file output", required=True)
    args = parser.parse_args()
    if args.command == "download":
        client = fusclient.FUSClient()
        path, filename, size = getbinaryfile(client, args.fw_ver, args.dev_model, args.dev_region)
        out = args.out_file if args.out_file else os.path.join(args.out_dir, filename)
        try:
            dloffset = os.stat(out).st_size if args.resume else 0
        except FileNotFoundError:
            args.resume = None
            dloffset = 0

        print("resuming" if args.resume else "downloading", filename)
        if dloffset == size:
            print("already downloaded!")
            return
        fd = open(out, "ab" if args.resume else "wb")
        initdownload(client, filename)
        r = client.downloadfile(path+filename, dloffset)
        if args.show_md5 and "Content-MD5" in r.headers:
            print("MD5:", base64.b64decode(r.headers["Content-MD5"]).hex())
        pbar = tqdm(total=size, initial=dloffset, unit="B", unit_scale=True)
        for chunk in r.iter_content(chunk_size=0x10000):
            if chunk:
                fd.write(chunk)
                fd.flush()
                pbar.update(0x10000)
        fd.close()
        if args.do_decrypt: # decrypt the file if needed
            dec = out.replace(".enc4", "").replace(".enc2", "") # TODO: use a better way of doing this
            if os.path.isfile(dec):
                print("file {} already exists, refusing to auto-decrypt!")
                return
            print("decyrpting", out)
            # TODO: remove code duplication with decrypt command
            getkey = crypt.getv2key if filename.endswith(".enc2") else crypt.getv4key
            key = getkey(args.fw_ver, args.dev_model, args.dev_region)
            length = os.stat(out).st_size
            with open(out, "rb") as inf:
                with open(dec, "wb") as outf:
                    crypt.decrypt_progress(inf, outf, key, length)
            os.remove(out)
    elif args.command == "checkupdate":
        print(versionfetch.getlatestver(args.dev_model, args.dev_region))
    elif args.command == "decrypt":
        getkey = crypt.getv4key if args.enc_ver == 4 else crypt.getv2key
        key = getkey(args.fw_ver, args.dev_model, args.dev_region)
        length = os.stat(args.in_file).st_size
        with open(args.in_file, "rb") as inf:
            with open(args.out_file, "wb") as outf:
                crypt.decrypt_progress(inf, outf, key, length)

def initdownload(client, filename):
    req = request.binaryinit(filename, client.nonce)
    resp = client.makereq("NF_DownloadBinaryInitForMass.do", req)

def getbinaryfile(client, fw, model, region):
    req = request.binaryinform(fw, model, region, client.nonce)
    resp = client.makereq("NF_DownloadBinaryInform.do", req)
    root = ET.fromstring(resp)
    status = int(root.find("./FUSBody/Results/Status").text)
    if status != 200:
        raise Exception("DownloadBinaryInform returned {}, firmware could not be found?".format(status))
    filename = root.find("./FUSBody/Put/BINARY_NAME/Data").text
    if filename is None:
        raise Exception("DownloadBinaryInform failed to find a firmware bundle")
    size = int(root.find("./FUSBody/Put/BINARY_BYTE_SIZE/Data").text)
    path = root.find("./FUSBody/Put/MODEL_PATH/Data").text
    return path, filename, size
