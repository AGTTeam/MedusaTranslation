from hacktools import common

# Control codes found in strings
codes = [0x0D, 0x0A]
# Control codes found in BIN strings
bincodes = [0x0A, 0x20]
# Ranges for BIN string locations
binrange = (1218500, 1244000)
# Characters that are encoded weirdly in the .cnut files
fixchars = {(0x83, 0x01): "ソ", (0x8D, 0x01): "構", (0x8F, 0x01): "十", (0x90, 0x01): "申", (0x93, 0x01): "貼", (0x94, 0x01): "能", (0x97, 0x01): "予"}
# Screen-size image files that have a wrong size in the NSCR file
screenfiles = [
    "adv/adv_map/bg_map_moon", "adv/adv_map/bg_map_shibusen", "adv/adv_map/bg_map_sun", "adv/adv_map/bg_mapdeathcity",
    "adv/chapter/chapter1_up_BG", "adv/chapter/chapter2_up_BG", "adv/chapter/chapter3_up_BG", "adv/chapter/chapter4_up_BG",
    "adv/death/bg_up_deathroom",
    "ui/makanote/bg_makaroom",
    "ui/menu/menu_up_BG",
    "ui/title/title_bottom", "ui/title/title_top"
]


def readShiftJIS(f, encoding="shift_jis"):
    strlen = f.readUInt()
    sjis = ""
    i = 0
    while i < strlen:
        b1 = f.readByte()
        if b1 == 0x0A:
            sjis += "|"
            i += 1
        else:
            b2 = f.readByte()
            if (b1, b2) in fixchars:
                sjis += fixchars[(b1, b2)]
                i += 2
            elif not common.checkShiftJIS(b1, b2):
                if b2 == 0x01:
                    sjis += "UNK(" + common.toHex(b1) + common.toHex(b2) + ")"
                    i += 2
                else:
                    f.seek(-1, 1)
                    sjis += chr(b1)
                    i += 1
            else:
                f.seek(-2, 1)
                try:
                    sjis += f.read(2).decode(encoding).replace("〜", "～")
                except UnicodeDecodeError:
                    common.logError("[ERROR] UnicodeDecodeError")
                    sjis += "[ERROR" + str(f.tell() - 2) + "]"
                i += 2
    return sjis


def writeShiftJIS(f, s, len2=False, untilZero=False, maxlen=0, encoding="shift_jis"):
    if not untilZero:
        pos = f.tell()
        f.writeUInt(0)
    i = 0
    x = 0
    s = s.replace("～", "〜")
    while x < len(s):
        c = s[x]
        if c == "<" and x < len(s) - 3 and s[x+3] == ">":
            code = s[x+1] + s[x+2]
            f.write(bytes.fromhex(code))
            x += 3
            i += 1
        elif c == "U" and x < len(s) - 4 and s[x:x+4] == "UNK(":
            code = s[x+4] + s[x+5]
            f.write(bytes.fromhex(code))
            code = s[x+6] + s[x+7]
            f.write(bytes.fromhex(code))
            x += 8
            i += 2
        elif c == "|":
            f.writeByte(0x0A)
            i += 1
        elif ord(c) < 128:
            f.writeByte(ord(c))
            i += 1
        else:
            f.write(c.encode(encoding))
            i += 2
        x += 1
        if maxlen > 0 and i >= maxlen:
            return -1
    if untilZero:
        f.writeByte(0x00)
    else:
        endpos = f.tell()
        f.seek(pos)
        f.writeUInt(i)
        f.seek(endpos)
    return i


def detectTextCode(s, i=0):
    if s[i] == "#":
        return len(s[i:].split(")", 1)[0]) + 1
    return 0


def detectShiftJIS(f):
    ret = ""
    sjis = 0
    while True:
        b1 = f.readByte()
        if b1 == 0:
            return ret
        if ret != "" and b1 in bincodes:
            ret += "<" + common.toHex(b1) + ">"
            continue
        elif b1 >= 32 and b1 <= 126 and (sjis > 0 or chr(b1) == "#" or ret.startswith("#")):
            ret += chr(b1)
            continue
        b2 = f.readByte()
        if b1 == 0x0D and b2 == 0x0A:
            ret += "|"
        elif common.checkShiftJIS(b1, b2):
            f.seek(-2, 1)
            try:
                ret += f.read(2).decode("shift-jis").replace("〜", "～")
                sjis += 1
            except UnicodeDecodeError:
                if ret.count("UNK(") >= 5:
                    return ""
                ret += "UNK(" + common.toHex(b1) + common.toHex(b2) + ")"
        elif len(ret) > 0 and ret.count("UNK(") < 5:
            ret += "UNK(" + common.toHex(b1) + common.toHex(b2) + ")"
        else:
            return ""
