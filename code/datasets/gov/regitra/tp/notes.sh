#!zsh

# https://data.gov.lt/datasets?q=&organization_id=132

# Peržiūrime rinkinius naudodamiesi ADP Public API
http -b "https://data.gov.lt/public/api/1/action/package_search?q=organization_id:132"  | jq '
.result.results[] | {
    title: .title,
    structure: .extras[]? | select(.key == "structure") | first(.value),
    resources: [.resources[]? | .url]
}
'
#| {
#|   "title": "Juridinių asmenų vardu Lietuvoje įregistruotų kelių transporto priemonių duomenys ",
#|   "structure": "https://data.gov.lt/dataset/1212/structure/749/Atviri_JTP_parko_duomenys_struktūra.csv",
#|   "resources": [
#|     "https://www.regitra.lt/atvduom/Atviri_JTP_parko_duomenys.zip"
#|   ]
#| }
#| {
#|   "title": "Lietuvoje įregistruotų kelių transporto priemonių duomenys",
#|   "structure": "https://data.gov.lt/dataset/1211/structure/1072/Atviri_TP_parko_duomenys_struktūra.csv",
#|   "resources": [
#|     "https://www.regitra.lt/atvduom/Atviri_TP_parko_duomenys.zip"
#|   ]
#| }

# Atsisiunčiame struktūros aprašus
structure=(
    https://data.gov.lt/dataset/1211/structure/1072/Atviri_TP_parko_duomenys_struktūra.csv tp
    https://data.gov.lt/dataset/1212/structure/749/Atviri_JTP_parko_duomenys_struktūra.csv jtp
)
for url name in ${(@kv)structure}; do
    http -bd $url -o $name.csv
done

# Įsidiegiame reikalingus paketus darbui su duomenimis
python -m venv env
env/bin/pip install spinta csvkit
source env/bin/activate

spinta check tp.csv jtp.csv
#| UnicodeDecodeError: 'utf-8' codec can't decode byte 0xeb in position 460: invalid continuation byte

# Bandome taisyti struktūros aprašą
csvclean -n tp.csv
#| Your file is not "utf-8-sig" encoded.
file -bi tp.csv
#| text/plain; charset=unknown-8bit
csvclean -n -e cp1257 tp.csv
#| Line 3: Expected 15 columns, found 1 columns
#| ...
cat tp.csv
sed -e 's/^"//g' -e 's/"\?\;\;\;\r$//g' -e 's/""/"/g' tp.csv | iconv -f cp1257 -t utf-8 -o tp-fix.csv
csvclean -n tp-fix.csv

csvclean -n jtp.csv
#| Your file is not "utf-8-sig" encoded.
iconv -f cp1257 -t utf-8 jtp.csv -o jtp-fix.csv
csvclean -n jtp-fix.csv

spinta check tp-fix.csv jtp-fix.csv
#| tp-fix.csv:32:type: Unknown additional dimension name choice
sed -i -e 's/choice/enum/g' tp-fix.csv
spinta check tp-fix.csv jtp-fix.csv
#| Error while parsing '5' manifest entry: Unknown component '' in 'types'.

# Kadangi yra daug klaidų, bandom žiūrėti į vystomą variantą iš GitHub
# https://github.com/atviriduomenys/manifest/tree/master/datasets/gov/regitra
http -bd https://github.com/atviriduomenys/manifest/raw/master/datasets/gov/regitra/tp.csv -o tp.csv
http -bd https://github.com/atviriduomenys/manifest/raw/master/datasets/gov/regitra/jtp.csv -o jtp.csv
spinta check tp.csv jtp.csv
#| Model reference 'datasets/gov/rc/ar/savivaldybe/Savivaldybe' not found.
http -bd https://github.com/atviriduomenys/manifest/raw/master/datasets/gov/rc/ar/savivaldybe.csv -o sav.csv
http -bd https://github.com/atviriduomenys/manifest/raw/master/datasets/gov/rc/ar/apskritis.csv -o aps.csv
spinta check aps.csv sav.csv tp.csv jtp.csv

# Peržiūrim struktūros aprašą
spinta copy aps.csv sav.csv tp.csv jtp.csv -o tp.xlsx

# Panašu, kad struktūros aprašai labai panašūs
csvcut tp.csv -c model,property -x > tp-props.csv
csvcut jtp.csv -c model,property -x > jtp-props.csv
diff -y tp-props.csv jtp-props.csv
# Struktūros aprašai nėra identiški, bet labai panašūs,
# gal juos galima apjungti?

csvstack tp.csv jtp.csv | csvgrep -c resource,model -a -r .+ | csvcut -c resource,base,model,type,ref,source,prepare | csvlook
#| | resource | base | model              | type | ref                   | source                                                       | prepare                                              |
#| | -------- | ---- | ------------------ | ---- | --------------------- | ------------------------------------------------------------ | ---------------------------------------------------- |
#| | csv      |      |                    | csv  |                       | https://www.regitra.lt/atvduom/Atviri_TP_parko_duomenys.zip  | self.extract("zip")["Atviri_TP_parko_duomenys.csv"]  |
#| |          |      | TransportoPriemone |      | keb_kodas, spec_kodas |                                                              |                                                      |
#| | csv      |      |                    | csv  |                       | https://www.regitra.lt/atvduom/Atviri_JTP_parko_duomenys.zip | self.extract("zip")["Atviri_JTP_parko_duomenys.csv"] |
#| |          |      | TransportoPriemone |      | keb_kodas, spec_kodas |                                                              |                                                      |

# Kadangi ZIP formatas yra gan nepatogus, duomenų naudojimo prasme ir gan
# sudėtingai aprašomas, todėl yra padaryta galiybė aprašyti ZIP failus
# patogiau, kaip atskirą resursą:
# https://atviriduomenys.readthedocs.io/duomenu-saltiniai.html#zip
#
# | resource | base | model              | type | ref                   | source                                |
# | -------- | ---- | ------------------ | ---- | --------------------- | ------------------------------------- |
# | atvduom  |      |                    | http |                       | https://www.regitra.lt/atvduom/{}.zip |
# | tp_zip   |      |                    | zip  | atvduom               | Atviri_TP_parko_duomenys              |
# | tp       |      |                    | csv  | tp_zip                | {}.csv                                |
# |          |      | TransportoPriemone |      | keb_kodas, spec_kodas | Atviri_TP_parko_duomenys              |
# | jtp_zip  |      |                    | zip  |                       | Atviri_JTP_parko_duomenys             |
# | jtp      |      |                    | csv  | jtp_zip               | {}.csv                                |
# |          |      | TransportoPriemone |      | keb_kodas, spec_kodas | Atviri_JTP_parko_duomenys             |

# Kadangi abiejų rinkinių struktūra yra vienoda, todėl galima juos apjungti:
# | resource | base               | model | type | ref                   | source                                |
# | -------- | ------------------ | ----- | ---- | --------------------- | ------------------------------------- |
# | atvduom  |                    |       | http |                       | https://www.regitra.lt/atvduom/{}.zip |
# | tp_zip   |                    |       | zip  | atvduom               | Atviri_TP_parko_duomenys              |
# | tp       |                    |       | csv  | tp_zip                | {}.csv                                |
# |          | TransportoPriemone |       |      |                       | Atviri_TP_parko_duomenys              |
# |          |                    | TP    |      | keb_kodas, spec_kodas | Atviri_TP_parko_duomenys              |
# | jtp_zip  |                    |       | zip  |                       | Atviri_JTP_parko_duomenys             |
# | jtp      |                    |       | csv  | jtp_zip               | {}.csv                                |
# |          | TransportoPriemone |       |      |                       | Atviri_JTP_parko_duomenys             |
# |          |                    | JTP   |      | keb_kodas, spec_kodas | Atviri_JTP_parko_duomenys             |

# Arba kitas apjungimo būdas, naudojant parametrizacija:
# | resource | model | property    | type  | ref                   | source                                | prepare        |
# | -------- | ----- | ----------- | ----  | --------------------- | ------------------------------------- | -------------- |
# |          |       |             | param | asmenys               | TP                                    |                |
# |          |       |             |       |                       | JTP                                   |                |
# | atvduom  |       |             | http  |                       | https://www.regitra.lt/atvduom/{}.zip |                |
# | tp_zip   |       |             | zip   | atvduom               | Atviri_{asmuo}_parko_duomenys         |                |
# | tp       |       |             | csv   | tp_zip                | {}.csv                                |                |
# |          | TransportoPriemone  |       | keb_kodas, spec_kodas | Atviri_{asmuo}_parko_duomenys         |                |
# |          |       |             | param | asmuo                 |                                       | param(asmenys) |
# |          |       | asmuo       | asmuo | string                |                                       | param(asmuo)   | 
# |          |       |             | enum  |                       | TP                                    | "fizinis"      | 
# |          |       |             |       |                       | JTP                                   | "juridinis"    | 

# Atsisiunčiame pačius duomenis
mkdir data
datasets=(
    https://www.regitra.lt/atvduom/Atviri_JTP_parko_duomenys.zip
    https://www.regitra.lt/atvduom/Atviri_TP_parko_duomenys.zip
)
for url in $datasets; do
    http -bd $url -o data/$(basename $url)
done

# Išarchyvuojam ZIP archyvus
for file in data/*.zip; do
    unzip $file -d data
done

# Kiek vietos užima duomenys?
du -sh data/*
wc -l data/*.csv

# Įdiegiam papildomas priemones duomenų analizei
pip install pandas matplotlib

# Analizuojame duomenis Python ir Pandas pagalba
python
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 120)

# Užsikraunam duomenis
tp = pd.read_csv('data/Atviri_TP_parko_duomenys.csv', index_col=['KEB_KODAS', 'SPEC_KODAS'], low_memory=False)

tp.info()
tp['VALD_TIPAS'].value_counts()
#| Fizinis      1673606
#| Juridinis     422585
# Kuo skiriasi TP ir JTP rinkiniai, jei šiame rinkinyje yra ir fiziniai ir juridiniai?

tp.head()
# Panašu, kad keb_kodas ir spec_kodas nėra pirminiai raktai, nes dubliuojasi arba nėra nurodyti.
# Kaip suprantu čia dėl nuasmeninimo?

tp.head().T
#| SAVIVALDYBE                                       KAUNO M. SAV.     UKMERGĖS R. SAV.    MARIJAMPOLĖS SAV.   ŠALČININKŲ R. SAV.              KAUNO M. SAV.
#| APSKRITIS                                                   KAU                  VIL                  MAR                  VIL                        KAU
# Panašu, kad savivaldybės ir apskrities pavadinimai nesutampa su RC AR, todėl jungimas gali būti sudėtingesnis, bet tikriausiai įmanomas.
# Šio lauko brandos lygis turėtu būti 2.

tp.nunique().sort_values()
#| SAVIVALDYBE                       66
# Panašu, kad savivaldybių yra daugiau nei jų yra iš tikrųjų.

tp['SAVIVALDYBE'].value_counts().sort_index()
# Pasirodo duomenyse pateiktos ne tik savivaldybės, bet ir šalys.
# Kadangi sumaišyti kelių skirtingų rūšių duomenys brandos lygis turėtu būti 1.
# Kaip suprantu, Lietuvoje galima registruoti užsienio piliečių transporto priemones?

# Kuo skiriasi modelio metai, nuo gamybos metų?
tp['MODELIO_METAI'].value_counts().sort_index()
tp['GAMYBOS_METAI'].value_counts().sort_index()

tp['PIRM_REG_DATA'].head()
tp[['PIRM_REG_DATA', 'GAMYBOS_METAI']].info()

ax = tp['GAMYBOS_METAI'].value_counts().sort_index().plot(grid=True)
pd.to_datetime(tp['PIRM_REG_DATA']).dt.year.value_counts().sort_index().plot(grid=True, ax=ax)
plt.show(); plt.close()
# Gan didelė dalis senų automoblilių.

tp['DEGALAI'].value_counts()
ax = tp['DEGALAI'].value_counts().plot.barh(grid=True)
plt.show(); plt.close()
# Įdomu, kodėl toks didelis skaičius TP pažymėta "--"?

tp['MARKE'].value_counts()
tp['KOMERCINIS_PAV'].value_counts()
tp['GAMINTOJO_PAV'].value_counts()
tp['GAMINTOJO_PAV_BAZ'].value_counts()
ax = tp['GAMINTOJO_PAV'].value_counts()[:10].plot.barh(grid=True)
plt.show(); plt.close()

ax = tp['MARKE'].value_counts()[:10].plot.barh(grid=True)
plt.show(); plt.close()
tp['MARKE'].value_counts()[:20]
# Kodėl skirtingia užrašyti pavadinimai, pavyzdžiui "VW" ir "VOLKSWAGEN. VW"?
# Panašu, kad čia brandos lygis turėtu būti 1?
