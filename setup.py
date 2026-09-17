#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clipforge",
    version="2.0.0",
    author="Miguel Alarcón",
    description="Modern GUI for yt-dlp built with CustomTkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kunhtrats/clipforge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "customtkinter>=5.2.0",
        "yt-dlp>=2024.0.0",
    ],
    entry_points={
        "console_scripts": [
            "clipforge=clipforge.app:main",
        ],
    },
)
