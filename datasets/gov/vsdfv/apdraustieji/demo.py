# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

#pertvarkyti percentges

# %% [markdown]
# Duomenų rinkiniai:
#
# 1. Apdraustieji
#    https://data.gov.lt/dataset/apdraustieji

# %%
http -bd https://atvira.sodra.lt/downloads/lt-eur/apdraustieji_ketv.zip

#| Done. 177.4 kB in 00:0.11224 (1.6 MB/s)

# %% [markdown]
# 2. Socialinio draudimo įmokos
#    https://data.gov.lt/dataset/socialinio-draudimo-pensijos

# %% 
http -bd https://atvira.sodra.lt/downloads/lt-eur/apdraustieji_ketv.zip

# %% [markdown]
# 3. Vidutinės apdraustųjų pajamos.
#    https://data.gov.lt/dataset/vidutines-apdraustuju-pajamos

# %%
http -bd https://atvira.sodra.lt/downloads/lt-eur/apdraustieji_det.zip
#| Done. 5.4 MB in 00:0.56334 (9.6 MB/s)

# %%
http -bd https://atvira.sodra.lt/downloads/lt-eur/apdraustuju_pajamu_analize.zip
#| Done. 6.6 MB in 00:0.64270 (10.3 MB/s)

# %%
http -bd https://atvira.sodra.lt/csv/lt-eur/apdraustieji_6_5.csv
#| Done. 90.7 MB in 00:7.77662 (11.7 MB/s)

# %% [markdown]
# Norint atvaizduoti duomenis žemėlapyje pirmiausia užsikraunam RC AR duomenis.
# https://data.gov.lt/dataset/adresu-registro-savivaldybiu-erdviniai-duomenys

# %% 
sav = gp.read_file('https://www.registrucentras.lt/aduomenys/?byla=adr_gra_savivaldybes.json')

# %% 
unzip apdraustieji_ketv.zip
unzip apdraustieji_det.zip
unzip apdraustuju_pajamu_analize.zip
cat skaityti.txt

# %%
du -sh *.csv
#| 87M     apdraustieji_6_5.csv
#| 113M    apdraustieji_det.csv
#| 2,8M    apdraustieji_ketv.csv
#| 56M     apdraustuju_pajamu_analize.csv

# %% 
wc -l *.csv

# %% 
poetry init -n
poetry add pandas geopandas matplotlib
poetry run python

# %%
import pandas as pd

# %% [markdown]
# Užsikraunam duomenis
# ********************

# %% [markdown]
# 1. Apdraustieji
# %% 
apdraustieji = pd.read_csv('apdraustieji_ketv.csv', encoding='cp1257', sep=';')

# %% [markdown]
# 2. Socialinio draudimo įmokos

# %% [markdown]
# 3. Vidutinės apdraustųjų pajamos.

# %%
apdraustieji_det = pd.read_csv('apdraustieji_det.csv', encoding='cp1257', sep=';')
pajamu_analize = pd.read_csv('apdraustuju_pajamu_analize.csv', encoding='cp1257', sep=';')
pajamos = pd.read_csv('apdraustieji_6_5.csv', encoding='cp1257', sep=';')

# %% [markdown]
# Apsižvalgom
# ***********

# %% [markdown]
# 1. Apdraustieji

# %%
apdraustieji.info()
#| RangeIndex: 9625 entries, 0 to 9624
#| Data columns (total 12 columns):
#|  #   Column                      Non-Null Count  Dtype
#| ---  ------                      --------------  -----
#|  0   METAI                       9625 non-null   float64
#|  1   KETVIRTIS                   9625 non-null   float64
#|  2   APDR_KATEG_GRUPE            9625 non-null   object
#|  3   APDR_KATEG_RUSIS            9625 non-null   object
#|  4   APDR_KATEG_PORUSIS          7833 non-null   object
#|  5   APDR_KATEG_TIPAS            5175 non-null   object
#|  6   DRAUDEJO_GRUPE              9625 non-null   object
#|  7   DRAUDEJO_TIPAS              9189 non-null   object
#|  8   PRISK_SUMA_EUR              6410 non-null   float64
#|  9   SUMOKETA_EUR                6403 non-null   float64
#|  10  VID_A_DARBO_APMOK_SUMA_EUR  5339 non-null   float64
#|  11  VID_B_APDRAUSTUJU_SK        9625 non-null   float64
#| dtypes: float64(6), object(6)
#| memory usage: 902.5+ KB

# %%
apdraustieji.nunique()
#| METAI                           14
#| KETVIRTIS                        4
#| APDR_KATEG_GRUPE                 3
#| APDR_KATEG_RUSIS                17
#| APDR_KATEG_PORUSIS              31
#| APDR_KATEG_TIPAS                12
#| DRAUDEJO_GRUPE                   2
#| DRAUDEJO_TIPAS                  27
#| PRISK_SUMA_EUR                2776
#| SUMOKETA_EUR                  2746
#| VID_A_DARBO_APMOK_SUMA_EUR    5143
#| VID_B_APDRAUSTUJU_SK          3824

# %%
apdraustieji.head(2).T
#|                                                                             0                                                  1
#| METAI                                                                  2009.0                                             2009.0
#| KETVIRTIS                                                                 1.0                                                1.0
#| APDR_KATEG_GRUPE                        1. Asmenys, už kuriuos mokamos įmokos              1. Asmenys, už kuriuos mokamos įmokos
#| APDR_KATEG_RUSIS            1.1. Asmenys, draudžiami visų rūšių valstybini...  1.1. Asmenys, draudžiami visų rūšių valstybini...
#| APDR_KATEG_PORUSIS                                                        NaN                                                NaN
#| APDR_KATEG_TIPAS                                                          NaN                                                NaN
#| DRAUDEJO_GRUPE                                Valstybės, biudžetinės įstaigos                    Valstybės, biudžetinės įstaigos
#| DRAUDEJO_TIPAS                                           05. Valstybės įmonės                           25. Biudžetinės įstaigos
#| PRISK_SUMA_EUR                                                        16804.8                                           179760.0
#| SUMOKETA_EUR                                                          15760.1                                           141951.3
#| VID_A_DARBO_APMOK_SUMA_EUR                                         42012404.7                                        449664104.8
#| VID_B_APDRAUSTUJU_SK                                                 17693.98                                          249955.08

# %% [markdown]
# 2. Socialinio draudimo įmokos

# %% [markdown]
# 3. Vidutinės apdraustųjų pajamos.

# %%
apdraustieji_det.info()
#| RangeIndex: 554490 entries, 0 to 554489
#| Data columns (total 10 columns):
#|  #   Column             Non-Null Count   Dtype
#| ---  ------             --------------   -----
#|  0   AGREGAVIMAS        554490 non-null  object
#|  1   METU_MENUO         554490 non-null  object
#|  2   APDRAUSTUJU_RUSIS  554490 non-null  object
#|  3   DRAUDEJO_GRUPE     5014 non-null    object
#|  4   DRAUDEJO_TIPAS     19876 non-null   object
#|  5   SAVIVALDYBE        466239 non-null  object
#|  6   LYTIS              313332 non-null  object
#|  7   AMZIUS             42459 non-null   object
#|  8   DARBO_UZMOK_EUR    155812 non-null  float64
#|  9   APDR_ASM_SK        554490 non-null  float64
#| dtypes: float64(2), object(8)
#| memory usage: 42.3+ MB

# %%
apdraustieji_det.nunique()
#| AGREGAVIMAS               8
#| METU_MENUO              148
#| APDRAUSTUJU_RUSIS        36
#| DRAUDEJO_GRUPE            2
#| DRAUDEJO_TIPAS           27
#| SAVIVALDYBE              61
#| LYTIS                     3
#| AMZIUS                   20
#| DARBO_UZMOK_EUR      114736
#| APDR_ASM_SK           21802

# %%
apdraustieji_det.head(2).T
#|                                                                    0                                                  1
#| AGREGAVIMAS                        Draudėjų grupė, apdraustųjų rūšys                  Draudėjų grupė, apdraustųjų rūšys
#| METU_MENUO                                              2010-01 mėn.                                       2010-01 mėn.
#| APDRAUSTUJU_RUSIS  Apdraustieji visomis valstybinio socialinio dr...  Apdraustieji visomis valstybinio socialinio dr...
#| DRAUDEJO_GRUPE                                        Kiti draudėjai                    Valstybės, biudžetinės įstaigos
#| DRAUDEJO_TIPAS                                                   NaN                                                NaN
#| SAVIVALDYBE                                                      NaN                                                NaN
#| LYTIS                                                            NaN                                                NaN
#| AMZIUS                                                           NaN                                                NaN
#| DARBO_UZMOK_EUR                                         406526120.44                                       127385656.89
#| APDR_ASM_SK                                                 914052.0                                           346662.0

# %%
pajamu_analize.info()
#| RangeIndex: 1152984 entries, 0 to 1152983
#| Data columns (total 6 columns):
#|  #   Column           Non-Null Count    Dtype
#| ---  ------           --------------    -----
#|  0   metai            1152984 non-null  float64
#|  1   mėnuo            1152984 non-null  float64
#|  2   amžius           1152984 non-null  float64
#|  3   lytis            1152984 non-null  object
#|  4   savivaldybe      1152984 non-null  object
#|  5   mėnesio pajamos  1152984 non-null  float64
#| dtypes: float64(4), object(2)
#| memory usage: 52.8+ MB

# %%
pajamu_analize.nunique()
#| metai                   1
#| mėnuo                   1
#| amžius                 85
#| lytis                   2
#| savivaldybe            61
#| mėnesio pajamos    304717

# %%
pajamu_analize.head(2).T
#|                                 0                 1
#| metai                      2022.0            2022.0
#| mėnuo                         4.0               4.0
#| amžius                       53.0              54.0
#| lytis                     Moteris             Vyras
#| savivaldybe      Vilniaus m. sav.  Vilniaus m. sav.
#| mėnesio pajamos             444.0           1470.05

# %%
pajamos.info()
#| RangeIndex: 799592 entries, 0 to 799591
#| Data columns (total 6 columns):
#|  #   Column           Non-Null Count   Dtype
#| ---  ------           --------------   -----
#|  0   METAI            799592 non-null  float64
#|  1   MENUO            799592 non-null  float64
#|  2   EVR_PAVADINIMAS  799592 non-null  object
#|  3   PROFESIJA        799592 non-null  object
#|  4   APDR_SK          799592 non-null  float64
#|  5   VID_PAJAMOS      787978 non-null  float64
#| dtypes: float64(4), object(2)
#| memory usage: 36.6+ MB

# %%
pajamos.nunique()
#| METAI                   3
#| MENUO                  12
#| EVR_PAVADINIMAS       946
#| PROFESIJA             431
#| APDR_SK              3051
#| VID_PAJAMOS        258992

# %%
pajamos.head(2).T
#|                                                           0                                                  1
#| METAI                                                2020.0                                             2020.0
#| MENUO                                                  12.0                                               12.0
#| EVR_PAVADINIMAS                     Kitos įrangos įrengimas     Azartinių lošimų ir lažybų organizavimo veikla
#| PROFESIJA        7412 Elektromechanikai ir elektromonteriai  4212 Lažybų tarpininkai, lošimo namų tarnautoj...
#| APDR_SK                                                67.0                                              400.0
#| VID_PAJAMOS                                         1756.61                                             601.36
