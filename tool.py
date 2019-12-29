import os
import click
import game
from hacktools import common, nds

version = "1.2.0"
romfile = "data/rom.nds"
rompatch = "data/rom_patched.nds"
bannerfile = "data/repack/banner.bin"
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
        binfile = "data/extract/arm9.bin"
        outfile = "data/bin_output.txt"
        common.logMessage("Extracting BIN to", outfile, "...")
        foundstrings = nds.extractBinaryStrings(binfile, outfile, game.binrange, game.detectShiftJIS)
        common.logMessage("Done! Extracted", len(foundstrings), "lines")
    if all or cnut:
        import extract_cnut
        extract_cnut.run()
    if all or ncgr:
        import extract_ncgr
        extract_ncgr.run()
    if nsbmd:
        import extract_nsbmd
        extract_nsbmd.run()


@common.cli.command()
@click.option("--no-rom", is_flag=True, default=False)
@click.option("--bin", is_flag=True, default=False)
@click.option("--cnut", is_flag=True, default=False)
@click.option("--ncgr", is_flag=True, default=False)
def repack(no_rom, bin, cnut, ncgr):
    all = not bin and not cnut and not ncgr
    if all or bin:
        import repack_bin
        repack_bin.run()
    if all or cnut:
        import repack_cnut
        repack_cnut.run()
    if all or ncgr:
        import repack_ncgr
        repack_ncgr.run()

    if not no_rom:
        if os.path.isdir(replacefolder):
            common.mergeFolder(replacefolder, outfolder)
        nds.editBannerTitle(bannerfile, "Soul Eater\nMedusa's Conspiracy\nBandai Namco Games")
        nds.repackRom(romfile, rompatch, outfolder, patchfile)


if __name__ == "__main__":
    click.echo("MedusaTranslation version " + version)
    if not os.path.isdir("data"):
        common.logError("data folder not found.")
        quit()
    common.cli()
