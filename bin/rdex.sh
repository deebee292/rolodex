export PYTHONPATH=$PYTHONPATH:../lib

source ../venv/bin/activate

python3 ./rdex.py $@

deactivate