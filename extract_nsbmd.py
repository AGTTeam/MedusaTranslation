import os
from hacktools import common, nitro


def run():
    infolder = "data/extract/data/Rom/"
    outfolder = "data/out_NSBMD/"
    common.makeFolder(outfolder)

    common.logMessage("Extracting NSBMD to", outfolder, "...")
    files = common.getFiles(infolder, ".nsbmd")
    for file in common.showProgress(files):
        common.logDebug("Processing", file, "...")
        nsbmd = nitro.readNSBMD(infolder + file)
        if nsbmd is not None and len(nsbmd.textures) > 0:
            common.makeFolders(outfolder + os.path.dirname(file))
            for texi in range(len(nsbmd.textures)):
                nitro.drawNSBMD(outfolder + file.replace(".nsbmd", "") + "_" + nsbmd.textures[texi].name + ".png", nsbmd, texi)
    common.logMessage("Done! Extracted", len(files), "files")
