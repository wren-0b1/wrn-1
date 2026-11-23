
from pathlib import Path
import struct
import zlib

MAGIC = b"WREN"
VERSION = 1
DATA = Path(__file__).parent / "data"

HEADER = struct.Struct(">4sBBH")
CRC = struct.Struct(">I")


def pack(payload, flags=0):
    if not isinstance(payload, bytes):
        raise TypeError("payload must be bytes")

    if len(payload) > 65535:
        raise ValueError("payload too large")

    header = HEADER.pack(
        MAGIC, VERSION, flags, len(payload)
    )

    checksum = CRC.pack(zlib.crc32(payload))

    return header + payload + checksum


def unpack(raw):
    if len(raw) < 12:
        raise ValueError("file too small")

    magic, version, flags, size = HEADER.unpack(
        raw[:HEADER.size]
    )

    if magic != MAGIC:
        raise ValueError("invalid signature")

    if version != VERSION:
        raise ValueError("unsupported version")

    if flags != 0:
        raise ValueError("unsupported flags")

    if len(raw) != HEADER.size + size + CRC.size:
        raise ValueError("incorrect file size")

    start = HEADER.size
    end = start + size

    payload = raw[start:end]

    stored_crc = CRC.unpack(raw[end:])[0]
    actual_crc = zlib.crc32(payload)

    if stored_crc != actual_crc:
        raise ValueError("checksum mismatch")

    return payload


def new_file():
    print("\nwrn / new file")

    name = input("filename > ").strip()

    if not name or "/" in name or "\\" in name:
        print("invalid filename")
        return

    if name.endswith(".wrn"):
        name = name[:-4]

    if not name or len(name) > 40:
        print("invalid filename")
        return

    payload = input("text > ").encode("utf-8")

    DATA.mkdir(parents=True, exist_ok=True)
    target = DATA / f"{name}.wrn"

    if target.exists():
        print("file already exists")
        return

    encoded = pack(payload)
    target.write_bytes(encoded)

    print(f"\nwritten // {target.name}")
    print(f"size    // {len(encoded)} bytes")


def inspect():
    print("\nwrn / inspect")

    files = sorted(DATA.glob("*.wrn")) if DATA.exists() else []

    if not files:
        print("no files found")
        return

    for i, file in enumerate(files, 1):
        print(f"[{i}] {file.name}")

    choice = input("\nselect: ").strip()

    if not choice.isdigit():
        print("invalid selection")
        return

    index = int(choice) - 1

    if not 0 <= index < len(files):
        print("invalid selection")
        return

    raw = files[index].read_bytes()

    try:
        payload = unpack(raw)
    except (ValueError, struct.error) as error:
        print(f"\ninvalid // {error}")
        return

    checksum = CRC.unpack(raw[-4:])[0]

    print("\n-- file info ----------------")
    print(f"version  : {VERSION}")
    print(f"flags    : 00")
    print(f"length   : {len(payload)} bytes")
    print(f"checksum : {checksum:08X}")
    print(f"hex      : {payload.hex(' ').upper()}")

    try:
        print(f"text     : {payload.decode('utf-8')}")
    except UnicodeDecodeError:
        print("text     : binary payload")

    print("\nstatus   : valid")


def hex_to_text():
    print("\nwrn / hex to text")

    raw = input("hex > ").strip()

    try:
        data = bytes.fromhex(raw)
    except ValueError:
        print("invalid hex")
        return

    try:
        result = data.decode("utf-8")
    except UnicodeDecodeError:
        print("valid hex, but not utf-8 text")
        return

    print(f"\ntext // {result}")


def main():
    while True:
        print("""
 wrn-1 v1.0
 --------------------
 [1] new file
 [2] inspect
 [3] hex to text
 [0] exit
""")

        choice = input("wrn > ").strip()

        if choice == "1":
            new_file()
        elif choice == "2":
            inspect()
        elif choice == "3":
            hex_to_text()
        elif choice == "0":
            print("wrn // offline")
            break
        else:
            print("unknown command")


if __name__ == "__main__":
    main()
