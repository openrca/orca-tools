from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


def get_requirements():
    with open("requirements.txt") as requirements:
        return requirements.read().splitlines()


setup(
    name="orca_tools",
    version="0.1.0",
    long_description=readme(),
    url="ttps://github.com/openrca/orca-tools",
    author="OpenRCA",
    license="Apache License 2.0",
    install_requires=get_requirements(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "orca-tools = orca_tools.cmd.cli:main",
        ],
    },
    zip_safe=False)
