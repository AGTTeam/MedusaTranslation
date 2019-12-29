import codecs
import os
import game
from hacktools import common, nitro


# CNUT functions:
# #WAI(n): Wait n frames
# #ARW(n): Change popup style
# #COL(n): Change color (1=Black, 4=Blue, 7=Red)
# #SPD(n): Change the draw speed to a character every n frames
# #CIN(x,y): Show character?
# #CLR(): Clear the screen?
# #INP(): Wait for input?
# #OUT(): ?

def run():
    infolder = "data/extract/data/Rom/event/script/"
    outfolder = "data/repack/data/Rom/event/script/"
    infile = "data/cnut_input.txt"
    fontfile = "data/repack/data/Rom/font/font0.NFTR"
    replacefontfile = "data/replace/data/Rom/font/font0.NFTR"
    chartot = transtot = 0

    if not os.path.isfile(infile):
        common.logError("Input file", infile, "not found")
        return

    common.logMessage("Repacking CNUT from", infile, "...")
    if os.path.isfile(replacefontfile):
        glyphs = nitro.getFontGlyphs(replacefontfile)
    else:
        glyphs = nitro.getFontGlyphs(fontfile)
    with codecs.open(infile, "r", "utf-8") as cnut:
        files = common.getFiles(infolder, ".cnut")
        for file in common.showProgress(files):
            section = common.getSection(cnut, file, "//")
            if len(section) == 0:
                common.makeFolders(outfolder + file)
                common.copyFile(infolder + file, outfolder + file)
                continue
            chartot, transtot = common.getSectionPercentage(section, chartot, transtot)
            # Repack the file
            common.logDebug("Processing", file, "...")
            size = os.path.getsize(infolder + file)
            lastpos = 0
            with common.Stream(infolder + file, "rb") as fin:
                common.makeFolders(infolder + file)
                with common.Stream(outfolder + file, "wb") as f:
                    while fin.tell() < size - 4:
                        pos = fin.tell()
                        b1 = fin.readByte()
                        b2 = fin.readByte()
                        b3 = fin.readByte()
                        b4 = fin.readByte()
                        if b1 == 0x10 and b2 == 0x00 and b3 == 0x00 and b4 == 0x08:
                            # Found a string
                            check = game.readShiftJIS(fin)
                            pre = post = ""
                            # Add back some codes that are removed from extracted lines
                            if check.startswith("#CLR()"):
                                pre = "#CLR()"
                                check = check[6:]
                            if check.startswith("#ARW("):
                                pre += check[:7]
                                check = check[7:]
                            if check.endswith("#INP()"):
                                post = "#INP()"
                                check = check[:-6]
                            # Check if the line is translated and replace it
                            if check in section:
                                newsjis = section[check].pop(0)
                                if len(section[check]) == 0:
                                    del section[check]
                                if newsjis != "":
                                    newsjis = pre + newsjis + post
                                    if newsjis != check:
                                        newsjis = common.wordwrap(newsjis, glyphs, 205, game.detectTextCode)
                                        newsjis = newsjis.replace(">>", "#INP()" + pre).replace("|", "<0A>")
                                        # Copy data up to here
                                        endpos = fin.tell()
                                        fin.seek(lastpos)
                                        f.write(fin.read(pos + 4 - lastpos))
                                        lastpos = endpos
                                        common.logDebug("  Repacking at", pos)
                                        game.writeShiftJIS(f, newsjis)
                        else:
                            fin.seek(pos + 1)
                    fin.seek(lastpos)
                    f.write(fin.read(size - lastpos))
    common.logMessage("Done! Translation is at {0:.2f}%".format((100 * transtot) / chartot))
