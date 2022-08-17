# https://data.gov.lt/dataset/covid-19-duomenys

# Atsisiunčiame duomenų struktūros aprašą
http -bd https://data.gov.lt/dataset/1670/structure/Covid19.csv -o adsa.csv

# Convertuojame struktūros aprašą į skaitomesnį formatą
pip install spinta
spinta copy adsa.csv -o adsa-orig.xlsx

# Atsisniučiame savivaldybių duomenis
# https://data.gov.lt/dataset/adresu-registro-savivaldybiu-erdviniai-duomenys
http -bd https://data.gov.lt/dataset/1345/structure/UTF8_1345.csv -o adsa-sav.csv
http -bd https://www.registrucentras.lt/aduomenys/?byla=adr_gra_savivaldybes.json
# https://data.gov.lt/dataset/adresu-registro-apskriciu-erdviniu-duomenys
http -bd https://data.gov.lt/dataset/1344/structure/UTF8_1344.csv -o adsa-aps.csv
http -bd https://www.registrucentras.lt/aduomenys/?byla=adr_gra_apskritys.json

# Atsisiunčiame gyventojų duomenis
# https://data.gov.lt/dataset/gyventoju-registro-duomenys-apie-lietuvos-gyventoju-amziu-ir-lyti-pagal-savivaldybes
http -bd https://www.registrucentras.lt/aduomenys/?byla=01_gr_open_amzius_lytis_pilietybes_sav_r1.csv
wc -l 01_gr_open_amzius_lytis_pilietybes_sav_r1.csv

spinta copy adsa-sav.csv adsa-aps.csv adsa.csv -o adsa.xlsx

# Kokie duomenys yra prieinami?
http -b https://get.data.gov.lt/datasets/gov/lsd/covid19/ | jq -r '._data[].name'

# Atsisiunčiame visus duomenis.
models=(
    datasets/gov/lsd/covid19/AtvejaiIrMirtys
    datasets/gov/lsd/covid19/AtvejaiPagalDarbovietes
    datasets/gov/lsd/covid19/DarbovieciuImunizacija
    datasets/gov/lsd/covid19/LaboratorijuRezultataiEvrk
    datasets/gov/lsd/covid19/LigoniniuDuomenys
    datasets/gov/lsd/covid19/MokiniuImunizacija
    datasets/gov/lsd/covid19/NeigaliujuStatistika
    datasets/gov/lsd/covid19/StudVakcPagalIstaigas
    datasets/gov/lsd/covid19/StudVakcPagalIstaigasIrProgramas
    datasets/gov/lsd/covid19/SvieslenciuStatistika
    datasets/gov/lsd/covid19/TyrimaiPadieniui
    datasets/gov/lsd/covid19/Vakcinavimas
)
for model in $models; do
    http -bd https://get.data.gov.lt/$model/:format/csv -o $(basename $model).csv
done

# Kiek disko vietos užima visi duomenys?
du -sh *.csv | sort -rh

# Kiek eilučių yra kiekviename duomenų faile?
wc -l *.csv | sort -rn

python

import pandas as pd

# Užsikraunam duomenis.
atvejai = pd.read_csv('AtvejaiIrMirtys.csv')

# Peržiūrim duomenų sudėtį.
atvejai.info()
atvejai.nunique()

atvejai['sex'].value_counts()
atvejai['age_gr'].value_counts()

# Patikrinam ar įmanoma duomenis sujungti pagal savivaldybių pavadinimus
atvejai['municipality_name'].value_counts()
sav_counts = atvejai['municipality_name'].value_counts()
sav_counts = atvejai.groupby('municipality_name')['new_cases'].sum()
sav_counts

import geopandas as gp

sav = gp.read_file('adr_gra_savivaldybes.json')
sav.info()
sav['SAV_PAV'].head()

sav_counts.head()

df = sav.join(sav_counts, on='SAV_PAV')
df.info()
df = df.rename(columns={'new_cases': 'cases'})
df.info()


# Atvaizduojame duomenis ant žemėlapio
df.plot('cases', legend=True)
import matplotlib.pyplot as plt
plt.show()
plt.close()


# Procentas sergančių nuo visos populiacijos

gyv = pd.read_csv('01_gr_open_amzius_lytis_pilietybes_sav_r1.csv')
gyv.info()
gyv.nunique()

gyv['sav_pavadinimas'].head()
gyv['sav_pavadinimas'].value_counts()

gyv['sav_pavadinimas'].value_counts().to_frame().join(
    atvejai['municipality_name'].value_counts()
).head()

df = gyv['sav_pavadinimas'].value_counts().to_frame().join(
    atvejai.groupby('municipality_name')['new_cases'].sum()
).rename(columns={
    'sav_pavadinimas': 'viso',
    'new_cases': 'atvejai',
})

df['atvejai'] / df['viso'] * 100
df['proc'] = df['atvejai'] / df['viso'] * 100

sav.join(df, on='SAV_PAV').plot('proc', legend=True)
plt.show()
