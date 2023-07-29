import os
import click
import game
from hacktools import common, nds, nitro

version = "1.5.0"
romfile = "medusa.nds"
rompatch = "data/medusa_patched.nds"
bannerfile = "data/repack/banner.bin"
binfile = "data/repack/arm9.bin"
patchfile = "data/patch.xdelta"
infolder = "data/extract/"
replacefolder = "data/replace/"
outfolder = "data/repack/"


@common.cli.command()
@click.option("--rom", is_flag=True, default=False)
@click.option("--bin", is_flag=True, default=False)
@click.option("--cnut", is_flag=True, default=False)
@click.option("--ncgr", is_flag=True, default=False)
@click.option("--nsbmd", is_flag=True, default=False)
def extract(rom, bin, cnut, ncgr, nsbmd):
    all = not rom and not bin and not cnut and not ncgr and not nsbmd
    if all or rom:
        nds.extractRom(romfile, infolder, outfolder)
    if all or bin:
        nds.extractBIN(game.binrange, game.detectShiftJIS)
    if all or cnut:
        import extract_cnut
        extract_cnut.run()
    if all or ncgr:
        nitro.extractIMG("data/extract/data/Rom/", "data/out_NCGR/", [".NCGR", ".NCBR"], game.readImage)
    if nsbmd:
        nitro.extractNSBMD("data/extract/data/Rom/", "data/out_NSBMD/")


@common.cli.command()
@click.option("--no-rom", is_flag=True, default=False, hidden=True)
@click.option("--bin", is_flag=True, default=False)
@click.option("--cnut", is_flag=True, default=False)
@click.option("--ncgr", is_flag=True, default=False)
def repack(no_rom, bin, cnut, ncgr):
    all = not bin and not cnut and not ncgr
    if all or bin:
        nds.repackBIN(game.binrange, game.freeranges, game.detectShiftJIS, game.writeBINShiftJIS, "shift_jis", "//")
        common.logMessage("Patching BIN ...")
        with common.Stream(binfile, "r+b") as fo:
            # Patch the text rendering function to allow more than 15 characters per line (Thanks StorMyu!)
            fo.seek(0x6680C)
            fo.writeByte(0xFF)
        common.logMessage("Done!")
    if all or cnut:
        import repack_cnut
        repack_cnut.run()
    if all or ncgr:
        nitro.repackIMG("data/work_NCGR/", "data/extract/data/Rom/", "data/repack/data/Rom/", [".NCGR", ".NCBR"], game.readImage)

    if not no_rom:
        if os.path.isdir(replacefolder):
            common.mergeFolder(replacefolder, outfolder)
        nds.editBannerTitle(bannerfile, "Soul Eater\nMedusa's Plot\nBandai Namco Games")
        nds.repackRom(romfile, rompatch, outfolder, patchfile)


@common.cli.command(hidden=True)
def patchdump():
    patchfile = "data/bad_to_good.xdelta"
    common.logMessage("Creating xdelta patch", patchfile, "...")
    xdelta = common.bundledFile("xdelta.exe")
    if not os.path.isfile(xdelta):
        common.logError("xdelta not found")
        return
    common.execute(xdelta + " -f -e -s {rom} {rompatch} {patch}".format(rom=romfile.replace(".nds", "_bad.nds"), rompatch=romfile, patch=patchfile), False)
    common.logMessage("Done!")


if __name__ == "__main__":
    common.setupTool("MedusaTranslation", version, "data", romfile, 0x151439bc)
