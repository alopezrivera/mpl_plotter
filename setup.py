import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpl_plotter",
    version="4.1.0.post4",
    author="Antonio Lopez Rivera",
    author_email="antonlopezr99@gmail.com",
    description="Matplotlib-based plotting library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonlopezr/mpl_plotter",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scikit-image",
        "pandas",
        "PyQt5",
        "Python-Alexandria>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
