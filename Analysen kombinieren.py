#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Zeitdaten der News Headlines-Datensatz formatieren 
import locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, locale.normalize("en"))
df['date']=pd.to_datetime(df['date'], format='%b-%d-%y')


# In[ ]:


#Einstellen der Spalte 'Datum' von Headlines-Datensatz als Indexspalte
df.set_index('date', inplace= True)


# In[ ]:


#Sortieren der Daten nach dem Index'Datum'
asset = asset.sort_index(ascending=False, axis=0)


# In[ ]:


#Duplikate löschen
df = df.loc[~df.index.duplicated(keep='first')]


# In[ ]:


#Verketten der 2 Datensätze
result = pd.concat([asset, df], axis=1)
result = result.sort_index(ascending=False, axis=0)


# In[ ]:


#die Spalten des gesamten Ergebnisses neu anordnen
result = result[['Close', 'compound', 'negative', 'neutral', 'positive', 'Prediction','Open', 'High', 'Low', 'Volume']]
print(result)

