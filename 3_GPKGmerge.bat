@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
cd support\results
for %%A IN (*.gpkg) DO (
    set "datasetName=%%~nA"
    ogr2ogr -f GPKG -update -append merge.gpkg "%%A"
    echo processing "%%A"
)

echo All processing completed.