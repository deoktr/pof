#!/usr/bin/env python3
"""pof setup."""

from pathlib import Path

from setuptools import find_packages, setup

root = Path(__file__).parent.resolve()

long_description = (root / "README.md").read_text()

install_requires = [
    "rope>=1.0.0",
    "Pillow>=10.0.0",
]

setup(
    name="python-obfuscation-framework",
    version="1.5.0",
    author="deoktr",
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
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Security",
    ],
    packages=find_packages(include=["pof", "pof.*"]),
    install_requires=install_requires,
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "pof=pof.cli:_cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
