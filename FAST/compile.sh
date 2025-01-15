
export CUDA_HOME=/usr/local/cuda-12.6
export PATH=/usr/local/cuda-12.6/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH

cd FAST/models/post_processing/pa/
python setup.py build_ext --inplace
cd ../pse/
python setup.py build_ext --inplace
cd ../ccl/
python setup.py build_ext --inplace
cd ../../../