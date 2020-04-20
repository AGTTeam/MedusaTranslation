import os
import click
import game
from hacktools import common, nds, nitro

version = "1.4.0"
romfile = "data/medusa.nds"
rompatch = "data/medusa_patched.nds"
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
        nds.extractBIN(game.binrange, game.detectShiftJIS)
    if all or cnut:
        import extract_cnut
        extract_cnut.run()
    if all or ncgr:
        nitro.extractIMG("data/extract/data/Rom/", "data/out_NCGR/", [".NCGR", ".NCBR"], game.readImage)
    if nsbmd:
        nitro.extractNSBMD("data/extract/data/Rom/", "data/out_NSBMD/")


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
        nitro.repackIMG("data/work_NCGR/", "data/extract/data/Rom/", "data/repack/data/Rom/", [".NCGR", ".NCBR"], game.readImage)

    if not no_rom:
        if os.path.isdir(replacefolder):
            common.mergeFolder(replacefolder, outfolder)
        nds.editBannerTitle(bannerfile, "Soul Eater\nMedusa's Plot\nBandai Namco Games")
        nds.repackRom(romfile, rompatch, outfolder, patchfile)


if __name__ == "__main__":
    click.echo("MedusaTranslation version " + version)
    if not os.path.isdir("data"):
        common.logError("data folder not found.")
        quit()
    common.cli()
