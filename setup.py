import re

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("rsi_scraper/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setuptools.setup(
    name="rsi-scraper",
    version=version,
    author="Urbain Corentin",
    url="https://github.com/Dymerz/RSI-Scraper",
    description="Web scaper for RSI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/Dymerz/RSI-Scraper/issues",
        "Chat": "https://github.com/Dymerz/RSI-Scraper/discussions"
    },
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='starcitizen robertsspaceindustries rsi scraper scraping',
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.25.1',
        'lxml>=4.6.3',
    ]
)
