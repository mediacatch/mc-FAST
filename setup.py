import os
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        # Call the standard install process
        install.run(self)

        # Run the bash script
        script_path = os.path.join(os.path.dirname(__file__), "FAST/compile.sh")
        if os.path.exists(script_path):
            os.system(f"bash {script_path}")
        else:
            raise FileNotFoundError("compile.sh script not found.")


setup(
    name="FAST",
    version="0.1.0",
    packages=["FAST"],
    install_requires=[],
    cmdclass={
        "install": CustomInstallCommand,
    },
)
