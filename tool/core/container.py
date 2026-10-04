import struct
import zlib

MAGIC = b"206S"
VERSION = 2


def pack(entries):
    out = bytearray()
    out += MAGIC
    out += bytes([VERSION])
    out += struct.pack(">H", len(entries))
    for name, data in entries:
        name_bytes = name.encode("ascii")
        out += bytes([len(name_bytes)])
        out += name_bytes
        out += struct.pack(">II", len(data), zlib.crc32(data) & 0xFFFFFFFF)
        out += data
    return bytes(out)


def unpack(blob):
    if len(blob) < 7 or blob[:4] != MAGIC:
        raise ValueError("invalid magic")
    if blob[4] != VERSION:
        raise ValueError("unsupported version")
    count = struct.unpack(">H", blob[5:7])[0]
    offset = 7
    entries = {}
    for _ in range(count):
        name_len = blob[offset]
        offset += 1
        name = blob[offset:offset + name_len].decode("ascii")
        offset += name_len
        data_len, crc = struct.unpack(">II", blob[offset:offset + 8])
        offset += 8
        data = blob[offset:offset + data_len]
        if len(data) != data_len or zlib.crc32(data) & 0xFFFFFFFF != crc:
            raise ValueError("corrupted entry")
        offset += data_len
        entries[name] = data
    if offset != len(blob):
        raise ValueError("corrupted file")
    return entries
