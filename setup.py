from setuptools import setup, find_packages

setup(
    name="apex-specagent",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "specagent=apex_specagent.cli:main",
        ],
    },
)
