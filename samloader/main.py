# SPDX-License-Identifier: GPL-3.0+
# Copyright (C) 2020 nlscc

import click
import os
import base64
import xml.etree.ElementTree as ET
from clint.textui import progress

from . import request
from . import crypt
from . import fusclient
from . import versionfetch

def getbinaryfile(client, fw, region, model):
    req = request.binaryinform(fw, region, model, client.nonce)
    resp = client.makereq("NF_DownloadBinaryInform.do", req)
    root = ET.fromstring(resp)
    status = int(root.find("./FUSBody/Results/Status").text)
    if status != 200:
        raise Exception("DownloadBinaryInform returned {}, firmware could not be found?".format(status))
    filename = root.find("./FUSBody/Put/BINARY_NAME/Data").text
    path = root.find("./FUSBody/Put/MODEL_PATH/Data").text
    return path, filename

def initdownload(client, filename):
    req = request.binaryinit(filename, client.nonce)
    resp = client.makereq("NF_DownloadBinaryInitForMass.do", req)

@click.group()
def cli():
    pass

@cli.command(help="Check the update server for the latest available firmware.")
@click.argument("model")
@click.argument("region")
def checkupdate(model, region):
    fw = versionfetch.getlatestver(region, model)
    print(fw)

@cli.command(help="Download the specified firmware version.")
@click.argument("version")
@click.argument("model")
@click.argument("region")
@click.argument("out")
def download(version, model, region, out):
    download_function(version, model, region, out)

def download_function(version, model, region, out):
    client = fusclient.FUSClient()
    path, filename = getbinaryfile(client, version, region, model)
    initdownload(client, filename)
    if os.path.isdir(out):
        out = os.path.join(out, filename)
    if os.path.exists(out):
        f = open(out, "ab")
        start = os.stat(out).st_size
        print("Resuming {} at {}".format(path+filename, start))
    else:
        f = open(out, "wb")
        start = 0
        print("Downloading {}".format(path+filename))
    r = client.downloadfile(path+filename, start)
    length = int(r.headers["Content-Length"])
    if "Content-MD5" in r.headers:
        md5 = base64.b64decode(r.headers["Content-MD5"]).hex()
        print("MD5: {}".format(md5))
    for chunk in progress.bar(r.iter_content(chunk_size=0x10000), expected_size=(length/0x10000)+1):
        if chunk:
            f.write(chunk)
            f.flush()
    f.close()
    print("Done!")
    return out

@cli.command(help="Decrypt enc4 files.")
@click.argument("version")
@click.argument("model")
@click.argument("region")
@click.argument("infile")
@click.argument("outfile")
def decrypt4(version, model, region, infile, outfile):
    decrypt4_function(version, model, region, infile, outfile)

def decrypt4_function(version, model, region, infile, outfile):
    key = crypt.getv4key(version, model, region)
    print("Decrypting with key {}...".format(key.hex()))
    length = os.stat(infile).st_size
    with open(infile, "rb") as inf:
        with open(outfile, "wb") as outf:
            crypt.decrypt_progress(inf, outf, key, length)
    print("Done!")

@cli.command(help="Download and decrypt enc4/enc2 files.")
@click.argument("version")
@click.argument("model")
@click.argument("region")
@click.argument("outfile", nargs = -1)
def mkfw(version, model, region, outfile):
    infile = download_function(version, model, region, ())
    if outfile == ():
        outfile = infile[:-5]
    if infile[-1] == '4':
        decrypt4_function(version, model, region, infile, outfile)
    else:
        decrypt2_function(version, model, region, infile, outfile)
    os.remove(infile)

@cli.command(help="Decrypt enc2 files.")
@click.argument("version")
@click.argument("model")
@click.argument("region")
@click.argument("infile")
@click.argument("outfile")
def decrypt2(version, model, region, infile, outfile):
    decrypt2_function(version, model, region, infile, outfile)

def decrypt2_function(version, model, region, infile, outfile):
    key = crypt.getv2key(version, model, region)
    print("Decrypting with key {}...".format(key.hex()))
    length = os.stat(infile).st_size
    with open(infile, "rb") as inf:
        with open(outfile, "wb") as outf:
            crypt.decrypt_progress(inf, outf, key, length)
    print("Done!")

if __name__ == "__main__":
    cli()
