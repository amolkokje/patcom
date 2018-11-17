import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="patcom",
    version="0.0.1",
    author="Amol Kokje",
    author_email="amolkokje@gmail.com",
    description="Python modules for ATE pattern compression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amolkokje/patcom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)