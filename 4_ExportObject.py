import os
import geopandas as gpd
from osgeo import ogr

base_dir = os.path.dirname(os.path.abspath(__file__))
gpkg_file = os.path.join(base_dir, "export_gpkg", "results", "merge.gpkg")

output_dir = os.path.join(base_dir, "export_gpkg", "results", "Final")
os.makedirs(output_dir, exist_ok=True)

ds = ogr.Open(gpkg_file)
for i in range(ds.GetLayerCount()):
    layer = ds.GetLayerByIndex(i)
    name = layer.GetName()
    gdf = gpd.read_file(gpkg_file, layer=name)

    if not gdf.geometry.isnull().all():
        gdf.to_file(os.path.join(output_dir, f"{name}.gpkg"), driver="GPKG")
        print(f"Saved {name}")

print("STEP4 complete")
