import re

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("rsi_scrapper/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setuptools.setup(
    name="rsi-scrapper",
    version=version,
    author="Urbain Corentin",
    author_email="corentin.urbain@gmail.com",
    description="Web scapper for RSI",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.25.1',
        'lxml>=4.6.2',
    ]
)
