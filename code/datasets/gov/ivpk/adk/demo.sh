# Katalogo viešasis API
https://data.gov.lt/public/api/1
http -b https://data.gov.lt/public/api/1/action/package_search
http -b "https://data.gov.lt/public/api/1/action/package_search?q=title:katalogo" | jq '.result.results[]'  
http -b "https://data.gov.lt/public/api/1/action/package_search?q=title:katalogo" | \
    jq '.result.results[] | {name: .name, title: .title, resources: [.resources[]? | {name: .name, url: .url}]}'  

# Katalogo duomenys RDF formatu
https://data.gov.lt/edp/dcat-ap.rdf
http -bd https://data.gov.lt/edp/dcat-ap.rdf
rdf query -i dcat-ap.rdf -q "select ?s ?p ?o where { ?s ?p ?o. } limit 10"

# Duomenų atvėrimo procesas
# #########################

# Duomenų atvėrimo užduočių valdymas:
https://github.com/orgs/atviriduomenys/projects/2/views/1

# 1. Šaltinio duomenų struktūros aprašo (ŠDSA) paruošimas
spinta inspect -b adp -o sdsa.xlsx

# 2. Atveriamų duomenų peržiūra prieš publikavimą
spinta run --mode external sdsa.xlsx

# 3. Atvirų duomenų struktūros aprašo (ADSA) atskyrimas nuo ŠDSA
spinta copy sdsa.xlsx --no-source --access open -o adsa.csv

# 4. ADSA kokybės užtikrinimo procedūra:
https://github.com/atviriduomenys/manifest/pulls

# 5. ADSA įkėlimas į duomenų publikavimo serverį (Saugyklą) ir į data.gov.lt:
https://get.data.gov.lt/

# 6. Duomenų publikavimas
spinta push sdsa.xlsx -o https://put-test.data.gov.lt


# Duomenų naudojimas
# ##################

# Iš data.gov.lt galima atsisiųsti 
https://data.gov.lt/dataset/atviru-duomenu-katalogo-api
http -bd https://data.gov.lt/dataset/1223/structure/adk.csv
spinta copy adk.csv -o adk.xlsx

url=https://get-test.data.gov.lt/datasets/gov/ivpk/adp/catalog
http -b $url/:ns | jq '._data[].name'
http -b $url'/Dataset?title.contains("katalogo")'
http -b $url'/Dataset?title.contains("katalogo")&select(title,status)' Accept:text/plain
http -b $url'/Dataset?title.contains("katalogo")&select(title,status)' Accept:text/csv
http -b $url'/Dataset?title.contains("katalogo")&select(title,status)' Accept:application/json
http -b $url'/Dataset?title.contains("katalogo")&select(title,status)' Accept:application/x-json-stream
http -b https://get-test.data.gov.lt/datasets/gov/ivpk/adp/catalog/Dataset/4d77f1b2-4f85-46cc-9bf0-ec299e9102ab

http -b $url'/Dataset?status="HAS_DATA"&count()'
http -b $url'/Dataset?status="HAS_DATA"&select(title)&limit(10)' Accept:text/plain
http -b $url'/Dataset?status="HAS_DATA"&select(title)&sort(title)&limit(10)' Accept:text/plain
http -b $url'/Dataset?status="HAS_DATA"&select(title)&sort(-title)&limit(10)' Accept:text/plain
http -b $url'/Dataset?status="HAS_DATA"&select(creator.title,title)&limit(10)' Accept:text/plain

