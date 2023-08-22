# nngm-idat-api

## Windows setup
- Download and install Anaconda Python distribution 
  - https://www.anaconda.com/download
- Start Anaconda Navigator
- Create new Environment
  - Select Environments
  - Select Create
  - Enter name (e.g. "nngm")
  - Select Python 3.11.x

## Setup Environment (one time)
- Start environment by clicking Play -> Open Terminal
- Install git with `conda install git`


- Create new directory with `md nngm`
- Change into directory with `cd nngm`


- Checkout repository with 
  - git clone https://github.com/TimoKuchheuser/nngm-idat-api.git


- Install pip with `conda install pip`
- Install dependencies with `pip install -r requirements.txt`
 
## Update Environment
- Run `git pull`
- Install dependencies with `pip install -r requirements.txt`

## Start endpoint
- Change into directory with `cd nngm-idat-api`
- Start endpoint with `python endpoint.py`

# Create package with PyInstaller (Windows)
## One time
- Start conda environment setup earlier
- Run `pip install pyinstaller`
- Note down the path names to the executables given after the installation
  - e.g. `C:\Users\user\AppData\Roaming\Python\Python311\Scripts`

## After an update
- Make sure the following variables in endpoint.py are up to date
  - VERSION_XSD
  - PUBLIC_KEY_HEX
  - VERSION_PRE
- Change to the source directory inside the conda environment
- Delete the `build/` and `dist/` directories
- Extend the current path variable
  - `set PATH=%PATH%;C:\Users\user\AppData\Roaming\Python\Python311\Scripts`
- Create the package
  - `pyinstaller --hidden-import=_cffi_backend --onefile endpoint.py`
  - `_cffi_backend` is necessary for the encryption to work
- Distribute file `dist/endpoint.exe`