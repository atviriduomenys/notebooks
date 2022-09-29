# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [markdown] tags=[]
# # IŠLAIDOS

# + Agreguoti duomenys iš juridinių asmenų pateiktos informacijos apie gyventojų patirtas įmokas ir gyventojų deklaruotas išlaidas,
# kuriomis gali būti mažinamos gyventojų apmokestinamosios pajamos. 
# https://data.gov.lt/dataset/gyventoju-patirtos-islaidos
# + Gyventojų registro (GR) duomenys apie Lietuvos Respublikos teritorijoje įregistruotus fizinius asmenis. GR duomenys apie Lietuvos gyventojų amžių ir lytį pagal savivaldybes
# https://www.registrucentras.lt/p/1539
# https://data.gov.lt/dataset/gyventoju-registro-duomenys-apie-lietuvos-gyventoju-amziu-ir-lyti-pagal-savivaldybes

# # Duomenų nuskaitymas

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pathlib import Path
# %matplotlib inline

data_dir = Path().resolve().parents[3] / 'data'
data_dir

islaidos=pd.read_csv(data_dir / "datasets/gov/vmi/gyventoju_islaidos/GyventojuIslaidos.csv")

rc = pd.read_csv(data_dir / "datasets/gov/rc/gr/01_gr_open_amzius_lytis_pilietybes_sav_r1.csv")

# + [markdown] tags=[]
# # Duomenų apžvalga
# -

pd.options.display.max_colwidth = 500
islaidos.head().T

# Kodėl daug nulinių reikšmių sumos stulpelyje?
islaidos[islaidos['suma'] == 0].head().T # 552 reikšmės

# Kai kurie Dtype neatitinka tipo nurodyto struktūros apraše. Pvz: sav_kodas

islaidos.info() 

islaidos.nunique()

# + [markdown] tags=[]
# # Išlaidų rūšys pagal populiarumą
# -

# Brėžiame diagramą, kuri vaizduoja kiekvienos išlaidų rūšies dažnį šiuose duomenyse.

mpl.rc('figure', figsize=(20,10))
df = round((islaidos['pavadinimas'].value_counts().sort_values(ascending=False) 
                 / islaidos['pavadinimas'].value_counts().sort_values(ascending=False).sum())*100,1)
ax = df.plot.barh()
ax.bar_label(ax.containers[0])
plt.xlabel('procentai')
plt.ylabel('pavadinimas')
plt.show()

# Skaičiuojant procentinę dalį pastebime, kad "Gyvybės draudimo įmokos" sudaro net 62 % visų išlaidų rūšių, kuriomis gali būti mažinamos gyventojų apmokestinamosios pajamos

# Taip pat galime pažiūrėt, kaip bendrai yra pasiskirstę visos išlaidų rūšys.

vienas = islaidos.set_index(['_id','pavadinimas'])['suma'].unstack() #.plot.box(logy = True)
fig, ax= plt.subplots(figsize=(20, 10))
ax.set_xscale('log')
g = sns.boxplot(data=vienas , palette='rainbow', orient="h", ax=ax)
plt.xlabel('suma')
plt.tight_layout()

# Iš boxplot diagramų matome, kad "Gyvybės draudimo įmokos" turi labai daug išsiskiriančių reikšmių. Kyla klausimas dėl 60000 ribos duomenyse. Taip pat matome, kad didžiausią medianą turi "Pastatų, statinių remonto, apdailos (išskyrus renovaciją) darbų išlaidos, o labiausiai svyruojančios išlaidų sumos yra dėl "Būsto kredito, suteikto iki 2008-12-31, palūkanos" ir "Nepilnamečių (iki 18 metų) vaikų (įvaikių, globotinių, kuriems nustatyta nuolatinė globa šeimoje) priežiūros paslaugų išlaidos."

# Naudojame procentų $\sum(1/2)^n$ progresiją. Šiuo būdu galime patikrinti, kokią sumą sudaro įmokos, kurias moka pvz. 50% mažiausiai sumokančių gyventojų arba mažiau nei 1% daugiausiai sumokančių gyventojų:

# +
rusis_islaidos = islaidos.loc[islaidos['pavadinimas'] == 'Gyvybės draudimo įmokos.']

_50H = rusis_islaidos.sort_values('suma', ascending = True).head(round(0.5*len(rusis_islaidos)))
a = _50H['suma'].sum()
_50T = rusis_islaidos.sort_values('suma', ascending = True).tail(round(0.5*len(rusis_islaidos)))

_25H =_50T.sort_values('suma', ascending = True).head(round(0.5*len(_50T)))
b = _25H['suma'].sum()
_25T = _50T.sort_values('suma', ascending = True).tail(round(0.5*len(_50T)))

_12_5H = _25T.sort_values('suma', ascending = True).head(round(0.5*len(_25T)))
c = _12_5H['suma'].sum()
_12_5T = _25T.sort_values('suma', ascending = True).tail(round(0.5*len(_25T)))

_6_25H = _12_5T.sort_values('suma', ascending = True).head(round(0.5*len(_12_5T)))
d = _6_25H['suma'].sum()
_6_25T = _12_5T.sort_values('suma', ascending = True).tail(round(0.5*len(_12_5T)))

_3_125H = _6_25T.sort_values('suma', ascending = True).head(round(0.5*len(_6_25T)))
e = _3_125H['suma'].sum()
_3_125T = _6_25T.sort_values('suma', ascending = True).tail(round(0.5*len(_6_25T)))

_1_56H = _3_125T.sort_values('suma', ascending = True).head(round(0.5*len(_3_125T)))
f = _1_56H['suma'].sum()
_1_56T = _3_125T.sort_values('suma', ascending = True).tail(round(0.5*len(_3_125T)))

_0_8H = _1_56T.sort_values('suma', ascending = True).head(round(0.5*len(_1_56T)))
g = _0_8H['suma'].sum()

_0_8T = _1_56T.sort_values('suma', ascending = True).tail(round(0.5*len(_1_56T)))
h = _0_8T['suma'].sum()
# -

fig = plt.figure()
s = fig.add_subplot(111)
s.bar([1, 2, 3, 4, 5, 6, 7, 8], [a, b, c, d, e, f, g, h], width=.5, log = True)
# plt.ticklabel_format(style = 'plain')
plt.xticks((1, 2, 3, 4, 5, 6, 7, 8), ('50%', '25%', '12.5%', '6.25%', '3.125%', '1.56%', '0.8%', '0.8%'))
plt.show()

ciklui = rusis_islaidos.sort_values( by = 'suma', ascending = True)
procentams = [a, b, c, d, e, f, g, h]
percentage = []
for i in procentams:
    pct = (i / ciklui['suma'].sum()) * 100
    percentage.append(round(pct,2))
print(percentage)

# # Vilniaus miesto ir Neringos savivaldybių išlaidų palyginimas

# Norėdami palyginti savivaldybes tarpusavyje, pirmiausia turime jas normalizuoti pagal gyventojų skaičių. Tam esame nusiskaitę duomenis iš gyventojų registro apie Lietuvos gyventojų amžių ir lytį pagal savivaldybes

# Pasirenkame palyginti būtent Neringos ir Vilniaus miesto savivaldybes, nes apskaičiavus visų išlaidų sumos medianą, paaiškėja, jog Neringos savivaldybėje išlaidų dydžiai yra aukščiausi. 

mediana = islaidos.groupby(['sav_pavadinimas'])['suma'].median().sort_values(ascending = False)
mediana.head().to_frame()

# Todėl lyginame jas dalindami visų išlaidų rūšių bendras sumas iš toje savivaldybėje gyvenančių gyventojų skaičiaus, šiuos duomenis gauname iš gyventojų registro. 

vilnius = islaidos.loc[islaidos['sav_pavadinimas'] == 'Vilniaus m. sav.']
vilnius1 = rc.loc[rc['sav_pavadinimas'] == 'Vilniaus m. sav.']
is_viso_vilnius = vilnius1.shape[0]
vilnius_dal_2 = vilnius.groupby(['pavadinimas'])['suma'].sum()/(is_viso_vilnius)
vilnius_dal_2.to_frame()

neringa = islaidos.loc[islaidos['sav_pavadinimas'] == 'Neringos sav.']
neringa1 = rc.loc[rc['sav_pavadinimas'] == 'Neringos sav.']
is_viso_neringa = neringa1.shape[0]
neringa_dal_2 = neringa.groupby(['pavadinimas'])['suma'].sum()/(is_viso_neringa)
neringa_dal_2.to_frame()

# Peržiūrėjus abi lenteles galime daryti išvadą, jog Neringos savivaldybėje gyvena turtingesni žmonės ir, kad ten pragyvenimas greičiausiai kainuoja daugiau, nei Vilniaus miesto savivaldybėje, kadangi beveik visos apskaičiuotos sumos Neringos savivaldybėje lenkia Vilniaus miesto savivaldybės išlaidas
