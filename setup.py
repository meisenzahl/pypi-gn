import distutils.cmd
import distutils.log
import os
import platform
import setuptools
import setuptools.command.install
import shutil
import urllib.request
import zipfile


class PostInstallCommand(setuptools.command.install.install):
    def run(self):
        setuptools.command.install.install.run(self)
        source_dir = os.path.dirname(os.path.abspath(__file__))

        OS = platform.system()
        url = "https://chrome-infra-packages.appspot.com/dl/gn/gn/{}-amd64/+/latest"
        executable = "gn"
        if OS == "Linux":
            url = url.format("linux")
        elif OS == "Darwin":
            url = url.format("mac")
        elif OS == "Windows":
            url = url.format("windows")
            executable = "gn.exe"
        else:
            self.announce(
                "ERROR: {} is not supported".format(OS),
                distutils.log.ERROR
            )
            exit(1)

        self.announce(
            "Downloading GN for {}".format(OS),
            distutils.log.INFO
        )

        zip_file = os.path.join(source_dir, "gn.zip")
        with urllib.request.urlopen(url) as response, open(zip_file, "wb") as out_file:
            shutil.copyfileobj(response, out_file)

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extract(executable, os.path.join(source_dir))
            os.chmod(os.path.join(source_dir, executable), 0o775)

        if os.path.isfile(zip_file):
            os.remove(zip_file)

        source = os.path.join(source_dir, executable)
        target = os.path.join(self.install_scripts, executable)
        if os.path.isfile(target):
            os.remove(target)

        self.move_file(source, target)


setuptools.setup(
    cmdclass={
        "install": PostInstallCommand,
    },
    name="gn-meisenzahl",
    version="latest",
    author="Marius Meisenzahl",
    author_email="mariusmeisenzahl@gmail.com",
    description="GN is a meta-build system that generates build files for Ninja.",
    url="https://github.com/meisenzahl/gn",
    packages=[],
    classifiers=[],
    python_requires=">=3.6",
    install_requires=["ninja"],
)
