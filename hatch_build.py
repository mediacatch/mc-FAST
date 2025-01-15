from hatchling.builders.hooks.custom import BuildHookInterface
import subprocess


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        print("Initializing build hook...")
        # Run your custom bash script
        subprocess.run(["bash", "./FAST/compile.sh"], check=True)
