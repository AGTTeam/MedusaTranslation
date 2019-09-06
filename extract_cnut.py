import codecs
import os
import game
from hacktools import common


def run():
    infolder = "data/extract/data/Rom/event/script/"
    outfile = "data/cnut_output.txt"

    common.logMessage("Extracting CNUT to", outfile, "...")
    with codecs.open(outfile, "w", "utf-8") as out:
        files = common.getFiles(infolder, ".cnut")
        for file in common.showProgress(files):
            common.logDebug("Processing", file, "...")
            first = True
            size = os.path.getsize(infolder + file)
            with common.Stream(infolder + file, "rb") as f:
                while f.tell() < size - 4:
                    pos = f.tell()
                    b1 = f.readByte()
                    b2 = f.readByte()
                    b3 = f.readByte()
                    b4 = f.readByte()
                    if b1 == 0x10 and b2 == 0x00 and b3 == 0x00 and b4 == 0x08:
                        # Found a string
                        check = game.readShiftJIS(f)
                        # Remove some codes that are found in almost every string start/end
                        if check.startswith("#CLR()"):
                            check = check[6:]
                        if check.startswith("#ARW("):
                            check = check[7:]
                        if check.endswith("#INP()"):
                            check = check[:-6]
                        if not common.isAscii(check):
                            if first:
                                out.write("!FILE:" + file + "\n")
                                first = False
                            out.write(check + "=\n")
                    else:
                        f.seek(pos + 1)
    common.logMessage("Done! Extracted", len(files), "files")
