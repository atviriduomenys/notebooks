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

# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib.ticker import StrMethodFormatter
from pathlib import Path
# %matplotlib inline
from itertools import combinations
from collections import Counter

# %%
data_dir = Path().resolve().parents[3] / 'data'
df = pd.read_csv(data_dir / "datasets/gov/vmi/verslo_liudijimai/VersloLiudijimas.csv")

# %%
df.info()

# %%
df['registracija'] = pd.to_datetime(df['registracija'])
df['sprendimo_data'] = pd.to_datetime(df['sprendimo_data'])
df['data_nuo'] = pd.to_datetime(df['data_nuo'])
df['data_iki'] = pd.to_datetime(df['data_iki'])
df['veiklos_pabaiga'] = pd.to_datetime(df['veiklos_pabaiga'])
df['anuliavimo_data'] = pd.to_datetime(df['anuliavimo_data'])
df['veiklos_sav'] = df['veiklos_sav'].astype(str).replace('\.0', '', regex=True)
df['veiklos_vieta_veiksmas'] = df['veiklos_vieta_veiksmas'].astype(str).replace('\.0', '', regex=True)
df['teritorija_kodas'] = df['teritorija_kodas'].astype(str).replace('\.0', '', regex=True)
df['eiles_nr'] = df['eiles_nr'].astype(str)
df['grupe'] = df['grupe'].astype(str)
df['teritorija'] = df['teritorija'].astype(str)
df['savivaldybe'] = df['savivaldybe'].astype(str)
df['rusies_kodas'] = df['rusies_kodas'].astype(str)

# %%
df.nunique()

# %%
df.head().T

# %%
# Sukuriami papildomi stulpeliai skaičiavimams
df['savaites_diena'] = df['registracija'].dt.dayofweek #išveda savaitės dieną, kada buvo registruotas verslo liūdijimas, čia 0 - pirmadinienis,..., 6 - sekmadienis
df['tarpas'] = abs(df['data_nuo'].dt.date - df['registracija'].dt.date) # išveda dienų skaičių, kurios praėjo nuo verslo liudijimo registarcijos datos iki jo įsigaliojimo pradžios 
df['laikotarpis'] = abs(df['data_iki'].dt.date - df['data_nuo'].dt.date) # išveda dienų skaičių, kurios praėjo nuo verslo liudijimo įsigaliojimo praždios iki pabaigas.

# %%
# Kurią savaitės dieną yra registruojama daugiausiai verslo liudijimų? 
labels = ('Pirmadienis', 'Antradienis', 'Trečiadienis', 'Ketvirtadienis', 'Penktadienis', 'Šeštadienis', 'Sekmadienis')
df.value_counts('savaites_diena').sort_index().plot.pie(autopct = '%.2f', figsize = (10,10), labels = labels)
plt.ylabel('')
plt.show()

# %%
# Kokiai procentinei daliai yra taikomos lengvatos?
plt.figure(0)
df.value_counts('lengvata').sort_index().plot.pie(autopct='%.2f')
plt.ylabel('')
plt.title('BENDRAI')

# Kuri iš rūšių gauna daugiausiai lengvatų?
plt.figure(1)
df[df['grupe'] == '1'].value_counts('lengvata').sort_index().plot.pie(autopct='%.2f')
plt.ylabel('')
plt.title('GAMYBA')

plt.figure(2)
df[df['grupe'] == '2'].value_counts('lengvata').sort_index().plot.pie(autopct='%.2f')
plt.ylabel('')
plt.title('PASLAUGOS')

plt.figure(3)
df[df['grupe'] == '3'].value_counts('lengvata').sort_index().plot.pie(autopct='%.2f')
plt.ylabel('')
plt.title('PREKYBA')

plt.show()

# %%
# Kiek (dažniausiai) praeina dienų nuo liudijimo registracijos datos iki jo įsigaliojimo pradžos?
savaite2 = df.value_counts('tarpas').sort_index().head(15)
savaite2.sort_index().plot.bar(width=0.1, figsize = (10,5))

# %%
# Koks dažniausias verslo liudijimo galiojimo laikotarpis?
df['laikotarpis'].median()

# %%
# Kiek procentų verslo liudijmų nėra anuliuojami arba nutraukiami?
percent_missing = df.isnull().sum() * 100 / len(df)
missing_value_df = pd.DataFrame({'veiklos_pabaiga': df.columns,
                                 'percent_missing': percent_missing})
percent_missing.round(2).sort_values(ascending = False).head(4)

# %%
# Surandame visus kiekvieno mokesčių mokėtojo verslo liudijimus  
new = df[df['mm_kodas'].duplicated(keep = False)].sort_values('mm_kodas') # patikriname visas eilutes is mm_kodas stulpelio ir randam visas, kurios kartojasi
new['grouped'] = new.groupby('mm_kodas')['rusies_kodas'].transform(lambda x: ','.join(x)) # sugrupuojame pagal mm_kodas ir sujungiame visus rusies_kodas
new = new[['mm_kodas', 'grouped']].drop_duplicates() # pašaliname dublikatus
new

# %%
# Kokios kombinacijos yra pačios rečiausios (įdomiausios) ?
count = Counter()
for row in new['grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,3))) 
n = 20
count.most_common()[:-n-1:-1]

# %%
pd.options.display.max_colwidth = 500
df[df['rusies_kodas'] == '2']['rusis_pavadinimas'].drop_duplicates().to_frame()
df[df['rusies_kodas'] == '16']['rusis_pavadinimas'].drop_duplicates().to_frame()
df[df['rusies_kodas'] == '51']['rusis_pavadinimas'].drop_duplicates().to_frame()
# 2,16,51 
# Pavyzdys: tas pats mokesčių mokėtojas turi/turėjo verslo liudijimus (2. Medienos ruoša, malkų gamyba, medienos ruošos paslaugų veikla, įskaitant rąstų vežimą miške
# 16. Avalynės taisymas, 51. Gyvenamosios paskirties patalpų nuoma.
