@echo off
setlocal enabledelayedexpansion

rem 결과를 저장할 폴더
set "output_dir=export_gpkg"

rem 폴더가 없으면 생성
if not exist "%output_dir%" (
    mkdir "%output_dir%"
)

rem 변환할 파일들의 목록을 가져옵니다.
for %%f in (KR*.000) do (
    echo Converting %%~nf.000 to %output_dir%\%%~nf.gpkg

    rem ogr2ogr로 파일을 GeoPackage으로 변환합니다.
    ogr2ogr -f "GPKG" -update -append "%output_dir%\%%~nf.gpkg" "%%f"
)

echo Conversion completed.
