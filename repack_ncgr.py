import os
import game
from hacktools import common, nitro


def run():
    workfolder = "data/work_NCGR/"
    infolder = "data/repack/data/Rom/"

    common.logMessage("Repacking NCGR from", workfolder, "...")
    files = common.getFiles(infolder, [".NCGR", ".NCBR"])
    for file in common.showProgress(files):
        extension = os.path.splitext(file)[1]
        pngfile = file.replace(extension, ".psd")
        if not os.path.isfile(workfolder + pngfile):
            pngfile = file.replace(extension, ".png")
            if not os.path.isfile(workfolder + pngfile):
                continue
        common.logDebug("Processing", file, "...")
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
        # Import img
        if nscr is None and ncer is None:
            nitro.writeNCGR(infolder + file, ncgr, workfolder + pngfile, palettes, width, height)
        elif ncer is None:
            nitro.writeNSCR(infolder + file, ncgr, nscr, workfolder + pngfile, palettes, width, height)
        else:
            nitro.writeNCER(infolder + file, ncgr, ncer, workfolder + pngfile, palettes)
    common.logMessage("Done!")
