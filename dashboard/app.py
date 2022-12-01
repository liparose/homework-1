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

# Obtain home path
home_path = str(Path.home())

# Data import
    #PARENT_PATH = str(Path().resolve().parent) + "/"
    #PATH = "data/"
    #SUBPATH = "external/"
    #FILE = "data"
    #FORMAT = ".csv"

    #PARENT_PATH

    #df = pd.read_csv(PARENT_PATH + PATH + SUBPATH + FILE + FORMAT)

# Data transformation
    # df['Date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    #df = df.rename(columns={ 
    #            "superbowl_ads_dot_com_url": "url"
    #}, errors="raise")

    #del df['youtube_url']
    #del df['url']


#-------------------
# START OF APP

#-------------------
# SIDEBAR

# Header
st.sidebar.header("Wie schätzt du dich ein?")

# Make a slider
impact = st.sidebar.slider('Wie stark lässt du dich von Werbung beeinflussen?', 0, 10, 1)

# Show output of slider selection
st.sidebar.write("Mein Beeinflussung liegt bei: ", impact)

#------------------
# HEADER

# Title of our app
st.title("Unsere Ergebnisse von der Homework 1")
# Add header
st.header("Homework 1")

#-------------------
# BODY

#-------------------

# Bar chart
st.subheader("Bar chart")
st.write("Hier ist zu sehen, welche Marke wie oft sexuell geduldete Inhalte in ihrer Werbung verwendet.")

c = alt.Chart(df).mark_bar().encode(
    alt.X('brand', axis=alt.Axis(title='Brand')),
    alt.Y('count(use_sex)', axis=alt.Axis(title='Number of sexual content in advertising')),
    ).properties(
        title='Which brands use the most sexual content in their advertising?',
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

#import
    #finalfinal = pd.concat([funny, product, patriotic, celebrity, danger, animals, sex], ignore_index=True)
    #for i in finalfinal:
    #    finalfinal['count'] = finalfinal['count'].astype(int)
    #finalfinal.info()
#-----------------

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

#-------------------
