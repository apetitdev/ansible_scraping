#!/usr/bin/env bash

install() {
    pip_update >> /dev/null
}
pip_update() {
    sudo pip install -r requirements.txt
}
init_env() {
    eval "$(ssh-agent -s)"
    ssh-add
    mkdir -p __OutPut__
    tar -zxvf __Data__.tar.gz
    export PYTHONPATH="`pwd`:`pwd`/tools:$PYTHONPATH"
    jupyter notebook --no-browser --port=8889
}

pip_update
init_env