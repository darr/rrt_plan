#!/bin/bash
#####################################
## File name : run.sh
## Create date : 2018-11-26 11:19
## Modified date : 2021-05-23 13:25
## Author : DARREN
## Describe : not set
## Email : lzygzh@126.com
####################################

realpath=$(readlink -f "$0")
basedir=$(dirname "$realpath")
export basedir=$basedir/cmd_sh/
export filename=$(basename "$realpath")
export PATH=$PATH:$basedir
export PATH=$PATH:$basedir/dlbase
export PATH=$PATH:$basedir/dlproc
#base sh file
. dlbase.sh
#function sh file
. etc.sh

kill -9 `ps -ef|grep main.py|grep -v grep|awk '{print $2}'`
kill -9 `ps -ef|grep defunct|grep -v grep|awk '{print$3}'`

function create_vir_env(){
    dlfile_check_is_have_dir $env_path

    if [[ $? -eq 0 ]]; then
        bash ./cmd_sh/create_env.sh
    else
        $DLLOG_INFO "$1 virtual env had been created"
    fi
}

create_vir_env

#bash ./cmd_sh/check_code.sh

#   source $env_path/py2env/bin/activate
#   deactivate

source $env_path/py3env/bin/activate
#jupyter notebook
#python ./tank_learn/main.py
#pip install torch-1.3.1-cp35-cp35m-manylinux1_x86_64.whl
#python main.py

#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple jupyter
#pip uninstall matplotlib
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib==2.2.0
#pip install matplotlib-2.2.0.tar.gz
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyrr
#python ./antisubmarine_learn/pic.py
#python ./antisubmarine_learn/main_PPO_continuous_gym.py
#python ./rrt_3D/rrt_connect3D.py
#python ./rrt_3D/Grrt_connect3D.py
#python ./Search_3D/DstarLite3D.py
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas
python ./rrt_main.py
#pip list


#python mytest.py
#python mat_test.py
#python mat_3d.py
#python main.py
#pip list
#pip --version
#pip install numpy
#pip install --upgrade --user nbconvert
#pip install --upgrade nbconvert
#pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade nbconvert
#jupyter notebook

deactivate
