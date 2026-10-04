import struct
import time
import zlib

MAGIC = b"206M"
VERSION = 1
SUITE = 1
HEAD_FMT = ">4sBBHQI"
MAX_ITER = 10000000


def build(text_name, hidden_name, iterations, created=None):
    if created is None:
        created = int(time.time())
    text_bytes = text_name.encode("ascii")
    hidden_bytes = hidden_name.encode("ascii")
    body = struct.pack(HEAD_FMT, MAGIC, VERSION, SUITE, 0, created, iterations)
    body += bytes([len(text_bytes)]) + text_bytes
    body += bytes([len(hidden_bytes)]) + hidden_bytes
    return body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def parse(data):
    head_len = struct.calcsize(HEAD_FMT)
    if len(data) < head_len + 6:
        raise ValueError("invalid manifest")
    body = data[:-4]
    crc = struct.unpack(">I", data[-4:])[0]
    if zlib.crc32(body) & 0xFFFFFFFF != crc:
        raise ValueError("corrupted manifest")
    magic, version, suite, flags, created, iterations = struct.unpack(HEAD_FMT, body[:head_len])
    if magic != MAGIC or version != VERSION or suite != SUITE:
        raise ValueError("unsupported manifest")
    if not 1 <= iterations <= MAX_ITER:
        raise ValueError("invalid iterations")
    offset = head_len
    text_len = body[offset]
    offset += 1
    text_name = body[offset:offset + text_len].decode("ascii")
    offset += text_len
    hidden_len = body[offset]
    offset += 1
    hidden_name = body[offset:offset + hidden_len].decode("ascii")
    offset += hidden_len
    if offset != len(body):
        raise ValueError("corrupted manifest")
    return {
        "created": created,
        "iterations": iterations,
        "text_name": text_name,
        "hidden_name": hidden_name,
    }
