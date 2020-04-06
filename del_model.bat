@echo off
cd models
del "%1.h5"
cd ../graphs
del "%1-scores.png"
cd ..