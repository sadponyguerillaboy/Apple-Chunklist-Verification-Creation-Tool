from Crypto.PublicKey import RSA
import numpy as np
import os

# Generate Keys
key = RSA.generate(2048)

# Get keys form RSA Key
public_key = key.publickey().exportKey('PEM')
pubkey = key.publickey().n
pkey = pubkey.to_bytes(256, 'big')
reversed_pubkey = np.flip(np.frombuffer(bytearray(pkey), dtype=np.uint8, count=-1, offset=0),0).tobytes()
private_key = key.exportKey('PEM')

# Display Keys
print('Public Key: ', public_key.decode('ascii'))
print('Raw Public Key: ', hex(pubkey))
print('Reversed Raw Public Key: ', reversed_pubkey)
print('Private Key: ', private_key.decode('ascii'))

# write public key 'PEM' format to file
with open('custom_keys/public_key.pem', 'wb+') as out_file:
	out_file.write(public_key)
	out_file.close()

# Remove pubkey.bin file if exists from previous attempt (becuase using append write option to build 'ab+')
if os.path.exists('custom_keys/pubkey.bin'):
	os.remove('custom_keys/pubkey.bin')

# write reversed public key in raw RSA format like the keys stored in EFI
header = b'\x18\x01\x00\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x01\x00\x00'
with open('custom_keys/pubkey.bin', 'ab+') as out_file:
	out_file.write(header)
	out_file.write(reversed_pubkey)
	out_file.close()

# write private key to file
with open('custom_keys/private_key.pem', 'wb+') as out_file:
	out_file.write(private_key)
	out_file.close()
