#!/bin/bash
function pip3_install {
  for p in $@; do
    sudo pip3 install $p
    if [ $? -ne 0 ]; then
      echo "could not install $p - abort"
      exit 1
    fi
  done
}

function unix_command {
  $@
  if [ $? -ne 0 ]; then
    echo "could not run $@ - abort"
    exit 1
  fi
}

clear
full_path=$(realpath $0)
dir_path=$(dirname $full_path)
pip3 install tqdm selenium argparse requests
pip3 install -U python-dotenv
chmod 755 download.py
./download.py

