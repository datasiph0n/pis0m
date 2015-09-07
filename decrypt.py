#!/usr/bin/python
import os, fnmatch, random, struct
from Crypto.Cipher import AES

key = raw_input("Decryption Key: ")
directory = raw_input("Directory: ")

def find_files(root_dir):
    extentions = ['*.enc']
    for dirpath, dirs, files in os.walk(root_dir):
        if 'Windows' not in dirpath:
            for basename in files:
                for ext in extentions:
                    if fnmatch.fnmatch(basename, ext):
                        filename = os.path.join(dirpath, basename)
                        yield filename

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

for filename in find_files(directory):
  print 'Found Source:', filename
  decrypt_file(key, filename)
  os.remove(filename)
