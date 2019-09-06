# Medusa Translation
## Setup
Create a "data" folder and copy the rom as "rom.nds" in it.  
Download [ndstool.exe](https://www.darkfader.net/ds/files/ndstool.exe).  
(Optional, only for patch creation) Download xdelta.exe.  
(Optional, only for PSD export) Create a "imagemagick" folder and extract [ImageMagick portable](https://imagemagick.org/script/download.php#windows) in it.  
## Run from binary
Download the latest [release](https://github.com/Illidanz/MedusaTranslation/releases) in the same folder as the dependencies.  
Run "tool extract" to extract everything and "tool repack" to repack after editing.  
Run "tool extract --help" or "tool repack --help" for more info.  
## Run from source
Install [Python 3.7](https://www.python.org/downloads/), pip and virtualenv.  
Pull [hacktools](https://github.com/Illidanz/hacktools).  
```
virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e ../hacktools
```
## Text Editing
Rename the \*\_output.txt files to \*\_input.txt (bin_output.txt to bin_input.txt, etc) and add translations for each line after the "=" sign.  
Control codes are specified as <XX> or UNK(XXXX), they should usually be kept. Line breaks are specified as "|" or "<0A>" depending on the file.  
To blank out a line, use a single "!". If just left empty, the line will be left untranslated.  
Comments can be added at the end of lines by using #  
## Image Editing
Rename the out\_\* folders to work\_\* (out_NCGR to work_NCGR, etc).  
Edit the images in the work folder(s). The palette on the right should be followed but the repacker will try to approximate other colors to the closest one.  
If an image doesn't require repacking, it should be deleted from the work folder.  
