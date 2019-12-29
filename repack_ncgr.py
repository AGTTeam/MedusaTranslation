import os
import game
from hacktools import common, nitro


def run():
    workfolder = "data/work_NCGR/"
    infolder = "data/extract/data/Rom/"
    outfolder = "data/repack/data/Rom/"

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
        palettefile = file.replace(extension, ".NCLR")
        mapfile = file.replace(extension, ".NSCR")
        cellfile = file.replace(extension, ".NCER")
        common.copyFile(infolder + file, outfolder + file)
        if os.path.isfile(infolder + palettefile):
            common.copyFile(infolder + palettefile, outfolder + palettefile)
        if os.path.isfile(infolder + mapfile):
            common.copyFile(infolder + mapfile, outfolder + mapfile)
        if os.path.isfile(infolder + cellfile):
            common.copyFile(infolder + cellfile, outfolder + cellfile)
        # Read image
        palettes, ncgr, nscr, ncer, width, height = nitro.readNitroGraphic(outfolder + palettefile, outfolder + file, outfolder + mapfile, outfolder + cellfile)
        if ncgr is None:
            continue
        # Fix a couple weird images with wrong sizes
        screenfile = False
        if file.replace(extension, "") in game.screenfiles or file.startswith("event/bg/bg0"):
            width = height = 256
            screenfile = True
        # Import img
        if nscr is None and ncer is None:
            nitro.writeNCGR(outfolder + file, ncgr, workfolder + pngfile, palettes, width, height)
        elif ncer is None:
            if screenfile:
                nitro.writeNSCR(outfolder + file, ncgr, nscr, workfolder + pngfile, palettes, width, height)
            else:
                nitro.writeMappedNSCR(outfolder + file, outfolder + mapfile, ncgr, nscr, workfolder + pngfile, palettes, width, height)
        else:
            nitro.writeNCER(outfolder + file, ncgr, ncer, workfolder + pngfile, palettes)
    common.logMessage("Done!")
