from typing import Union
import zlib
from cose.messages import CoseMessage
import cbor2
import qrcode

#---- INSERT HERE A VALID GREENPASS CODE ----
str = "HC1:<GREENPASS QR CODE STRING>"
#---- INSERT HERE WHAT DO YOU WANT TO REPLACE ----
#---- The two strings must have the same lenght ----
# For example: YOUR_SURNAME and YOUR_NEW_SURNAME
strToReplace = "str1"
strToReplaceTo = "str2"

BASE45_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
BASE45_DICT = {v: i for i, v in enumerate(BASE45_CHARSET)}

def b45encode(buf: bytes) -> bytes:
    """Convert bytes to base45-encoded string"""
    res = ""
    buflen = len(buf)
    for i in range(0, buflen & ~1, 2):
        x = (buf[i] << 8) + buf[i + 1]
        e, x = divmod(x, 45 * 45)
        d, c = divmod(x, 45)
        res += BASE45_CHARSET[c] + BASE45_CHARSET[d] + BASE45_CHARSET[e]
    if buflen & 1:
        d, c = divmod(buf[-1], 45)
        res += BASE45_CHARSET[c] + BASE45_CHARSET[d]
    return res.encode()

def b45decode(s: str) -> bytes:
    """Decode base45-encoded string to bytes"""
    try:
        buf = [BASE45_DICT[c] for c in s.strip()]
        
        buflen = len(buf)
        if buflen % 3 == 1:
            raise ValueError("Invalid base45 string")

        res = []
        for i in range(0, buflen, 3):
            if buflen - i >= 3:
                x = buf[i] + buf[i + 1] * 45 + buf[i + 2] * 45 * 45
                if x > 0xFFFF:
                    raise ValueError
                res.extend(divmod(x, 256))
            else:
                x = buf[i] + buf[i + 1] * 45
                if x > 0xFF:
                    raise ValueError
                res.append(x)
        return bytes(res)
    except (ValueError, KeyError, AttributeError):
        raise ValueError("Invalid base45 string")


# 1 - strip string
strip = str.replace("HC1:", "")
#2 - b45 decode
decoded = b45decode(strip)
#3 - zlib decompress
decompressed = zlib.decompress(decoded)

# ----------- NOT USEFUL ------------
#4 - CoseMessage decode
cosedecode = CoseMessage.decode(decompressed)
#5 - cbor2 loads
data = cbor2.loads(cosedecode.payload)
# ------------------------------------
print(decompressed)
newdecompressed = decompressed

newdecompressedstr = newdecompressed.decode('iso-8859-15')
newdecompressedstr = newdecompressedstr.replace(strToReplace, strToReplaceTo)
newdecompressed = newdecompressedstr.encode('iso-8859-15')
print(newdecompressed)
#3 - compress
compress = zlib.compress(newdecompressed)
#2 - b45 encode
encode = b45encode(compress)
#1 - string header
newstring = "HC1:" + encode.decode("utf-8")

img = qrcode.make(newstring)
type(img)
img.save("qr.png")


