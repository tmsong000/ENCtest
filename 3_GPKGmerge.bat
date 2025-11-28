@echo off
setlocal enabledelayedexpansion

set "base_dir=%~dp0"
cd "%base_dir%export_gpkg\results"

if exist merge.gpkg del merge.gpkg

for %%A in (*.gpkg) do (
    echo appending %%A
    ogr2ogr -f GPKG -update -append merge.gpkg "%%A"
)

echo All processing completed.