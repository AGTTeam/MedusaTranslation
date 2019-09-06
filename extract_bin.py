import codecs
import game
from hacktools import common


def run():
    infile = "data/extract/arm9.bin"
    outfile = "data/bin_output.txt"

    common.logMessage("Extracting BIN to", outfile, "...")
    with codecs.open(outfile, "w", "utf-8") as out:
        with common.Stream(infile, "rb") as f:
            # Skip the beginning and end of the file to avoid false-positives
            f.seek(game.binrange[0])
            foundstrings = []
            while f.tell() < game.binrange[1]:
                pos = f.tell()
                check = game.detectShiftJIS(f)
                if check != "":
                    if check not in foundstrings:
                        common.logDebug(" Found string at", pos)
                        foundstrings.append(check)
                        out.write(check + "=\n")
                    pos = f.tell() - 1
                f.seek(pos + 1)
    common.logMessage("Done! Extracted", len(foundstrings), "lines")
