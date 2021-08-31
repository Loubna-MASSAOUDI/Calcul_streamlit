#the libraries used to create the app
import streamlit as st
import pandas as pd

from first import calculate_ratios
from first import groupby_pays
from first import groupby_region

import os
import jinja2
import pdfkit
import base64

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#the template used to create the PDF Table
TABLE_TEMPLATE_FILE = 'table_template.html'
#the directory of the HTML version of the table
BASE_HTML = os.path.join(os.getcwd())
#the directory of the pdf output
PDF_TARGET_FILE = os.path.join(os.getcwd(),'output.pdf')
#the path to the wkhtmltopdf library to work with pdfkit
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#the configuration of the wkhtmltopdf library
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#upload the data
@st.cache(allow_output_mutation=True)
#loading the data either from xlsx or csv format
def load_data(data_file):
    dp = " "
    if data_file is not None:
        if data_file.name[-4:] == 'xlsx':
            dp = pd.read_excel(data_file,header = None, index_col= 0)
            dp = dp.rename(index={ind: ind.strip() for ind in dp.index})
        elif data_file.name[-3:] == 'csv':
            dp = pd.read_csv(data_file,header = None, index_col=0)
            dp = dp.rename(index={ind: ind.strip() for ind in dp.index})
        else:
            st.write("Please select a csv or an excel file")
    return dp.T

#choose what you want to calculate (region, pays ou ville)
def choice(df):
    if df is not None:
        #annee sidebar
        st.sidebar.subheader('Créer le rapport')
        ann =df["Annee"].unique()
        annee = st.sidebar.selectbox('Choisir l année ', ann)

        #choose the region, pays, or ville
        rpv = st.sidebar.radio('Choisir le type de calcul',("Région","Pays","Ville"))
        if rpv == "Région":
            col = df["Region"].unique()
            choice = st.sidebar.selectbox("Région", col)
        elif rpv == "Pays":
            col = df["Pays"].unique()
            choice = st.sidebar.selectbox("Pays", col)
        else: 
            col = df["Libellés des Variables"].unique()
            choice = st.sidebar.selectbox("Ville",col)
    return annee, rpv, choice

#calculate the ratios + filtering 
def calcul(df, rpv, annee, choix ):
    if rpv == 'Région':
        result = groupby_region(df)
        filtered_data = result[(result["Region"]== choix) & (result["Annee"] == annee)]

    elif rpv == 'Pays':
        result = groupby_pays(df)
        filtered_data = result[(result["Pays"]== choix) & (result["Annee"] == annee)]

    else:
        result = calculate_ratios(df)
        all  = result[(result["Libellés des Variables"]== choix) & (result["Annee"] == annee)]
        filtered_data = all[["Pays",
                        "Region",
                        "Population",
                        "Annee",
                        "Recette réelles de fonctionnement en dollar", 
                        "Dépense reelles de fonctionnement en dollar",
                        "Epargne Brute en dollar",
                        "Depenses totales / habitant en dollar",
                        "Recettes réelles fonctionnement / habitant en dollar",
                        "Dépenses réelles fonctionnement / habitant en dollar",
                        "Dépense d'équipement / habitant en dollar",
                        "Recette réelles de fonctionnement en Euro",
                        "Dépense reelles de fonctionnement en Euro",
                        "Epargne Brute en Euro",
                        "Depenses totales / habitant en Euro",
                        "Recettes réelles fonctionnement / habitant en Euro",
                        "Dépenses réelles fonctionnement / habitant en Euro",
                        "Dépense d'équipement / habitant en Euro",
                        "Frais de personnel / Recettes de fonctionnement",
                        "Marge d'autofinancement",
                        "Taux de couverture des dépenses de fonctionnement"]]
        
    return filtered_data

#create html table
def create_html_table(df):
   templateLoader = jinja2.FileSystemLoader(searchpath="./")
   templateEnv = jinja2.Environment(loader=templateLoader)
   template = templateEnv.get_template(TABLE_TEMPLATE_FILE)
   outputText = template.render(df=df)
   file_name = 'result.html'
   file_name = os.path.join(BASE_HTML, 'result.html')

   html_file = open(file_name,'w')
   html_file.write(outputText)
   html_file.close()


#create pdf files
def create_pdf_files():
    options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
     ],
    'no-outline': None,
    'footer-right': '[page]/[topage]',
    'footer-line': None,
    'footer-left': '[isodate]',
    'footer-spacing': '10.0', 
    'header-spacing': '10.0', 
    'header-line': None, 
    'print-media-type': None
    }
    file_name = 'result.html'
    source_code = ""
    if os.path.isfile(file_name):
        html_file = open(file_name,'r')
        source_code += html_file.read()
    pdfkit.from_string(source_code, PDF_TARGET_FILE, configuration = config, options=options)


#main
if __name__ == "__main__":
    #The file uploader
    data_file = st.file_uploader("Telechargez la base de données",type = ["csv","xlsx"])

    #load the data and mutate it
    if data_file is not None: 
        df = load_data(data_file)
    

        #watch raw data
        if st.checkbox("Voir la base de données compléte",False):
            st.subheader('Raw  data')
            st.dataframe(df.T)

        #mutate the data
        numeric_columns = [col for col in df.columns if col not in ["Region", "Pays", "Libellés des Variables"]]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

        #select the city, the country, or the continent

        annee, rpv, choix = choice(df)

        #calculate the ratios
        result = calcul(df, rpv,annee, choix)
        t = result.T.reset_index()
        
        st.table(result.T)
        
        #Export as PDF
        if st.button("Créer le rapport en PDF"):
            st.info('Génerez le html file')
            create_html_table(t)
            st.info('Génerze le pdf file')
            create_pdf_files()
            st.success('C est fait') 

            
            with open(PDF_TARGET_FILE,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)
        
        #Visualisation 
        #do the axis
        st.sidebar.subheader('Créer la Visualisation')
        c = st.sidebar.radio('Choisir le type de visualisation',("Région","Pays","Ville"))
        if c == "Région":
            xa = "Region"
        elif c == "Pays":
            xa = "Pays"
        else: 
            xa = "Libellés des Variables"

        #do the yaxis
        ed = st.sidebar.radio('Choisir le devise',("Dollar", "Euro")) 

        if ed == "Dollar":
                
            ya = st.sidebar.selectbox('Choisir le yaxis', ("Recette réelles de fonctionnement en dollar",
                                            "Dépense reelles de fonctionnement en dollar",
                                            "Epargne Brute en dollar",
                                            "Depenses totales / habitant en dollar",
                                            "Recettes réelles fonctionnement / habitant en dollar",
                                            "Dépenses réelles fonctionnement / habitant en dollar",
                                            "Frais de personnel / Recettes de fonctionnement",
                                            "Marge d'autofinancement",
                                            "Taux de couverture des dépenses de fonctionnement"))
        else:
            ya = st.sidebar.selectbox('Choisir le yaxis', ("Recette réelles de fonctionnement en Euro",
                                                "Dépense reelles de fonctionnement en Euro",
                                                "Epargne Brute en Euro",
                                                "Depenses totales / habitant en Euro",
                                                "Recettes réelles fonctionnement / habitant en Euro",
                                                "Dépenses réelles fonctionnement / habitant en Euro",
                                                "Dépense d'équipement / habitant en Euro",
                                                "Frais de personnel / Recettes de fonctionnement",
                                                "Marge d'autofinancement",
                                                "Taux de couverture des dépenses de fonctionnement"))
        
        vis = calculate_ratios(df)
        vis = vis[vis["Annee"] == annee]
        st.write(vis.head())

        if st.checkbox("Visualisation de data",False):
        
            fig = Figure(figsize = (14,6), dpi = 80)
            ax = fig.subplots()
            sns.barplot(x=vis[xa],y=vis[ya], color = 'goldenrod' ,ax=ax)
            st.pyplot(fig)



    

    