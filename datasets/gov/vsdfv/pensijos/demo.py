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

# %% [markdown]
# Socialinio draudimo pensijos
# *****************

# %% [markdown]
# https://data.gov.lt/dataset/socialinio-draudimo-pensijos

# %% [markdown]
# Duomenų nuskaitymas
# ********************

# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
from pathlib import Path
from matplotlib.ticker import StrMethodFormatter

# %%
data_dir = Path().resolve().parents[3] / 'data'
data_dir

# %%
import zipfile
with zipfile.ZipFile(data_dir / 'datasets/gov/vsdfv/pensijos/pensijos.zip', 'r') as zip_ref:
    zip_ref.extractall(data_dir / 'datasets/gov/vsdfv/pensijos/sodrapensijos') # PERVADINTI

# %%
# Koduočių ir skirtuko problema, todėl naudojame papildomas komandas encoding ir sep.
pensijos = pd.read_csv(data_dir / 'datasets/gov/vsdfv/pensijos/sodrapensijos/pensijos.csv', encoding='cp1257', sep=';')

# %% [markdown]
# Duomenų apžvalga
# ***********

# %%
pensijos.info()

# %%
pensijos.nunique()

# %%
pensijos.head().T

# %%
# Neteisingas datos formatas, todėl pridedame naują kintamąjį 'LAIKAS' su teisingu datos formatu
pensijos['LAIKAS'] = pd.to_datetime(pensijos['METU_MENUO'], format = '%Y-%m mėn.') 

# %%
# Kodėl 'PENSIJOS_PORUSIS' išskirta būtent ta grupė 'Našliai iki  95-01-01', 'Našliai po  95-01-01' Koks ivykis 1995 m.? Ką reiškia rūšis '-' ?
pensijos['PENSIJOS_PORUSIS'].unique()

# %%
# Kodėl 'NET_DARB_GRUPE' grupės išskiriamos dviem būdais : ir procentais, ir grupėmis.
pensijos['NET_DARB_GRUPE'].unique()

# %%
# Pridedame naują kintamąjį 'VIDURKIS', kuris leis mums atlikti informatyvesnius skaičiavimus
pensijos['VIDURKIS'] = pensijos['PRISK_SUMA_EUR']/pensijos['GAVEJU_SK']

# %% [markdown]
# DUOMENŲ ANALIZĖ
# *********************

# %%
# Kokia pensijų rūšis yra populiariausia?
mpl.rc('figure', figsize=(20,5))
temp_df = round((pensijos.groupby('PENSIJOS_RUSIS')['GAVEJU_SK'].sum().sort_values(ascending=False) 
           / pensijos.groupby('PENSIJOS_RUSIS')['GAVEJU_SK'].sum().sort_values(ascending=False).sum())*100,1)
ax = temp_df.plot(kind='bar', rot = 45)
ax.bar_label(ax.containers[0])
plt.ylabel('PROCENTAI')
plt.show()

# %%
#Senatvės pensijų išmokų gavėjų skaičius pagal lytį:
pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].groupby('LYTIS')['GAVEJU_SK'].sum().plot(kind = 'pie', autopct='%1.0f%%')
pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].groupby('LYTIS')['GAVEJU_SK'].sum().to_frame()

# %%
# Vidutinis senatvės pensijų dydis pagal lytį:
pd.options.display.float_format = '{:,.2f}'.format
pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].groupby('LYTIS')['PRISK_SUMA_EUR'].sum()/pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].groupby('LYTIS')['GAVEJU_SK'].sum()

# %%
# Vidutinių senatvės pensijų dydžių (pagal lytį) skirtumas procentais:
round(((459.48 - 386.11) / 459.38 ) * 100)

# %%
# Kokia suma senatvės pensijų išmokama per metus?
pd.options.display.float_format = '{:,.2f}'.format
pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].set_index('LAIKAS').resample('Y')['PRISK_SUMA_EUR'].sum()

# %%
# Kokia suma senatvės pensijų išmokama kas mėnesį?
mpl.rc('figure', figsize=(20,5))
ax = pensijos.set_index('LAIKAS').resample('M')['PRISK_SUMA_EUR'].sum().plot(grid = True, c = 'y')
ax.yaxis.set_major_formatter(StrMethodFormatter( '{x:,.0f}'))
plt.ylabel('PRISK_SUMA_EUR')
plt.show()
#kiekvienais metais sausį įvyksta pakilimas

# %%
# Koks yra senatvės pensijų gavėjų skaičius kas mėnesį?
mpl.rc('figure', figsize=(20,5))
ax = pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].set_index('LAIKAS').resample('M')['GAVEJU_SK'].sum().plot(grid = True, c = 'y')
ax.yaxis.set_major_formatter(StrMethodFormatter( '{x:,.0f}'))
plt.ylabel('GAVEJU_SK')
plt.show()
# Kodėl kiekvienais metais įvyksta pakilimas prieš metų pabaigą?

# %%
# Senatvės pensijos dydžio pasiskirtymas pagal lytį: 
mpl.rc('figure', figsize=(20,5))
sns.histplot(data =pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'], x = 'VIDURKIS', hue = 'LYTIS', kde = True)
plt.show()

# %%
# Senatvės pensijos dydzio pasiskirtymas pagal tai, ar pensijos gavėjas turi stažą, ar ne:
sns.histplot(data = pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'], x = 'VIDURKIS', hue = 'AR_TURI_STAZA', kde = True)
plt.show()

# %%
# Vidutinis senatvės pensijų dydis pagal tai, ar pensijos gavėjas turi stažą:
pd.options.display.float_format = '{:,.2f}'.format
pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].groupby('AR_TURI_STAZA')['PRISK_SUMA_EUR'].sum()/pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'].groupby('AR_TURI_STAZA')['GAVEJU_SK'].sum()

# %%
# Vidutinių senatvės pensijų dydžių (pagal tai, ar pensijos gavėjas turi stažą) skirtumas procentais:
round(((433.13 - 238.89) / 433.13 ) * 100)

# %% [markdown]
# PAPILDOMAI (iš "Socialinio draudimo pensijos")
# **********

# %%
# Senatvės pensijos vidurkių pasiskirstymas pagal lytį ir amžių:
sns.catplot(data=pensijos[pensijos['PENSIJOS_RUSIS'] == '01. Senatvės pensijos'], x='AMZIUS', y='VIDURKIS', hue='LYTIS', sharey=False, kind = 'strip', height=10)

# %%
# Netekto darbingumo grupės pagal gyventojų skaičių:
mpl.rc('figure', figsize=(30,5))
pagal_grupe = pensijos.groupby('NET_DARB_GRUPE')['GAVEJU_SK'].sum()
plt.ticklabel_format(style = 'plain')
plt.xlabel('GAVEJU_SK')
pagal_grupe.plot.barh(color = 'y').legend(labels=['Dažnis'])

# %%
# Gaunamų pensijų vidurkių pasiskirstymas pagal lytį ir netekto darbingumo grupę:
sns.catplot(data= pensijos, x='NET_DARB_GRUPE', y='VIDURKIS', hue='LYTIS', kind = 'bar', height=10)

# %% [markdown]
# PAPILDOMAI (iš "Vidutinės apdraustųjų pajamos : Apdraustųjų pajamų analizė")'
# ****************************

# %% [markdown]
# https://data.gov.lt/dataset/vidutines-apdraustuju-pajamosimport

# %%
import zipfile
with zipfile.ZipFile(data_dir / 'datasets/gov/vsdfv/vap/apdraustuju_pajamu_analize.zip', 'r') as zip_ref:
    zip_ref.extractall(data_dir / 'datasets/gov/vsdfv/vap') # PERVADINTI

# %%
# pajamu_analize = pd.read_csv(data_dir / 'datasets/gov/vsdfv/vap/PajamuAnalize.csv', encoding='cp1257', sep=';')

# %%
pajamu_analize.info()

# %%
pajamu_analize.nunique()

# %%
pajamu_analize.head().T

# %%
pajamu_analize['laikas'] = pd.to_datetime(pajamu_analize['metai'], format = '%Y')# ?????????????
# pajamu_analize['laikas'] = pd.to_datetime(pajamu_analize['mėnuo'], format = '%m')# ?????????????
# pakeisti menesi ir amziu

# %%
pajamu_analize

# %%
# Vidutinis pajamų dydis pagal lytį: 
pajamu_analize.groupby('lytis')['mėnesio pajamos'].mean()

# %%
# Vidutinių pajamų dydžių (pagal lytį) skirtumas procentais:
round(((1861.43 - 1624.18) / 1861.43 ) * 100)


# %%
# Iš stulpelio 'amžius' reikšmių sudarome naują stulpelį 'grupe', kuriame amžius suskirstytas į keturias grupes:
def calc_new_col(pajamu_analize):
   if pajamu_analize['amžius'] < 18 :
        return 'Nepilnametis'
   if (pajamu_analize['amžius'] >= 18) & (pajamu_analize['amžius'] < 36)  :
        return ' 18-35 m.'
   if (pajamu_analize['amžius'] >= 36) & (pajamu_analize['amžius'] < 65)  :
        return ' 36-64 m.'
   if (pajamu_analize['amžius'] >= 65)  :
        return ' 65 m. +'
pajamu_analize["grupe"] = pajamu_analize.apply(calc_new_col, axis=1)

# %%
# Gaunamų pajamų pasiskirstymas pagal lytį ir amžiaus grupę:
sns.catplot(data= pajamu_analize, x='grupe', y='mėnesio pajamos', hue='lytis', kind = 'bar', height=10)

# %% [markdown]
# PAPILDOMAI (iš "Vidutinės apdraustųjų pajamos : Vidutinės apdraustųjų pajamos")'
# ****************************

# %% [markdown]
# https://data.gov.lt/dataset/vidutines-apdraustuju-pajamosimport

# %%
import zipfile
with zipfile.ZipFile(data_dir / 'datasets/gov/vsdfv/vap/apdraustieji_det.zip', 'r') as zip_ref:
    zip_ref.extractall(data_dir / 'datasets/gov/vsdfv/vap') # PERVADINTI

# %%
# apdraustieji_det = pd.read_csv(data_dir / 'datasets/gov/vsdfv/vap/Apdraustas.csv', encoding='cp1257', sep=';')

# %%
apdraustieji_det.info()

# %%
apdraustieji_det.nunique()

# %%
apdraustieji_det.head()

# %%
# Neteisingas datos formatas, todėl pridedame naują kintamąjį 'LAIKAS' su teisingu datos formatu
apdraustieji_det['LAIKAS'] = pd.to_datetime(apdraustieji_det['METU_MENUO'], format = '%Y-%m mėn.') 

# %%
# Kiek apdraustųjų yra kas mėnesį?
mpl.rc('figure', figsize=(20,5))
ax = apdraustieji_det.set_index('LAIKAS').resample('M')['APDR_ASM_SK'].sum().plot(grid = True, c = 'y')
ax.yaxis.set_major_formatter(StrMethodFormatter( '{x:,.0f}'))
plt.ylabel('APDR_ASM_SK')
plt.show()
# Kodėl ties 2011 m. tokie staigūs kritimai ir kilimai?

# %%
# Darbo užmokesčio vidurkių pasiskirtymas pagal lytį:
sns.histplot(data = apdraustieji_det[apdraustieji_det['VIDURKIS'] < 3000], x = 'VIDURKIS', hue = 'LYTIS', kde = True)
plt.show()

# %%
# Kuri amžiaus grupė draudžasi dažniausiai?
mpl.rc('figure', figsize=(20,5))
temp_df = round((apdraustieji_det.groupby('AMZIUS')['APDR_ASM_SK'].sum().sort_values(ascending=False)
           / apdraustieji_det.groupby('AMZIUS')['APDR_ASM_SK'].sum().sort_values(ascending=False).sum())*100, 1)
ax = temp_df.plot(kind='bar', rot = 45)
ax.bar_label(ax.containers[0])
plt.ylabel('PROCENTAI')
plt.show()
