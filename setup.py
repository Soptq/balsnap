import setuptools

setuptools.setup(
    name="balsnap",
    version="0.1",
    author="Soptq",
    description="Module for eth-brownie used to take snapshots of token balances of accounts",
    url="https://github.com/Soptq/balsnap",
    project_urls={
        "Bug Tracker": "https://github.com/Soptq/balsnap/issues"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)