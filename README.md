
# wrn-1

**wrn-1** (typically stylised as wrn, or wrn-1) is a hexadecimal/binary format made purely for the fun of it and is regularly updated.

## Current release

`wrn-1 v1.0`

## Features

- Encode text into `.wrn` files
- Inspect WRN files
- View hexadecimal payloads
- Convert hexadecimal into readable text
- CRC32 checksum validation

## Usage

Run the WRN utility:

```bash
wrn
```

## Format

| Field | Size |
|---|---:|
| Signature (`WREN`) | 4 bytes |
| Version | 1 byte |
| Flags | 1 byte |
| Payload length | 2 bytes |
| Payload | Variable |
| CRC32 | 4 bytes |

All multi-byte header values use big-endian byte order.

## Development

WRN is currently implemented in Python.

Additional language implementations and developer tools are planned.

## Status

Early development. Contributions and testing are planned.
