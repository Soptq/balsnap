import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="balsnap",
    version="0.1.0",
    author="Soptq",
    description="A light-weight python library that help take balance snapshots of multiple tokens and accounts at once",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Soptq/balsnap",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/Soptq/balsnap/issues"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["eth-brownie", "prettytable"],
    python_requires=">=3.9",
)