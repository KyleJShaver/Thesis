## Install Dependencies
### linux: 
`sudo apt-get install -y git python3 python3-pip libsm6 libxrender1 libfontconfig1 libxtst6`

`git clone https://github.com/KyleJShaver/Thesis.git`

`cd Thesis`

`pip install -r requirements.txt`

`cp Dockerfile_templace Dockerfile`



## Run setup.py

## Google Cloud command
Run the above commands up until the Dockerfile, or the following command:

`sudo apt-get install -y git python3 python3-pip libsm6 libxrender1 libfontconfig1 libxtst6 && git clone https://github.com/KyleJShaver/Thesis.git && cd Thesis && pip3 install -r requirements.txt`



`screen -S thesis`

`python3 setup.py python3 <firebase domain>`

`screen -r thesis` to reattach