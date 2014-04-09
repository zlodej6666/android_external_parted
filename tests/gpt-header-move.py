# open img file, subtract 33 from altlba address, and move the last 33 sectors
# back by 33 sectors

from struct import *
from zipfile import crc32
import array
import sys
file = open(sys.argv[1],'rb+')
file.seek(512)
gptheader = file.read(512)
altlba = unpack_from('<q', gptheader,offset=32)[0]
gptheader = array.array('c',gptheader)
pack_into('<Q', gptheader, 32, altlba-33)
#zero header crc
pack_into('<L', gptheader, 16, 0)
#compute new crc
newcrc = ((crc32(buffer(gptheader,0,92))) & 0xFFFFFFFF)
pack_into('<L', gptheader, 16, newcrc)
file.seek(512)
file.write(gptheader)
file.seek(512*altlba)
gptheader = file.read(512)
file.seek(512*(altlba-32))
backup = file.read(512*32)
altlba -= 33
gptheader = array.array('c',gptheader)
#update mylba
pack_into('<Q', gptheader, 24, altlba)
#update table lba
pack_into('<Q', gptheader, 72, altlba-32)
#zero header crc
pack_into('<L', gptheader, 16, 0)
#compute new crc
newcrc = ((crc32(buffer(gptheader,0,92))) & 0xFFFFFFFF)
pack_into('<L', gptheader, 16, newcrc)
file.seek(512*(altlba-32))
file.write(backup)
file.write(gptheader)
file.write("\0" * (512 * 33))

