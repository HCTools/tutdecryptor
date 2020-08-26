from argparse import ArgumentParser
from sys import stderr, stdout

from base64 import b64decode

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

# password to derive the key from
PASSWORD = b'fubvx788b46v'

# some utility functions
def error(error_msg = 'Corrupted/unsupported file.'):
    stderr.write(f'\033[41m\033[30m ERROR \033[0m {error_msg}\n')
    stderr.flush()

    exit(1)

# parse arguments
parser = ArgumentParser()
parser.add_argument('file', help='file to decrypt')

output_args = parser.add_mutually_exclusive_group()
output_args.add_argument('--output', '-o', help='file to output to')
output_args.add_argument('--stdin', '-O', action='store_true', help='output to stdout')

args = parser.parse_args()

# open file
encrypted_contents = ''

try:
    encrypted_contents = open(args.file, 'r').read()
except FileNotFoundError:
    error(f'File "{args.file}" was not found.')

# split the file
split_base64_contents = encrypted_contents.split('.')

if len(split_base64_contents) != 3:
    error()

split_contents = list(map(b64decode, split_base64_contents))

# derive the key
decryption_key = PBKDF2(PASSWORD, split_contents[0])

# decrypt the file
decrypted_contents = AES.new(decryption_key, AES.MODE_GCM, nonce=split_contents[1]).decrypt(split_contents[2])

print(decrypted_contents)
