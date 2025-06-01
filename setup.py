# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyfoxpro-ide",
    version="0.1.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="Un IDE moderne pour Python inspiré de Visual FoxPro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eddymaue/Vfp2python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Integrated Development Environments (IDE)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.5.0",
    ],
    entry_points={
        "console_scripts": [
            "pyfoxpro=main:main",
        ],
    },
)