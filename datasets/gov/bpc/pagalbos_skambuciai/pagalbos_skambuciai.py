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

# %% [markdown] tags=[]
# # DUOMENŲ NUSKAITYMAS/PASIRUOŠIMAS

# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
from matplotlib.ticker import StrMethodFormatter
from pathlib import Path
# %matplotlib inline
from itertools import combinations
from collections import Counter

# %%
data_dir = Path().resolve().parents[3] / 'data'
klas = pd.read_csv(data_dir / "datasets/gov/bpc/pagalbos_skambuciai/IvykiuKlasifikatorius.csv")
laik = pd.read_csv(data_dir / "datasets/gov/bpc/pagalbos_skambuciai/IvykiuLaikas.csv")

# %% [markdown] tags=[]
# # ĮVYKIŲ KLASIFIKATORIUS. Keli pastebėjimai

# %%
klas.head()

# %%
klas.info()

# %%
klas.nunique() # matome, kad vienas ivykio_tipo_kodas pasikartoja 2 kartus

# %%
klas.value_counts('ivykio_tipo_kodas').sort_values(ascending = False).head(5) 

# %%
klas[klas['ivykio_tipo_kodas'] == '4.4.4'] # Su tuo pačiu 4.4.4 kodu yra du GMP įvykiai (Prasidėjęs gimdymas ir Gaisras pastate, nežinoma situacija)

# %%
# Dėl kurių įvykių tipų sulaukiama daugiausiai įvykių?
klas.value_counts('aukstesnis_ivykio_tipas').plot.bar()

# %% [markdown] tags=[]
# # ĮVYKIŲ LAIKAS. Duomenų analizė

# %%
laik.info()

# %%
laik.nunique()

# %%
laik.head()

# %%
# Sukuriami nauji stulpeliai 'savaite_valanda_minute', 'paros_metas' ir savaites_metas'
laik['savaite_valanda_minute'] = laik['savaites_diena'].astype(str) + '_' + laik['valanda'].astype(str) +'_'+ laik['minute']

def new_col(laik):
    if (laik['valanda'] == 22) | (laik['valanda'] == 23) | (laik['valanda'] == 0) | (laik['valanda'] == 1) | (laik['valanda'] == 2) | (laik['valanda'] == 3) | (laik['valanda'] == 4) | (laik['valanda'] == 5):
        return 'nakties metu'
    else:
        return 'dienos metu'
laik['paros_metas'] = laik.apply(new_col, axis=1)

def new_col2(laik):
    if (laik['savaites_diena'] == 6) | (laik['savaites_diena'] == 7):
        return 'savaitgalis'
    else:
        return 'darbo diena'
laik['savaites_metas'] = laik.apply(new_col2, axis = 1)

# %%
# Kurį 2022 m. vasaros mėnesį fiksuotą daugiausiai įvykių?
laik.groupby('menuo')['ivykiu_skaicius'].sum().to_frame()

# %%
# Kuriuo paros metu nutinka daugiausiai įvykių?
laik.groupby('paros_metas')['ivykiu_skaicius'].sum().plot.bar()

# %%
# Kuriuo savaitės metu nutinka daugiausiai įvykių?
laik.groupby('savaites_metas')['ivykiu_skaicius'].sum().plot.bar()

# %%
# Kuriuo metu (darbo dieną) įvyksta daugiausiai įvykių:
laik[laik['savaites_metas'] == 'darbo diena'].groupby(['savaite_valanda_minute','paros_metas'])['ivykiu_skaicius'].sum().sort_values(ascending = False).to_frame().head(5)

# %%
# Kuriuo metu (savaitgalį) įvyksta daugiausiai įvykių:
laik[laik['savaites_metas'] == 'savaitgalis'].groupby(['savaite_valanda_minute','paros_metas'])['ivykiu_skaicius'].sum().sort_values(ascending = False).to_frame().head(5)

# %% [markdown]
# Galime pastebėti, kad savaitgaliais daugiausiai įvykių įvyksta nakties metu ir sekmadieniais, o darbo dienomis - dienos metu ir ketvirtadieniais bei pirmadieniais.

# %%
# Kuriomis valandomis (darbo dieną ir dienos metu) nutinka daugiausiai įvykių:
laik[(laik['savaites_metas'] == 'darbo diena') & (laik['paros_metas'] == 'dienos metu')].groupby(['savaite_valanda_minute'])['ivykiu_skaicius'].sum().sort_values(ascending = False).to_frame().tail(5)

# %%
# Kuriomis valandomis (savaitgalį ir dienos metu) nutinka daugiausiai įvykių:
laik[(laik['savaites_metas'] == 'savaitgalis') & (laik['paros_metas'] == 'dienos metu')].groupby(['savaite_valanda_minute'])['ivykiu_skaicius'].sum().sort_values(ascending = False).to_frame().tail(5)

# %% [markdown]
# Galime pastebėti, kad dienos metu tiek savaitgaliais, tiek ir darbo dienomis, daugiausiai įvykių įvyksta 6 valandą ryto.

# %%
# Kokie įvykių tipai populiariausi darbo dienomis?
laik[laik['savaites_metas'] == 'darbo diena'].groupby(['ivykio_tipo_kodas._id'])['ivykiu_skaicius'].sum().sort_values(ascending = False).to_frame().head(5)

# %%
# Kokie įvykių tipai popliariausi savaitgaliais?
laik[laik['savaites_metas'] == 'savaitgalis'].groupby(['ivykio_tipo_kodas._id'])['ivykiu_skaicius'].sum().sort_values(ascending = False).to_frame().head(5)

# %%
klas[klas['_id'] == '32d2310b-621e-457c-8159-670b185fa580']

# %% [markdown]
# Pastebime, kad populiariausi įvykių tipai išlieka tie patys tiek savaitgaliais, tiek darbo dienomis. Tačiau įvykio tipas '32d2310b-621e-457c-8159-670b185fa580' - Smurtas artimoje aplinkoje darbo dienomis užima penktąją vietą, o savaitgaliais jau ketvirtąją.

# %%
# Kurią savaitės dieną įvyksta daugiausiai įvykių dienos metu?
laik[laik['paros_metas'] == 'dienos metu'].groupby('savaites_diena')['ivykiu_skaicius'].sum().sort_values(ascending = False)

# %%
# Kurią savaitės dieną įvyksta daugiausiai įvykių nakties metu?
laik[laik['paros_metas'] == 'nakties metu'].groupby('savaites_diena')['ivykiu_skaicius'].sum().sort_values(ascending = False)

# %% [markdown]
# Pastebime, įdomų faktą, kad dienos metu pirmadieniais įvyksta mažiausiai įvykių, tačiau nakties metu - pirmadieniai užima net antrąją vietą.

# %%
# Kuriomis savaitės dienomis, tiek dienos, tiek ir nakties metu įvykių yra daugiausia ?
mpl.rc('figure', figsize=(30,10))
laik.groupby(['savaites_diena'])['ivykiu_skaicius'].sum().plot()
plt.grid()

# %%
# Kuriomis valandomis, tiek savaitgaliais, tiek ir darbo dienomis, įvykių yra daugiausia?
mpl.rc('figure', figsize=(30,10))
plt.plot(laik.groupby('valanda')['ivykiu_skaicius'].sum())
plt.grid()

# %%
sav.info()
# ivykio_skaicius nėra struktūros apraše

# %%
sav.nunique()

# %%
sav.head()

# %%
# Populiariausi įvykių tipai:
sav.groupby('ivykio_tipo_kodas._id')['ivykiu_skaicius'].sum().sort_values(ascending = False).head(3)

# %%
# Populiariausi įvykių tipai:
sav.groupby(['ivykio_tipo_kodas._id', 'menuo'])['ivykiu_skaicius'].sum().sort_values(ascending = False).head(9).to_frame()

# %%
# Pasinaudojant ĮvykiųKlasifikatorius duomenimis, išvedami įvykio tipo duomenys
klas[klas['_id'] == '505a4081-64ab-4a13-9fad-ec1ed336e57d']
