#!/usr/bin/env python3
"""pof setup."""

from pathlib import Path

from setuptools import find_packages, setup

root = Path(__file__).parent.resolve()

requirements = (root / "requirements.txt").read_text().splitlines()

long_description = (root / "README.md").read_text()

setup(
    name="pof",
    version="1.3.10",
    author="deoktr",
    author_email="",
    description="Python Obfuscation Framework.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3 license",
    url="https://github.com/deoktr/pof",
    project_urls={
        "Bug Tracker": "https://github.com/deoktr/pof/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
    ],
    packages=find_packages(include=["pof", "pof.*"]),
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "pof=pof.cli:_cli",
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
