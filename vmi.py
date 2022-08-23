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

# %%
islaidos=pd.read_csv("Gyventojuislaidos.csv")

# %%
#Išlaidos#

# %%
islaidos.info() #paklausti del strukturoje esanciu beveik visu string

# %%
islaidos.nunique()

# %%
islaidos.head(10)

# %%
islaidos['suma'].nlargest(n=10) #10 didziausiu islaidu
#prideti ir rusi/savivaldybe
#is apraso "Išlaidų suma esanti virš 600000 eurų yra fiksuojama 600000 verte"

# %%
islaidos['suma'].nsmallest(n=10) #KAIP IMTI BE NULIU IR PRIDETI RUSI ARBA ISTRINTI NULINES

# %%
#------------RUSYS----------------#

# %%
islaidos_rusys=islaidos.groupby(['ir_kodas', 'pavadinimas']).sum(['suma']).drop(['metai','sav_kodas'],axis=1)
islaidos_rusys #pagal islaidu rusies kodus susumuota islaidu sumos

# %%
mpl.rc('figure', figsize=(10,10))
islaidos_rusys.reset_index().plot(x='ir_kodas', y='suma', c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Suma'])
plt.xlabel("Išlaidų rūšies kodas")
plt.ylabel("Išlaidų suma per 2020 m.")

# %%
islaidos_dazniai=islaidos.value_counts(['ir_kodas','pavadinimas']).sort_index()
islaidos_dazniai
#suskaiciuota kiek kiekvienos rusies (pagal koda ir pavadinima) yra islaidu duomenyse

# %%
mpl.rc('figure', figsize=(20,10))
islaidos_dazniai.reset_index().plot(x='ir_kodas', y=0, c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Dažniai'])
plt.xlabel("Išlaidų rūšies kodas")
plt.ylabel("Dažniai")

# %%
islaidos_vidurkiai=islaidos.groupby(['ir_kodas','pavadinimas']).mean().round(2).sort_values(by = 'ir_kodas').drop(['metai','sav_kodas'], axis=1)
islaidos_vidurkiai

# %%
mpl.rc('figure', figsize=(10,10))
islaidos_vidurkiai.reset_index().plot(x='ir_kodas', y='suma', c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Vidurkiai'])
plt.xlabel("Išlaidų rūšies kodas")
plt.ylabel("2020 m. vidurkis")

# %%
mpl.rc('figure', figsize=(20,10))
islaidos_dv = [islaidos_dazniai,islaidos_vidurkiai]
result=pd.concat(islaidos_dv)
result.hist() #0 pakeisti i daznius

# %%
islaidos_dazniai.max()

# %%
#---------------SAVIVALDYBES------------------#

# %%
islaidos_sav=islaidos.groupby(['sav_kodas', 'sav_pavadinimas']).sum(['suma']).sort_values(by ='sav_kodas').drop(['metai','ir_kodas'],axis=1)#kiek kiekvienam rusies savivaldybes kodui priklauso islaidu
islaidos_sav['suma'].nlargest(n=10)

# %%
islaidos_sav['suma'].nsmallest(n=10).sort_values(ascending = False)

# %%
mpl.rc('figure', figsize=(20,10))
islaidos_sav.reset_index().plot(x='sav_kodas', y='suma', c = 'blue', marker = 'o',  markersize=3, grid = True).legend(labels = ['Išlaidos'])
plt.xlabel("Savivaldybės kodas")
plt.ylabel("Išlaidų savivaldybėse suma (2020 m.)")

# %%
dazniai_sav = islaidos.value_counts(['sav_kodas','sav_pavadinimas']).sort_index()
dazniai_sav.head(5)

# %%
mpl.rc('figure', figsize=(20,10))
dazniai_sav.reset_index().plot(x='sav_kodas', y=0, c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Dažniai'])
plt.xlabel("Savivaldybės kodas")
plt.ylabel("Dažniai")

# %%
vidurkiai_sav=islaidos.groupby(['sav_kodas','sav_pavadinimas']).mean().round(2).drop(['metai', 'ir_kodas'], axis=1).sort_index()
vidurkiai_sav.head(10)

# %%
mpl.rc('figure', figsize=(20,10))
vidurkiai_sav.reset_index().plot(x='sav_kodas', y='suma', c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Vidurkiai'])
plt.xlabel("Savivaldybės kodas")
plt.ylabel("Išlaidų savivaldybėse vidurkiai (2020 m.)")

# %%
islaidos.loc[islaidos['sav_kodas'] == 23]

# %%
islaidos_miestui = islaidos.value_counts(['sav_pavadinimas', 'ir_kodas','pavadinimas']).sort_index()
islaidos_miestui.head()#rasti kiekveinai savivaldybei sriti, kur dazniausios/daugiausiai islaidu
islaidos_miestui['Neringos sav.'].nlargest(n=3) #trys popiliariausios tam mieste islaidu rusys)

# %%
islaidos['sav_pavadinimas'].unique()

# %%
islaidos_rusiai = islaidos.value_counts(['pavadinimas','sav_pavadinimas']).sort_index()
islaidos_rusiai.head()#rasti kiekveinai savivaldybei sriti, kur dazniausios/daugiausiai islaidu
islaidos_rusiai['Nepilnamečių (iki 18 metų) vaikų (įvaikių, globotinių, kuriems nustatyta nuolatinė globa šeimoje) priežiūros paslaugų išlaidos.'].nlargest(n=3)

# %%
islaidos['pavadinimas'].unique()

# %%
islaidos['suma'].plot.box(logy = True)

# %%
islaidos_sav.plot.box(logy = True)

# %%
sns.histplot(data=islaidos[islaidos['suma'] < 7000], x = 'suma', kde = True)

# %%
sns.histplot(data=islaidos[islaidos['suma'] < 2000], x = 'suma')

# %%
#######################################################################################################

# %%
#######################################################################################################

# %%
#Pajamos#

# %%
pajamos=pd.read_csv("GyventojuPajamos.csv")

# %%
pajamos.info() #kodėl nėra non-null ir count stulpeliu

# %%
pajamos.nunique()

# %%
pajamos.head(10)

# %%
#RUSYS#

# %%
pajamos_rusys=pajamos.groupby(['kodas', 'aprasas']).sum(['suma']).drop(['eil_num','sav_kodas', 'metai'],axis=1)
pajamos_rusys #pagal islaidu rusies kodus ir aprasus susumuota islaidu sumos

# %%
plt.rcParams['figure.figsize']=[20,10]
pajamos_rusys.reset_index().plot(x='kodas', y = 'suma', c = 'blue', marker = 'o',  markersize=3, grid = True).legend(labels = ['Suma'])
plt.xlabel("Pajamų kilmės kodas")
plt.ylabel("Pajamų suma")

# %%
pajamos_dazniai=pajamos.value_counts(['kodas', 'aprasas']).sort_index()
pajamos_dazniai
#cia suskaiciuota kiek kiekvienos rusies (pagal koda ir pavadinima) yra islaidu duomenyse

# %%
mpl.rc('figure', figsize=(20,10))
pajamos_dazniai.reset_index().plot(x='kodas', y = 0, c = 'blue', marker = 'o',  markersize=3, grid = True).legend(labels = ['Dažniai'])
plt.xlabel("Pajamų kilmės kodas")
plt.ylabel("Dažniai")

# %%
pajamos_vidurkiai=pajamos.groupby(['aprasas','kodas']).mean().round(2).sort_values(by = 'kodas').drop(['metai','sav_kodas','eil_num'], axis=1)
pajamos_vidurkiai 

# %%
mpl.rc('figure', figsize=(20,10))
pajamos_vidurkiai.reset_index().plot(x='kodas', y='suma', c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Vidurkiai'])
plt.xlabel("Pajamų rūšies kodas")
plt.ylabel("2020 m. vidurkis")

# %%
pajamos_dv = [pajamos_dazniai,pajamos_vidurkiai]
result=pd.concat(pajamos_dv)
result.hist()

# %%
#SAVIVALDYBES#

# %%
pajamos_sav=pajamos.groupby(['sav_kodas', 'sav_pavadinimas']).sum(['suma']).sort_values(by ='sav_kodas').drop(['metai','kodas','eil_num'],axis=1)
pajamos_sav.head(10) #kiek kiekvienam rusies savivaldybes kodui priklauso islaidu

# %%
plt.rcParams['figure.figsize']=[20,10]
pajamos_sav.reset_index().plot(x = 'sav_kodas', y = 'suma', c = 'blue', marker = 'o',  markersize=3, grid = True).legend(labels = ['Suma'])
plt.xlabel("Savivaldybės kodas")
plt.ylabel("Savivaldybės pajamų suma (2020 m.)")
#kaip paimti atskirus daugiausiai (ar mažiausiai) išleidžiančius miestus, padidinti tikslumą diagramoje

# %%
dazniai_sav_paj=pajamos.value_counts(['sav_kodas','sav_pavadinimas']).sort_index()
dazniai_sav_paj.head(10)

# %%
mpl.rc('figure', figsize=(20,10))
dazniai_sav_paj.reset_index().plot(x='sav_kodas', y = 0, c = 'blue', marker = 'o',  markersize=3, grid = True).legend(labels = ['Dažniai'])
plt.xlabel("Savivaldybės kodas")
plt.ylabel("Dažniai")

# %%
vidurkiai_sav_paj=pajamos.groupby(['sav_kodas','sav_pavadinimas']).mean().round(2).drop(['metai', 'kodas', 'eil_num'], axis=1).sort_index()
vidurkiai_sav_paj.head(10)

# %%
mpl.rc('figure', figsize=(20,10))
vidurkiai_sav_paj.reset_index().plot(x='sav_kodas', y='suma', c = 'red', marker = 'o',  markersize=7, grid = True).legend(labels = ['Vidurkiai'])
plt.xlabel("Savivaldybės kodas")
plt.ylabel("Pajamų savivaldybėse vidurkiai (2020 m.)")

# %%
pajamos.loc[pajamos['sav_kodas'] == 23]

# %%
miestui_paj = pajamos.value_counts(['sav_pavadinimas', 'kodas','aprasas']).sort_index()
miestui_paj.head()#rasti kiekveinai savivaldybei sriti, kur dazniausios/daugiausiai islaidu
miestui_paj['Alytaus m. sav.'].nlargest(n=3) #trys popiliariausios tam mieste islaidu rusys) ir taip su visais kazka bendro

# %%
pajamos['sav_pavadinimas'].unique()

# %%
rusiai_paj = pajamos.value_counts(['aprasas','sav_pavadinimas']).sort_index()
rusiai_paj.head()#rasti kiekveinai savivaldybei sriti, kur dazniausios/daugiausiai islaidu
rusiai_paj['Azartinių lošimų laimėjimų pajamos'].nlargest(n=3)

# %%
pajamos['aprasas'].unique()

# %%
pajamos['suma'].plot.box(logy = True)

# %%
pajamu_sav['suma'].plot.box(logy = True)

# %%
sns.histplot(data=pajamos[pajamos['suma'] <20000], x = 'suma')

# %%
sns.histplot(data=pajamos[pajamos['suma'] <1000], x = 'suma')

# %%
pajamos['suma'].min() #kodel and dia kitaip
