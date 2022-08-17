http -bd https://atvira.sodra.lt/downloads/lt-eur/apdraustieji_ketv.zip
unzip apdraustieji_ketv.zip
#|  inflating: apdraustieji_ketv.csv
workon data
python
import pandas as pd
df = pd.read_csv('apdraustieji_ketv.csv', encoding='cp1257', sep=';')
df.info()
