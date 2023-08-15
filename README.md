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
- Install additional packages into created environment
  - git

## Setup Environment (one time)
- Start environment by clicking Play -> Open Terminal
- Create new directory with "md nngm"
- Change into directory with "cd nngm"
- Checkout repository with 
  - git clone https://github.com/TimoKuchheuser/nngm-idat-api.git
- Install pip with "conda install pip"
- Install dependencies with "pip install -r requirements.txt"
 
## Update Environment
- Run "git pull"
- Install dependencies with "pip install -r requirements.txt"

## Start endpoint
- Change into directory with "cd nngm-idat-api"
- Start endpoint with "python endpoint.py"