# based on qwerty12356-wart's scripton and scripton_ndk patch
# https://github.com/waydroid/waydroid/issues/788#issuecomment-2167334937
# https://github.com/waydroid/waydroid/issues/788#issuecomment-2162386712

def check_hex(file_path, skip_bytes, num_bytes, hex_to_check):
    with open(file_path, "r+b") as f:
        f.seek(skip_bytes)
        b = int.from_bytes(f.read(num_bytes), byteorder="big")
        return hex_to_check == b


def patch_hex(file_path, base_hex, ghidra_offset, hex_to_check, hex_to_write):
    skip_bytes = ghidra_offset - base_hex
    num_bytes = (len(hex(hex_to_write)) - 2) // 2
    if check_hex(file_path, skip_bytes, num_bytes, hex_to_check):
        with open(file_path, "r+b") as f:
            f.seek(skip_bytes)
            f.write(hex_to_write.to_bytes(length=num_bytes, byteorder="big"))
            print("libndk patched")
    elif check_hex(file_path, skip_bytes, num_bytes, hex_to_write):
        print("Already patched")
    else:
        print("Hex mismatch!")


def patch_libndk(libndk_path):
    base_hex = 0x101000
    patch_hex(libndk_path, base_hex, 0x307dd1, 0x83e2fa, 0x83e2ff)
    patch_hex(libndk_path, base_hex, 0x307cd6, 0x83e2fa, 0x83e2ff)


# untested
def patch_libhoudini(libhoudini_path):
    base_hex = 0x100000
    patch_hex(libhoudini_path, base_hex, 0x4062a5, 0x48b8fbffffff, 0x48b8ffffffff)
    patch_hex(libhoudini_path, base_hex, 0x4099d6, 0x83e0fb, 0x83e0ff)
    patch_hex(libhoudini_path, base_hex, 0x409b42, 0xe8892feeff, 0x9090909090)
