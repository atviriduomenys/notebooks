# https://data.gov.lt/dataset/zemelapiu-nomenklaturiniu-lapu-tinkleliai
# https://www.geoportal.lt/download/Specifikacijos/Nomenklaturiniu_lapu_tinkleliai_specifikacija_1v.pdf

wget https://www.geoportal.lt/download/opendata/Nomenklat_lapai/Nomenklaturiniai_lapai.zip
unzip Nomenklaturiniai_lapai.zip
ls
#| Baltija-93
#| KS-1942
#| KS-1963
#| LKS-94
#| UTM

poetry init -n
poetry add pandas geopandas matplotlib
poetry run python

import geopandas as gp

df = gp.read_file('LKS-94/LKS_94_500.shp')
df.info()
#| RangeIndex: 1,112,800 entries, 0 to 1112799
#| Data columns (total 10 columns):
#|  #   Column      Non-Null Count    Dtype
#| ---  ------      --------------    -----
#|  0   CENTROID_X  1112800 non-null  float64
#|  1   CENTROID_Y  1112800 non-null  float64
#|  2   NOM05K      1112800 non-null  object
#|  3   NOM1K       1112800 non-null  object
#|  4   NOM2K       1112800 non-null  object
#|  5   NOM5K       1112800 non-null  object
#|  6   NOM10K      1112800 non-null  object
#|  7   Shape_Leng  1112800 non-null  float64
#|  8   Shape_Area  1112800 non-null  float64
#|  9   geometry    1112800 non-null  geometry
#| dtypes: float64(4), geometry(1), object(5)
#| memory usage: 84.9+ MB

df.nunique()
#| CENTROID_X       1520
#| CENTROID_Y       1160
#| NOM05K        1112800
#| NOM1K          278200
#| NOM2K           69550
#| NOM5K           11128
#| NOM10K           2782
#| Shape_Leng          1
#| Shape_Area          1
#| geometry      1112800
#| dtype: int64
