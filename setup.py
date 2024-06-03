import platform
from io import open

from setuptools import (
    find_packages,
    setup,
)

requested_libs = [
    "yagmail==0.15.293",
    "requests==2.32.3",
    "twilio==9.1.0",
    "python-telegram-bot==21.2",
    "keyring==25.2.1",
]

if platform.system() == "Windows":
    requested_libs.append("win11toast==0.34")

setup(
    name="knock-knock",
    version="0.1.0",
    description="Be notified when your want with only two additional lines of code",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UdsonWillams/knock-knock",
    author="Udson Willams",
    author_email="udson.willams@gmail.com",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["knockknock = knockknock.__main__:main"]},
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=requested_libs,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
