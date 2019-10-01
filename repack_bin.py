import codecs
import os
import struct
import game
from hacktools import common


def run():
    binin = "data/extract/arm9.bin"
    binout = "data/repack/arm9.bin"
    binfile = "data/bin_input.txt"
    freeranges = [(0x1220A0, 0x122960)]
    currentrange = 0
    rangepos = freeranges[currentrange][0]

    common.logMessage("Patching BIN ...")
    common.copyFile(binin, binout)
    with common.Stream(binout, "r+b") as fo:
        # Patch the text rendering function to allow more than 15 characters per line (Thanks StorMyu!)
        fo.seek(0x6680C)
        fo.writeByte(0xFF)
    common.logMessage("Done!")

    if not os.path.isfile(binfile):
        common.logError("Input file", binfile, "not found")
        return

    common.logMessage("Repacking BIN from", binfile, "...")
    # load common section
    section = {}
    with codecs.open(binfile, "r", "utf-8") as bin:
        section = common.getSection(bin, "", "//")
        chartot, transtot = common.getSectionPercentage(section)
    with common.Stream(binin, "rb") as fi:
        allbin = fi.read()
        strpointers = {}
        with common.Stream(binout, "r+b") as fo:
            # Skip the beginning and end of the file to avoid false-positives
            fi.seek(game.binrange[0])
            while fi.tell() < game.binrange[1]:
                pos = fi.tell()
                check = game.detectShiftJIS(fi)
                if check in section and section[check][0] != "":
                    newstr = section[check][0]
                    common.logDebug("Replacing string at", pos)
                    fo.seek(pos)
                    endpos = fi.tell() - 1
                    newlen = game.writeShiftJIS(fo, newstr, False, True, endpos - pos + 1)
                    if newlen < 0:
                        if rangepos >= freeranges[currentrange][1] and newstr not in strpointers:
                            common.logWarning("No more room! Skipping ...")
                        else:
                            # Write the string in a new portion of the rom
                            if newstr in strpointers:
                                newpointer = strpointers[newstr]
                            else:
                                common.logDebug("No room for the string, redirecting to", common.toHex(rangepos))
                                fo.seek(rangepos)
                                game.writeShiftJIS(fo, newstr, False, True)
                                fo.writeZero(1)
                                newpointer = 0x02000000 + rangepos
                                rangepos = fo.tell()
                                strpointers[newstr] = newpointer
                                if rangepos >= freeranges[currentrange][1]:
                                    if currentrange + 1 < len(freeranges):
                                        currentrange += 1
                                        rangepos = freeranges[currentrange][0]
                            # Search and replace the old pointer
                            pointer = 0x02000000 + pos
                            pointersearch = struct.pack("<I", pointer)
                            index = 0
                            common.logDebug("Searching for pointer", pointersearch.hex().upper())
                            while index < len(allbin):
                                index = allbin.find(pointersearch, index)
                                if index < 0:
                                    break
                                common.logDebug("Replaced pointer at", str(index))
                                fo.seek(index)
                                fo.writeUInt(newpointer)
                                index += 4
                    else:
                        fo.writeZero(endpos - fo.tell())
                fi.seek(pos + 1)
    common.logMessage("Done! Translation is at {0:.2f}%".format((100 * transtot) / chartot))
