"""
 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :conda create -n projet python pandas numpy ..........
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Chargement des données
df = pd.read_csv(r"C:\SAE 6-01\projet_notebook\ds_salaries.csv")


### 2. Exploration visuelle des données
st.title("📊 Visualisation des Salaires en Data Science")
st.text("")
st.text("Auteurs : COCHET Théo - VERLY-LAGADEC Corentin")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")
if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head())


#Statistique générales avec describe pandas 
st.subheader("📌 Statistiques générales")
st.write(df.describe())


### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
st.subheader("📈 Distribution des salaires en France")

hist_data = df[df["company_location"] == "FR"]
fig = px.box(hist_data, x='job_title', y='salary_in_usd', color='experience_level')
st.plotly_chart(fig)

st.text("")
st.text("Les seniors et les cadres sont mieux payés que les autres employés.")
st.text("")

### 4. Analyse des tendances de salaires :
st.subheader("👁️‍🗨️ Analyse des tendances de salaires")
selected_option = st.selectbox('Choisir une option', options=['experience_level', 'employment_type', 'job_title', 'company_location'])
vary = df.groupby(selected_option, as_index=False)['salary_in_usd'].mean()
fig2 = px.bar(vary, x=selected_option, y="salary_in_usd")
st.plotly_chart(fig2)

st.text("")
st.text("On observe différentes informations liées au niveau d'expérience, au type de contrat, au titre du travail et au pays de l'entreprise.")
st.text("")

### 5. Corrélation entre variables
numeric_df = df.select_dtypes(include=[np.number])
ndf = numeric_df.corr()
st.subheader("🔗 Corrélations entre variables numériques")
fig3, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(ndf, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig3)


### 6. Analyse interactive des variations de salaire
st.subheader("🧪 Analyse interactive des variations de salaire")
df2 = df["job_title"].value_counts()
top10 = df2.head(10)
top10data = top10.index.tolist()
x = df[df["job_title"].isin(top10data)]
w = x.groupby('job_title')['salary_in_usd'].mean()
fig4 = px.line(w, x = w.index, y = 'salary_in_usd')
st.plotly_chart(fig4)

st.text("")
st.text("Courbe représentant le salaire en fonction du titre.")
st.text("")

### 7. Salaire médian par expérience et taille d'entreprise
st.subheader("🤓 Salaire médian par expérience et taille d'entreprise")
o = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median()
st.write(o)


### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages
st.subheader("📍 Filtrer les données par salaire utilisant st.slider pour selectionner les plages")
mindata = df["salary_in_usd"].min()
maxdata = df["salary_in_usd"].max()

min_slider, max_slider = st.slider(label = "glisseur",
    min_value=mindata,
    max_value=maxdata,
    value=(mindata, maxdata)
)
salarydata = df[(df["salary_in_usd"] >= min_slider) & (df["salary_in_usd"] <= max_slider)]
st.write(salarydata)

st.text("")
st.text("Lorsque le filtre est plus haut sur la plage, on observe une plus grande proportion de seniors, des entreprises de taille medium-large et localisées aux États-Unis.")
st.text("")

### 9. Impact du télétravail sur le salaire selon le pays
st.subheader("🖥️ Impact du télétravail sur le salaire selon le pays")
t = df.groupby("company_location").apply(lambda x: x["remote_ratio"].corr(x["salary_in_usd"]))
st.write(t)

st.text("")
st.text("Nous avons fait le choix de laisser les 'None' pour observer les pays dont leurs employés ne travaillent pas en distanciel.")
st.text("Dans la majorité des cas, le télétravail a une influence négative sur le salaire. Par exemple, le Danemark fait partie des exceptions, avec une corrélation à 0.92.")
st.text("")

### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
st.subheader("🎞️ Filtrage avancé des données")
sel_exp = st.multiselect(label = "Sélectionnez le niveau d'expérience", options = df["experience_level"].unique(), default = df["experience_level"].unique())
sel_siz = st.multiselect(label = "Sélectionnez la taille d'entreprise", options = df["company_size"].unique(), default = df["company_size"].unique())
z = df[(df["experience_level"].isin(sel_exp)) & (df["company_size"].isin(sel_siz))]
st.write(z)

st.text("")
st.text("Par défaut, toutes les options sont disponibles.")
st.text("")

st.text("")
gif_url = "https://media1.tenor.com/m/9AOAZZ4YN_oAAAAd/blackbeard-blackbeard-writing.gif"
st.image(gif_url)