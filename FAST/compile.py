import os
import subprocess


current_dir = os.path.dirname(os.path.realpath(__file__))


# export CUDA_HOME=/usr/local/cuda-12.6
# export PATH=/usr/local/cuda-12.6/bin:$PATH
# export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH

# cd FAST/models/post_processing/pa/
# python setup.py build_ext --inplace
# cd ../pse/
# python setup.py build_ext --inplace
# cd ../ccl/
# python setup.py build_ext --inplace
# cd ../../../


def compile():
    os.environ["CUDA_HOME"] = "/usr/local/cuda-12.6"
    os.environ["PATH"] = "/usr/local/cuda-12.6/bin:" + os.environ["PATH"]
    os.environ["LD_LIBRARY_PATH"] = "/usr/local/cuda-12.6/lib64:" + os.environ.get(
        "LD_LIBRARY_PATH", ""
    )

    # Compile post_processing/pa
    os.chdir(os.path.join(current_dir, "models/post_processing/pa"))
    subprocess.call(["python", "setup.py", "build_ext", "--inplace"])
    os.chdir(os.path.join(current_dir, "models/post_processing/pse"))
    subprocess.call(["python", "setup.py", "build_ext", "--inplace"])
    os.chdir(os.path.join(current_dir, "models/post_processing/ccl"))
    subprocess.call(["python", "setup.py", "build_ext", "--inplace"])
    os.chdir(current_dir)


if __name__ == "__main__":
    compile()
