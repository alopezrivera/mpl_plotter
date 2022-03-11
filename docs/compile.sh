#!/bin/bash

find . -name 'mpl_plotter*rst' -delete
make clean
make latex
find . -name 'mpl_plotter*rst'
find . -name 'mpl_plotter*rst' -delete

cd build
cd latex
make LATEXMKOPTS="-lualatex"