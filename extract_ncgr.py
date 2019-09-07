import os
import game
from hacktools import common, nitro


def run():
    infolder = "data/extract/data/Rom/"
    outfolder = "data/out_NCGR/"
    common.makeFolder(outfolder)

    common.logMessage("Extracting NCGR to", outfolder, "...")
    files = common.getFiles(infolder, [".NCGR", ".NCBR"])
    for file in common.showProgress(files):
        common.logDebug("Processing", file, "...")
        extension = os.path.splitext(file)[1]
        palettefile = infolder + file.replace(extension, ".NCLR")
        mapfile = infolder + file.replace(extension, ".NSCR")
        cellfile = infolder + file.replace(extension, ".NCER")
        # Read image
        palettes, ncgr, nscr, ncer, width, height = nitro.readNitroGraphic(palettefile, infolder + file, mapfile, cellfile)
        if ncgr is None:
            continue
        # Fix a couple weird images with wrong sizes
        if file.replace(extension, "") in game.screenfiles or file.startswith("event/bg/bg0"):
            width = height = 256
        # Export img
        common.makeFolders(outfolder + os.path.dirname(file))
        outfile = outfolder + file.replace(extension, ".png")
        if ncer is not None:
            nitro.drawNCER(outfile, ncer, ncgr, palettes, True, True)
        else:
            nitro.drawNCGR(outfile, nscr, ncgr, palettes, width, height)
    common.logMessage("Done! Extracted", len(files), "files")
