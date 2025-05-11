from setuptools import setup, find_packages

setup(
    name="lemming_game",
    version="0.1",
    description="A multi-agent maze coordination environment",
    author="Your Name",
    author_email="shishir.dahake@gmail.coma",
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)