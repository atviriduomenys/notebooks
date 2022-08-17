#!zsh

# Duomenų rinkinys
# https://data.gov.lt/dataset/eismo-ivykiu-ivykusiu-lietuvos-respublikoje-kuriu-metu-zuvo-ir-ar-buvo-suzeisti-zmones-duomenys

# Struktūros aprašas
# https://github.com/atviriduomenys/manifest/blob/master/datasets/gov/pd/eiis.csv

git clone https://github.com/atviriduomenys/manifest.git
cd manifest/datasets/gov
spinta copy \
    rc/ar/apskritis.csv \
    rc/ar/savivaldybe.csv \
    rc/ar/seniunija.csv \
    rc/ar/gyvenamojivietove.csv \
    rc/ar/gatve.csv \
    rc/ar/patalpa.csv \
    rc/ar/pastatas.csv \
    lakd/keliai.csv \
    regitra/tp.csv \
    pd/eiis.csv \
    -o eiis.xlsx

# Atsisiunčiame duomenis
http -b 'https://data.gov.lt/public/api/1/action/package_search?q=title:"Eismo įvykių, įvykusių Lietuvos Respublikoje, kurių metu žuvo ir (ar) buvo sužeisti žmonės, duomenys"' | jq -r "
.result.results[].resources[].url
"

dists=(
    "https://data.gov.lt/dataset/509/download/10097/EI_2018 12 31.json"
    "https://data.gov.lt/dataset/509/download/10096/EI_2017 12 31.json"
    "https://data.gov.lt/dataset/509/download/10095/EI_2016 12 31.json"
    "https://data.gov.lt/dataset/509/download/10094/EI_2015 12 31.json"
    "https://data.gov.lt/dataset/509/download/10100/EI_2013 12 31.json"
    "https://data.gov.lt/dataset/509/download/10099/EI_2020 12 31.json"
    "https://data.gov.lt/dataset/509/download/10098/EI_2019 12 31.json"
    "https://data.gov.lt/dataset/509/download/10093/EI_2014 12 31.json"
)
mkdir data
for dist in $dists; do
    http -db "$dist" -o "data/$(basename $dist)"
done

du -sh data/*.json
#| 85M     data/EI_2013 12 31.json
#| 80M     data/EI_2014 12 31.json
#| 81M     data/EI_2015 12 31.json
#| 85M     data/EI_2016 12 31.json
#| 83M     data/EI_2017 12 31.json
#| 97M     data/EI_2018 12 31.json
#| 111M    data/EI_2019 12 31.json
#| 89M     data/EI_2020 12 31.json

head "data/EI_2013 12 31.json"

# Įsidiegiame priemones skirtas duomenų analizei
python -m venv .venv
source .venv/bin/activate
pip install dask pandas geopandas geoplot folium matplotlib mapclassify

python
import webbrowser
import pandas as pd
import geopandas as gp
import geoplot as gplt
import dask.dataframe as dd
import matplotlib.pyplot as plt

# Užkrauname visus duomenų failus.
df = dd.read_json('data/EI_*.json', orient='records', lines=False).compute()

df.shape
#| (182222, 52)

df.info()

# Sutvarkome duomenų tipus:

#| 1   dataLaikas                    182222 non-null  object
df['dataLaikas'] = pd.to_datetime(df['dataLaikas'])

#| 2   registravimoData              182222 non-null  object
df['registravimoData'] = pd.to_datetime(df['registravimoData'])

#| 3   paskutinioRedagavimoLaikas    181228 non-null  object
df['paskutinioRedagavimoLaikas'] = pd.to_datetime(df['paskutinioRedagavimoLaikas'])

# Kokia eismo įvykių tendencija laike?
df_ = df.set_index('dataLaikas')['registrokodas'].resample('D').count()
ax = df_.plot(alpha=.5)
df_.rolling(30, center=True).mean().plot(ax=ax, grid=True)
plt.show(); plt.close()


#| 48  ilguma                        160550 non-null  float64
#| 49  platuma                       160550 non-null  float64
# Kodėl kai kurie eismo įvykiai neturi koordinačių?
df_ = df.dropna(subset=['platuma', 'ilguma'])
gdf = gp.GeoDataFrame(df_, geometry=gp.points_from_xy(df_['platuma'], df_['ilguma'], crs=3346))

gdf.head(1).T

# Koks yra unikalių reikšmių pasiskirstymas?
df.nunique().sort_values(ascending=False)
arr = [
    'kitosOroSalygos',
    'kitiNuliamentysVeiksniai',
    'eismoDalyviai',
    'eismoTranspPreimone',
]
df[[c for c in df if c not in arr]].nunique().sort_values(ascending=False)

#| ilguma     160550 non-null  float64
#| platuma    160550 non-null  float64
#| geometry   124742
# Pasirodo yra nemažai eismo įvykių, kurie paseitaikė identiškai toje pačioje vietoje.
gdf['geometry'].value_counts().head(10)
# Įdomu, kokios tai vietos?
gdf_ = gdf['geometry'].value_counts().head(10).reset_index()[1:]
gdf_ = gp.GeoDataFrame(gdf_, geometry='index').set_crs(3346).to_crs(4326)
gdf_.explore(marker_kwds={'radius': 10}).save('map.html')
webbrowser.open('map.html')

# Įdomu, kur bendrai yra įvykę eismo įvykiai?

# Norint atvaizduoti duomenis žemėlapyje pirmiausia užsikraunam RC AR duomenis.
# https://data.gov.lt/dataset/adresu-registro-savivaldybiu-erdviniai-duomenys
sav = gp.read_file('https://www.registrucentras.lt/aduomenys/?byla=adr_gra_savivaldybes.json')

ax = sav.plot(color='none', edgecolor='steelblue')
gdf.plot(alpha=.1, color='red', markersize=.1, ax=ax); plt.show(); plt.close()

gdf['zuvusiuSkaicius'].value_counts()
ax = sav.plot(color='none', edgecolor='steelblue')
gdf[gdf['zuvusiuSkaicius'] > 0].plot(alpha=.2, color='red', markersize=20, ax=ax); plt.show(); plt.close()
