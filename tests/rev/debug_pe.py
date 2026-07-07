import pefile

pe = pefile.PE(r"C:\Users\saran\Downloads\ChromeSetup.exe")

print(hex(pe.FILE_HEADER.Machine))
print(pe.FILE_HEADER.Machine)
print(hex(pe.OPTIONAL_HEADER.Magic))
print(pe.PE_TYPE)