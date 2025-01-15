import os
import subprocess


current_dir = os.path.dirname(os.path.realpath(__file__))


def run_compile_sh():
    # run_cmd = "sh FAST/compile.sh"
    run_cmd = "sh " + current_dir + "/compile.sh"
    print(run_cmd)
    p = subprocess.Popen(run_cmd, shell=True, stderr=subprocess.STDOUT)
    p.wait()

    if p.returncode != 0:
        print("Error in compile.sh")
        exit(1)


if __name__ == "__main__":
    run_compile_sh()
    print("Done")
