# Simple Python script to Decrypt, Encrypt Raycity.0m
# Other 0m files will not be decrypt/encrypted.

import zlib
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('mode',help='encrypt=0 decrypt=1')
parser.add_argument('input',help='path')
parser.add_argument('output',help='path')
args=parser.parse_args()

if args.mode=='0':
    input_file=open(args.input,'rb')
    output_file=open(args.output,'wb')
    
    # Get compressed data
    out_data=zlib.compress(input_file.read(),zlib.Z_BEST_COMPRESSION)
    
    # Get File size
    size=len(out_data)+10
    size=size.to_bytes(length=4,byteorder='little')
    
    # Get Adler32 Hash
    input_file.seek(0,0)
    adler32=zlib.adler32(input_file.read(),0)
    
    # Write Header
    output_file.write((10154).to_bytes(length=4,byteorder='little'))
    
    # Write File size
    output_file.write(size)
    
    # Write Unknown bytes
    output_file.write(bytes([0x53,0x01]))
    
    # Write Adler32 Hash
    output_file.write(adler32.to_bytes(length=4,byteorder='little'))
    
    # Write (Unpacked) File size
    input_file.seek(0,0)
    output_file.write(len(input_file.read()).to_bytes(length=4,byteorder='little'))
    
    # Write Output Data (Compressed by zlib)
    output_file.write(out_data)
    input_file.close()
    output_file.close()
elif args.mode=='1':
    input_file=open(args.input,'rb')
    output_file=open(args.output,'wb')
    
    # Simply decompress using zlib library, and save into file
    input_file.seek(0x12,0)
    decrypted_data=zlib.decompress(input_file.read())
    output_file.write(decrypted_data)
    
    input_file.close()
    output_file.close()
else:
    pass
