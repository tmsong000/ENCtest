from osgeo import ogr
import geopandas as gpd
import os

gpkg_file_path = "C:/WORK/US_ENC_EXPORT_250724/all/ENC6118/export_gpkg/results/merge.gpkg"

# 'Final'이라는 출력 폴더 생성
base_folder = os.path.dirname(gpkg_file_path)
output_folder = os.path.join(base_folder, "Final")
os.makedirs(output_folder, exist_ok=True)

gpkg_ds = ogr.Open(gpkg_file_path)
num_layers = gpkg_ds.GetLayerCount()

for i in range(num_layers):
    layer = gpkg_ds.GetLayerByIndex(i)
    table_name = layer.GetName()
    
    print(f"처리 중: {table_name}")
    
    gdf = gpd.read_file(gpkg_file_path, layer=table_name)
    
    if not isinstance(gdf, gpd.GeoDataFrame):
        print(f"⚠️ {table_name}은 GeoDataFrame이 아님 (일반 DataFrame 반환됨)")
        continue
    if gdf.geometry.isnull().all():
        print(f"⚠️ {table_name}의 geometry 컬럼이 모두 비어 있음")
        continue
    
    output_file_path = os.path.join(output_folder, f"{table_name}.gpkg")
    gdf.to_file(output_file_path, driver="GPKG")
    print(f"✅ 저장 완료: {output_file_path}")

gpkg_ds = None
