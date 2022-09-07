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
# %matplotlib inline

# %% [markdown] tags=[]
# # IŠLAIDOS

# %% [markdown]
# Agreguoti duomenys iš juridinių asmenų pateiktos informacijos apie gyventojų patirtas įmokas ir gyventojų deklaruotas išlaidas,
# kuriomis gali būti mažinamos gyventojų apmokestinamosios pajamos. 
# https://data.gov.lt/dataset/gyventoju-patirtos-islaidos

# %%
islaidos=pd.read_csv("data/datasets/gov/vmi/gyventoju_islaidos/GyventojuIslaidos.csv")

# %% [markdown] tags=[]
# # KLAUSIMAI

# %%
# Kodėl daug nulinių reikšmių
# Pataisyti brandos lygiai (visi)
# Kodėl yra maksimali riba 600000

# %% [markdown] tags=[]
# # Duomenų apžvalga

# %%
pd.options.display.max_colwidth = 500
islaidos.head(5)

# %% [markdown]
# Kai kurie Dtype neatitinka tipo nurodyto struktūros apraše. Pvz: sav_kodas, 

# %%
islaidos.info() 

# %%
islaidos.nunique()

# %% [markdown] tags=[]
# # Išlaidų rūšys pagal populiarumą

# %% [markdown]
# Brėžiame diagramą, kuri vaizduoja kiekvienos išlaidų rūšies dažnį šiuose duomenyse.

# %%
mpl.rc('figure', figsize=(20,10))
islaidos_dazniai=islaidos.value_counts(['ir_kodas','pavadinimas']).sort_values(ascending = False).to_frame()
islaidos_dazniai.plot.barh().legend(labels=['Dažnis'])

# %% [markdown]
# Diagramos matome, kad tarp išlaidų rūšių, kuriomis gali būti mažinamos gyventojų apmokestinamosios pajamos, akivaizdžiai pirmauja gyvybės draudimo įmokos.

# %% [markdown]
# Taip pat galime pažiūrėt, kaip bendrai yra pasiskirstę visos išlaidų rūšys.

# %%
vienas = islaidos.set_index(['_id','pavadinimas'])['suma'].unstack() #.plot.box(logy = True)
fig, ax= plt.subplots(figsize=(20, 10))
ax.set_xscale('log')
g = sns.boxplot(data=vienas , palette='rainbow', orient="h", ax=ax)
plt.tight_layout()

# %% [markdown]
# Iš boxplot diagramų matome, kad "Gyvybės draudimo įmokos" turi labai daug išsiskiriančių reikšmių. Kyla klausimas dėl 60000 ribos duomenyse. Taip pat matome, kad didžiausią medianą turi "Pastatų, statinių remonto, apdailos (išskyrus renovaciją) darbų išlaidos, o labiausiai svyruojančios išlaidų sumos yra dėl "Būsto kredito, suteikto iki 2008-12-31, palūkanos" ir "Nepilnamečių (iki 18 metų) vaikų (įvaikių, globotinių, kuriems nustatyta nuolatinė globa šeimoje) priežiūros paslaugų išlaidos."

# %%
rūšis_islaidos = islaidos.loc[islaidos['pavadinimas'] == 'Gyvybės draudimo įmokos.']
count_row_visos = islaidos.shape[0] 
count_row_gd = rūšis_islaidos.shape[0]
def percentage(part, whole):
 Percentage = 100 * float(part)/float(whole)
 return str(Percentage)
percentage(count_row_gd, count_row_visos)

# %% [markdown]
# Skaičiuojant procentinę dalį pastebime, kad "Gyvybės draudimo įmokos" sudaro net 62 % visų išlaidų rūšių, kuriomis gali būti mažinamos gyventojų apmokestinamosios pajamos

# %% [markdown]
# Brėžiame diagramą, kuri vaizduoja "Gyvybės draudimo įmokos" sumas ir jų dažnius.

# %%
mpl.rc('figure', figsize=(20,10))
rūšis_islaidos['suma'].plot.hist(bins = 100, logy = True, color='y', grid = True)

# %% [markdown]
# Pastebime aiškiai išsiskiriančias reikšmes - pavieniai atvejai, kuomet "Gyvybės draudimo įmokos" sumos siekia 100000 ar net 600000.

# %%
islaidos_gyv_draud = islaidos.loc[islaidos['pavadinimas'] == 'Gyvybės draudimo įmokos.']
count_row = islaidos_gyv_draud.shape[0]
isl = islaidos_gyv_draud['suma'].nlargest(2732).to_frame()
m_isl = islaidos_gyv_draud['suma'].nsmallest(270442).to_frame()
count_row_visos = islaidos_gyv_draud.shape[0] 
count_row_gd = isl.shape[0]
def percentage(part, whole):
 Percentage = 100 * float(part)/float(whole)
 return str(Percentage)
percentage(count_row_gd, count_row_visos)

# %% [markdown]
# Galime patikrinti pavyzdžiui kokią dalį iš visos "Gyvybės draudimo įmokos" išlaidų sumos sudaro 1 % daugiausiai sumokančių žmonių.

# %%
islaidos_all = islaidos_gyv_draud['suma'].sum()
islaidos_isl = isl['suma'].sum()
islaidos_m_isl = m_isl['suma'].sum()
count_row_visos = islaidos_all 
count_row_gd = islaidos_isl
def percentage(part, whole):
 Percentage = 100 * float(part)/float(whole)
 return str(Percentage)
percentage(count_row_gd, count_row_visos)

# %% [markdown]
# Matome, kad 1 % didžiausias įmokas sumokančių mokesčių mokėtojų išleidžiamos sumos gyvybės draudimui sudaro beveik 9 % visos šios rūšies išlaidų sumos.

# %% [markdown]
# # Vilniaus miesto ir Neringos savivaldybių išlaidų palyginimas

# %% [markdown]
# Norėdami palyginti savivaldybes tarpusavyje, pirmiausia turime jas normalizuoti pagal gyventojų skaičių. Tam nusiskaitome duomenis iš gyventojų registro apie Lietuvos gyventojų amžių ir lytį pagal savivaldybes

# %%
rc = pd.read_csv("data/datasets/gov/rc/gr/01_gr_open_amzius_lytis_pilietybes_sav_r1.csv")

# %% [markdown]
# Gyventojų registro (GR) duomenys apie Lietuvos Respublikos teritorijoje įregistruotus fizinius asmenis. GR duomenys apie Lietuvos gyventojų amžių ir lytį pagal savivaldybes. Duomenų geografinė imtis — visa šalies teritorija. Brandos lygis — III. Atnaujinimo dažnumas — kas 12 mėn. Duomenų formatas — CSV. Licencija — CC BY 4.0. Atvėrimo data — 2022-01-14
# https://www.registrucentras.lt/p/1539
# https://data.gov.lt/dataset/gyventoju-registro-duomenys-apie-lietuvos-gyventoju-amziu-ir-lyti-pagal-savivaldybes

# %%
# islaidos_sav=islaidos.groupby(['sav_kodas', 'sav_pavadinimas'])['suma'].sum().sort_values(ascending = False)
# islaidos_sav.head(10)

# %%
rc.head()

# %%
rc.nunique()

# %% [markdown]
# Pasirenkame palyginti būtent Neringos ir Vilniaus miesto savivaldybes, nes apskaičiavus visų išlaidų sumos medianą, paaiškėja, jog Neringos savivaldybėje išlaidų dydžiai yra aukščiausi. 

# %%
mediana = islaidos.groupby(['sav_pavadinimas'])['suma'].median().sort_values(ascending = False)
mediana.head().to_frame()

# %% [markdown]
# Todėl lyginame jas dalindami visų išlaidų rūšių bendras sumas iš toje savivaldybėje gyvenančių gyventojų skaičiaus, šiuos duomenis gauname iš gyventojų registro. 

# %%
vilnius = islaidos.loc[islaidos['sav_pavadinimas'] == 'Vilniaus m. sav.']
vilnius1 = rc.loc[rc['sav_pavadinimas'] == 'Vilniaus m. sav.']
is_viso_vilnius = vilnius1.shape[0]
vilnius_dal_2 = vilnius.groupby(['pavadinimas'])['suma'].sum()/(is_viso_vilnius)
vilnius_dal_2.to_frame()

# %%
neringa = islaidos.loc[islaidos['sav_pavadinimas'] == 'Neringos sav.']
neringa1 = rc.loc[rc['sav_pavadinimas'] == 'Neringos sav.']
is_viso_neringa = neringa1.shape[0]
neringa_dal_2 = neringa.groupby(['pavadinimas'])['suma'].sum()/(is_viso_neringa)
neringa_dal_2.to_frame()

# %% [markdown]
# Peržiūrėjus abi lenteles galime daryti išvadą, jog Neringos savivaldybėje gyvena turtingesni žmonės ir, kad ten pragyvenimas greičiausiai kainuoja daugiau, nei Vilniaus miesto savivaldybėje, kadangi beveik visos apskaičiuotos sumos Neringos savivaldybėje lenkia Vilniaus miesto savivaldybės išlaidas
