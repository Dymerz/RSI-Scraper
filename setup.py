import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rsi-scrapper",
    version="0.6.7",
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
    python_requires='>=3.6',
)