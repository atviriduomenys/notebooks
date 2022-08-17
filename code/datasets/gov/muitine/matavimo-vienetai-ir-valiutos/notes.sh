# Matavimo vienetai ir valiutos
# https://data.gov.lt/dataset/6-matavimo-vienetu-naudojamu-deklaruojant-prekes-lietuvos-respublikos-muitinei-sarasas
# https://data.gov.lt/dataset/7-matavimo-vienetu-naudojamu-deklaruojant-prekes-lietuvos-muitinei-patikslintoju-kodu-sarasas
# https://data.gov.lt/dataset/9-muitineje-naudojamu-valiutu-kursu-sarasas
# https://data.gov.lt/dataset/10-valiutu-naudojamu-deklaruojant-prekes-lietuvos-muitinei-sarasas

http -bd https://www.lrmuitine.lt/mport/other_files/AtviriDuom_klasifikatoriai/9LT.xml
http -bd https://www.lrmuitine.lt/mport/other_files/AtviriDuom_klasifikatoriai/10LT.xml
http -bd https://www.lrmuitine.lt/mport/other_files/AtviriDuom_klasifikatoriai/92LT.xml
http -bd https://www.lrmuitine.lt/mport/other_files/AtviriDuom_klasifikatoriai/18LT.xml
http -bd https://www.lrmuitine.lt/mport/other_files/AtviriDuom_klasifikatoriai/16LT.xml

du -sh *.xml | sort -h
wc -l *.xml

poetry init -n
poetry add pandas lxml matplotlib
poetry run python

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)


# Prekės kodų, matavimo vienetų ir jų patikslintojų kodų sąryšio sąrašas
sarysis = pd.read_xml('46LT.xml', stylesheet='''
<xsl:stylesheet
 version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns="http://rep.xmlstandards.eu/icdts/LT/schemas/ReferenceData.xsd"
 >
  <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <data>
      <xsl:apply-templates select="/ns:ReferenceData/ns:Correlation"/>
    </data>
  </xsl:template>
  <xsl:template match="/ns:ReferenceData/ns:Correlation">
    <row>
      <commodity><xsl:value-of select="@code1"/></commodity>
      <unit><xsl:value-of select="@code2"/></unit>
      <unit_qualifier><xsl:value-of select="@code3"/></unit_qualifier>
      <country><xsl:value-of select="@code4"/></country>
      <import><xsl:value-of select="@code5"/></import>
      <export><xsl:value-of select="@code6"/></export>
      <valid_from><xsl:value-of select="@validFrom"/></valid_from>
      <valid_to><xsl:value-of select="@validTo"/></valid_to>
    </row>
  </xsl:template>
</xsl:stylesheet>
''')
sarysis['valid_from'] = pd.to_datetime(sarysis['valid_from'])
sarysis['valid_to'] = pd.to_datetime(sarysis['valid_to'])
#| Out of bounds nanosecond timestamp: 4712-12-31 00:00:00
sarysis['valid_to'] = pd.to_datetime(sarysis['valid_to'], errors='coerce')
sarysis.info()
sarysis.nunique()
sarysis.head()

# Šalių pasiskirstymas
sarysis['country'].value_counts()

# Galiojimo trukmė
(sarysis['valid_to'] - sarysis['valid_from']).value_counts()

# Galiojimo pasiskirstymas laike
sarysis['valid_from'].value_counts().to_frame().join(sarysis['valid_to'].value_counts()).plot()
plt.show(); plt.close()

sarysis['valid_to'].value_counts().plot()
plt.show(); plt.close()

# Ar teisingai nurodytas pirminis raktas?
(sarysis.groupby(['commodity', 'unit', 'unit_qualifier', 'country']).size() > 1).sum()
sarysis.groupby(['commodity', 'unit', 'unit_qualifier', 'country']).size().sort_values()

sarysis[['export', 'import']].sum().plot.barh()
plt.show(); plt.close()


# Prekių nomenklatūros prekių kodų sąrašas
prekes = pd.read_xml('16LT.xml', stylesheet='''
<xsl:stylesheet
 version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns="http://rep.xmlstandards.eu/icdts/LT/schemas/ReferenceData.xsd"
 >
  <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <data>
      <xsl:apply-templates select="/ns:ReferenceData/ns:CommodityCode"/>
    </data>
  </xsl:template>
  <xsl:template match="/ns:ReferenceData/ns:CommodityCode">
    <row>
      <code><xsl:value-of select="@code"/></code>
      <indents><xsl:value-of select="@indents"/></indents>
      <suffix><xsl:value-of select="@suffix"/></suffix>
      <import><xsl:value-of select="@import"/></import>
      <export><xsl:value-of select="@export"/></export>
      <excise><xsl:value-of select="@excise"/></excise>
      <valid_from><xsl:value-of select="@validFrom"/></valid_from>
      <valid_to><xsl:value-of select="@validTo"/></valid_to>
      <description_lt><xsl:value-of select="ns:CodeDescription[@languageCode='LT']/@description"/></description_lt>
      <description_en><xsl:value-of select="ns:CodeDescription[@languageCode='EN']/@description"/></description_en>
    </row>
  </xsl:template>
</xsl:stylesheet>
''')
prekes['valid_from'] = pd.to_datetime(prekes['valid_from'])
prekes['valid_to'] = pd.to_datetime(prekes['valid_to'])
#| Out of bounds nanosecond timestamp: 4712-12-31 00:00:00
prekes['valid_to'] = pd.to_datetime(prekes['valid_to'], errors='coerce')
prekes.info()
prekes.nunique()

# Ar teisingai nurodytas pirminis raktas?
(prekes.groupby(['code', 'suffix']).size() > 1).sum()
prekes.groupby(['code', 'suffix']).size().sort_values()

# Galiojimo pasiskirstymas laike
prekes['valid_from'].value_counts().to_frame().join(prekes['valid_to'].value_counts()).plot()
plt.show(); plt.close()

# Export VS Import
prekes[['export', 'import']].sum().plot.barh()
plt.show(); plt.close()

prekes
prekes.head(20)
prekes.nunique()
prekes['indents'].value_counts()
prekes[prekes['indents'] == 12].head(20)

# Matavimo vienetų, naudojamų deklaruojant prekes Lietuvos Respublikos muitinei, sąrašas
units = pd.read_xml('9LT.xml', stylesheet='''
<xsl:stylesheet
 version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns="http://rep.xmlstandards.eu/icdts/LT/schemas/ReferenceData.xsd"
 >
  <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <data>
      <xsl:apply-templates select="/ns:ReferenceData/ns:SimpleItem"/>
    </data>
  </xsl:template>
  <xsl:template match="/ns:ReferenceData/ns:SimpleItem">
    <row>
      <code><xsl:value-of select="@code"/></code>
      <national><xsl:value-of select="@national"/></national>
      <valid_from><xsl:value-of select="@validFrom"/></valid_from>
      <valid_to><xsl:value-of select="@validTo"/></valid_to>
      <description_lt><xsl:value-of select="ns:CodeDescription[@languageCode='LT']/@description"/></description_lt>
      <description_en><xsl:value-of select="ns:CodeDescription[@languageCode='EN']/@description"/></description_en>
    </row>
  </xsl:template>
</xsl:stylesheet>
''')
units['valid_from'] = pd.to_datetime(units['valid_from'])
units['valid_to'] = pd.to_datetime(units['valid_to'])
#| Out of bounds nanosecond timestamp: 4712-12-31 00:00:00
units['valid_to'] = pd.to_datetime(units['valid_to'], errors='coerce')
units.info()
units.nunique()

prekiu_vienetai = (
    sarysis.
    set_index('commodity').
    join(
        prekes.
        set_index('code'),
        rsuffix='_preke'
    ).
    reset_index().
    rename(columns={'index': 'code'}).
    set_index('unit').
    join(
        units.
        set_index('code'),
        rsuffix='_unit'
    )[[
        'code',
        'description_lt',
        'description_en',
        'description_lt_unit',
        'description_en_unit',
    ]]
)
prekiu_vienetai[['code', 'description_lt', 'description_lt_unit']]


# Matavimo vienetų, naudojamų deklaruojant prekes Lietuvos muitinei, patikslintojų kodų sąrašas
unit_qualifiers = pd.read_xml('10LT.xml', stylesheet='''
<xsl:stylesheet
 version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns="http://rep.xmlstandards.eu/icdts/LT/schemas/ReferenceData.xsd"
 >
  <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <data>
      <xsl:apply-templates select="/ns:ReferenceData/ns:SimpleItem"/>
    </data>
  </xsl:template>
  <xsl:template match="/ns:ReferenceData/ns:SimpleItem">
    <row>
      <code><xsl:value-of select="@code"/></code>
      <national><xsl:value-of select="@national"/></national>
      <valid_from><xsl:value-of select="@validFrom"/></valid_from>
      <valid_to><xsl:value-of select="@validTo"/></valid_to>
      <description_lt><xsl:value-of select="ns:CodeDescription[@languageCode='LT']/@description"/></description_lt>
      <description_en><xsl:value-of select="ns:CodeDescription[@languageCode='EN']/@description"/></description_en>
    </row>
  </xsl:template>
</xsl:stylesheet>
''')
unit_qualifiers['valid_from'] = pd.to_datetime(unit_qualifiers['valid_from'])
unit_qualifiers['valid_to'] = pd.to_datetime(unit_qualifiers['valid_to'])
#| Out of bounds nanosecond timestamp: 4712-12-31 00:00:00
unit_qualifiers['valid_to'] = pd.to_datetime(unit_qualifiers['valid_to'], errors='coerce')
unit_qualifiers.info()
unit_qualifiers.nunique()
unit_qualifiers


# Valiutų, naudojamų deklaruojant prekes Lietuvos muitinei, sąrašas
currencies = pd.read_xml('18LT.xml', stylesheet='''
<xsl:stylesheet
 version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns="http://rep.xmlstandards.eu/icdts/LT/schemas/ReferenceData.xsd"
 >
  <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <data>
      <xsl:apply-templates select="/ns:ReferenceData/ns:SimpleItem"/>
    </data>
  </xsl:template>
  <xsl:template match="/ns:ReferenceData/ns:SimpleItem">
    <row>
      <code><xsl:value-of select="@code"/></code>
      <national><xsl:value-of select="@national"/></national>
      <valid_from><xsl:value-of select="@validFrom"/></valid_from>
      <valid_to><xsl:value-of select="@validTo"/></valid_to>
      <description_lt><xsl:value-of select="ns:CodeDescription[@languageCode='LT']/@description"/></description_lt>
      <description_en><xsl:value-of select="ns:CodeDescription[@languageCode='EN']/@description"/></description_en>
      <description_ru><xsl:value-of select="ns:CodeDescription[@languageCode='RU']/@description"/></description_ru>
    </row>
  </xsl:template>
</xsl:stylesheet>
''')
currencies['valid_from'] = pd.to_datetime(currencies['valid_from'])
currencies['valid_to'] = pd.to_datetime(currencies['valid_to'])
#| Out of bounds nanosecond timestamp: 4712-12-31 00:00:00
currencies['valid_to'] = pd.to_datetime(currencies['valid_to'], errors='coerce')
currencies.info()
currencies.nunique()


# Muitinėje naudojamų valiutų kursų sąrašas
rates = pd.read_xml('92LT.xml', stylesheet='''
<xsl:stylesheet
 version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:ns="http://rep.xmlstandards.eu/icdts/LT/schemas/ReferenceData.xsd"
 >
  <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <data>
      <xsl:apply-templates select="/ns:ReferenceData/ns:ExchangeRate"/>
    </data>
  </xsl:template>
  <xsl:template match="/ns:ReferenceData/ns:ExchangeRate">
    <row>
      <currency><xsl:value-of select="@currency"/></currency>
      <rate_eur><xsl:value-of select="@rateEUR"/></rate_eur>
      <valid_from><xsl:value-of select="@validFrom"/></valid_from>
      <valid_to><xsl:value-of select="@validTo"/></valid_to>
    </row>
  </xsl:template>
</xsl:stylesheet>
''')
rates['valid_from'] = pd.to_datetime(rates['valid_from'])
rates['valid_to'] = pd.to_datetime(rates['valid_to'])
rates.info()
rates.nunique()

# Jungiam valiutas su kursais
rates.set_index('currency').join(currencies.set_index('code'), rsuffix='_currency')[[
    'rate_eur',
    'description_lt',
    'description_en',
    'description_ru',
]].head()

rates.set_index('currency').join(currencies.set_index('code'), rsuffix='_currency')[[
    'rate_eur',
    'valid_from',
    'valid_to',
    'description_lt',
    'description_en',
    'description_ru',
]].loc[['USD', 'RUB']].head()

# Galiojimo trukmė
(rates['valid_to'] - rates['valid_from']).value_counts()
