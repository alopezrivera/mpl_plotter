import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpl_plotter",
    version="5.4.0",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Publication-quality data representation library based on Matplotlib. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alopezrivera/mpl_plotter",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.19.5",
        "pandas>=1.1.5",
        "matplotlib>=3.5.2",
        "toml>=0.10.1",
        "PyQt5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
