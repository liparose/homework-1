# SETUP
import streamlit as st

import numpy as np
import pandas as pd
import altair as alt

from pathlib import Path
import datetime as dt
from datetime import datetime

#-------------------

# DATA
# Data import
PARENT_PATH = str(Path().resolve().parent) + "/"
PATH = "data/"
SUBPATH = "external/"
FILE = "data"
FORMAT = ".csv"

PARENT_PATH

df = pd.read_csv(PARENT_PATH + PATH + SUBPATH + FILE + FORMAT)

# Data transformation
df = df.rename(columns={ 
    "superbowl_ads_dot_com_url": "url"
}, errors="raise")

del df['youtube_url']
del df['url']
#-------------------
list_nominal = ["funny", "show_product_quickly", "patriotic", "celebrity", "danger", "animals", "use_sex"]

for i in list_nominal:
    df[i] = df[i].astype("category")

dummy_nominal = pd.get_dummies(df[list_nominal],  prefix_sep='__').astype('category')

dummy_nominal.drop(columns=['funny__False', 'show_product_quickly__False', 'patriotic__False', 'celebrity__False', 'danger__False', 'animals__False', 'use_sex__False'], inplace=True)
#-------------------
liste = df[['brand']].copy()

for i in dummy_nominal:
    dummy_nominal[i] = dummy_nominal[i].astype("int64")

liste = liste.join(dummy_nominal)

liste = liste.rename(columns={ 
            "funny__True": "funny",
            "show_product_quickly__True": "product",
            "patriotic__True": "patriotic",
            "celebrity__True": 'celebrity',
            "danger__True": "danger",
            "animals__True": "animals",
            "use_sex__True": "sex"
}, errors="raise")
#-------------------
final = liste.groupby(['brand']).agg({
    'funny': ['sum'],
    'product': ['sum'],
    'patriotic': ['sum'],
    'celebrity': ['sum'],
    'danger': ['sum'],
    'animals': ['sum'],
    'sex': ['sum']
    }).reset_index()

final.columns = final.columns.droplevel(level=1)
#-------------------
#df Funny erstellen
eins = final.groupby(['brand', 'funny']).size().reset_index(name='category')
funny =pd.DataFrame(eins, columns=["brand", "funny", "category"])
funny.rename(columns={"funny": "count"}, inplace=True, errors="raise")
for i in funny:
    funny.replace(1, "funny", inplace=True)

#df product erstellen
zwei = final.groupby(['brand', 'product']).size().reset_index(name='category')
product =pd.DataFrame(zwei, columns=["brand", "product", "category"])
product.rename(columns={"product": "count"}, inplace=True, errors="raise")
for i in product:
    product.replace(1, "product", inplace=True)

#df patriotic erstellen
drei = final.groupby(['brand', 'patriotic']).size().reset_index(name='category')
patriotic =pd.DataFrame(drei, columns=["brand", "patriotic", "category"])
patriotic.rename(columns={"patriotic": "count"}, inplace=True, errors="raise")
for i in patriotic:
    patriotic['category'].replace(1, "patriotic", inplace=True)

#df celebrity erstellen
vier = final.groupby(['brand', 'celebrity']).size().reset_index(name='category')
celebrity =pd.DataFrame(vier, columns=["brand", "celebrity", "category"])
celebrity.rename(columns={"celebrity": "count"}, inplace=True, errors="raise")
for i in celebrity:
    celebrity.replace(1, "celebrity", inplace=True)

#df danger erstellen
fuenf = final.groupby(['brand', 'danger']).size().reset_index(name='category')
danger =pd.DataFrame(fuenf, columns=["brand", "danger", "category"])
danger.rename(columns={"danger": "count"}, inplace=True, errors="raise")
for i in danger:
    danger.replace(1, "danger", inplace=True)

#df animals erstellen
sechs = final.groupby(['brand', 'animals']).size().reset_index(name='category')
animals =pd.DataFrame(sechs, columns=["brand", "animals", "category"])
animals.rename(columns={"animals": "count"}, inplace=True, errors="raise")
for i in animals:
    animals.replace(1, "animals", inplace=True)

#df sex erstellen
sieben = final.groupby(['brand', 'sex']).size().reset_index(name='category')
sex =pd.DataFrame(sieben, columns=["brand", "sex", "category"])
sex.rename(columns={"sex": "count"}, inplace=True, errors="raise")
for i in sex:
    sex['category'].replace(1, "sex", inplace=True)

#-------------------
finalfinal = pd.concat([funny, product, patriotic, celebrity, danger, animals, sex], ignore_index=True)
for i in finalfinal:
    finalfinal['count'] = finalfinal['count'].astype(int)
finalfinal.info()

#-------------------
# START OF APP

#-------------------
# SIDEBAR

# Header
st.sidebar.header("Wie schätzt Du dich ein?")

# Make a slider
impact = st.sidebar.slider('Wie stark lässt du dich von Werbung beeinflussen?', 0, 10, 1)

# Show output of slider selection
st.sidebar.write("Mein Beeinflussung liegt bei: ", impact)

#------------------
# HEADER

# Title of our app
st.title("Unsere Ergebnisse")
# Add header
st.header("Im Rahmen der Homework 1")

#-------------------
# BODY
st.write("Im Folgenden sind unterschiedliche Diagramme erzeugt worden, welche bestimmte Beziehungen darstellen.")

#-------------------

# Bar chart
st.subheader("Bar chart")
st.write("Hier ist zu sehen, welche Marke wie oft sexuell geduldete Inhalte in ihrer Werbung verwendet.")

c = alt.Chart(df).mark_bar().encode(
    alt.X('brand', axis=alt.Axis(title='Brand')),
    alt.Y('count(use_sex)', axis=alt.Axis(title='Number of sexual content in advertising')),
    ).properties(
        width=900,
        height=400
    ).configure_title(
        fontSize=16,
        font='Helvetica',
        anchor='start',
        color='black'
    ).interactive()

st.altair_chart(c, use_container_width=True)


# Bar chart
st.subheader("Line chart")
st.write("Diese Grafik zeigt die absolute Häufigkeit der Werbeschaltungen von Unternehmen, sortiert nach Jahren.")

line = alt.Chart(df).mark_line().encode(
    alt.X('year'),
    alt.Y('count()', axis=alt.Axis(title='Ads placed', format='d')))

point = alt.Chart(df).mark_circle().encode(
    alt.X('year'),
    y='count()'
).properties(
    title='Number of advertising clips placed',
    width=900,
    height=400
).interactive()

c = line + point
st.altair_chart(c, use_container_width=True)
   

# Bar chart
st.subheader("Bar chart")
st.write("In diesem Diagramm werden die am häufigsten verwendeten Kategorien, sortiert nach Unternehmen, dargestellt.")

source=finalfinal

bars = alt.Chart(source).mark_bar().encode(
    x=alt.X('sum(count):Q', stack='normalize', title='percentage distribution of frequency'),
    y=alt.Y('brand'),
    color=alt.Color('category')
).properties(
    title='Distribution of categories by brands',
    width=900,
    height=400
)

text = alt.Chart(source).mark_text(align='center', dx=-11, dy=3, color='white').encode(
    x=alt.X('sum(count):Q', stack='normalize'),
    y=alt.Y('brand:N'),
    detail='category:N',
    text=alt.Text('sum(count):Q', format='.0f')
)

c = bars + text
st.altair_chart(c, use_container_width=True)


# Map
st.subheader("Häufigkeitsverteilung")
st.write("In diesem letzten Diagramm wird die Verteilung der Kategorien nach den Marken dargestellt.") 

source = df

# Configure common options
base = alt.Chart(source).transform_aggregate(
    total='count()',
    groupby=['celebrity', 'funny']
).encode(
    alt.X('funny:O', scale=alt.Scale(paddingInner=0)),
    alt.Y('celebrity:O', scale=alt.Scale(paddingInner=0)),
).properties(
    title='Distribution of categories by brands',
    width=90,
    height=100
)

# Configure heatmap
heatmap = base.mark_rect().encode(
    color=alt.Color('total:Q',
        scale=alt.Scale(scheme='viridis'),
        legend=alt.Legend(direction='horizontal')
    )
)

# Configure text
text = base.mark_text(baseline='middle').encode(
    text='total:Q',
    color=alt.condition(
        alt.datum.num_cars > 100,
        alt.value('black'),
        alt.value('white')
    )
)

# Draw the chart
c = heatmap + text
st.altair_chart(c, use_container_width=True)

#-------------------
