1번코드: OSGeo4W Shell 로 실행, 파일을 전자해도 경로에 넣고 실행하면 "전자해도 경로/export_gpkg" 에 파일 저장됨

2번코드: QGIS 실행 후 python console 로 실행, 코드에서 input_dir = r"전자해도 경로/export_gpkg" 를 수정, 경로는 \말고 /를 사용, 경로를 수정하여 실행하면 수정한경로/results 폴더속에 파일 생성

3번코드: OSGeo4W Shell 로 실행, 2번 코드의 result 폴더 속에 3번 코드를 넣고, OSGeo4W Shell로 실행하면 같은 경로에 merge.gpkg 생성됨

4번코드: QGIS python console로 실행, 코드에서 merge.gpkg 경로(예: gpkg_file_path = "C:/ENC/export_gpkg/results/merge.gpkg") 를 수정하고, 실행하면, Final이라는 폴더가 생성되어 전자해도 객체가 저장됨
