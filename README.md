# Medusa Translation
This repository is for the tool used to translate the game. If you're looking for the English patch, click [here](https://agtteam.net/medusa).  
## Setup
Install [Python 3](https://www.python.org/downloads/).  
Install [ImageMagick](https://imagemagick.org/script/download.php). For Windows, check "Add application directory to your system path" while installing.  
Download this repository by downloading and extracting it, or cloning it.  
Copy the original Japanese rom into the same folder and rename it as `medusa.nds`.  
Run `run_windows.bat` (for Windows) or `run_bash` (for OSX/Linux) to run the tool.  
## Text Editing
Rename the \*\_output.txt files to \*\_input.txt (bin_output.txt to bin_input.txt, etc) and add translations for each line after the "=" sign.  
The text in cnut_input is automatically wordwrapped, but a `|` can be used to force a line break.  
New textboxes can be added by appending `>>` followed by the new text.  
Control codes are specified as `\<XX\>` or `UNK(XXXX)`, they should usually be kept. Line breaks are specified as `|` or `<0A>` depending on the file.  
To blank out a line, use a single `!`. If just left empty, the line will be left untranslated.  
Comments can be added at the end of lines by using `//`  
## Image Editing
Rename the out\_\* folders to work\_\* (out_NCGR to work_NCGR, etc).  
Edit the images in the work folder(s). The palette on the right should be followed but the repacker will try to approximate other colors to the closest one.  
If an image doesn't require repacking, it should be deleted from the work folder.  
## Run from command line
This is not recommended if you're not familiar with Python and the command line.  
After following the Setup section, run `pipenv sync` to install dependencies.  
Run `pipenv run python tool.py extract` to extract everything, and `pipenv run python tool.py repack` to repack.  
You can use switches like `pipenv run python tool.py repack --bin` to only repack certain parts to speed up the process.  
