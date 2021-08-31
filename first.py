import pandas as pd
#first.py contains the functions used to calculate the financial ratios needed

#function to calculate all the financial ratios
def calculate_ratios(data):
   
    #dollar
    data["Recette réelles de fonctionnement en dollar"] = data["Total recettes réelles de fonctionnement"] * data["Dollar"]
    data["Dépense reelles de fonctionnement en dollar"] = data["Dépenses de fonctionnement (hors prélèvement)"] * data["Dollar"]
    data["Epargne Brute en dollar"] = (data["Total recettes réelles de fonctionnement"] - data["Dépenses de fonctionnement (hors prélèvement)"])* data["Dollar"]
    data["Depenses totales / habitant en dollar"] = ((data["Dépenses de fonctionnement (hors prélèvement)"] + data["Dépenses d'investissement"]) / data["Population"])* data["Dollar"]
    data["Recettes réelles fonctionnement / habitant en dollar"] = (data["Total recettes réelles de fonctionnement"]/ data['Population'])* data["Dollar"]
    data["Dépenses réelles fonctionnement / habitant en dollar"] = (data["Dépenses de fonctionnement (hors prélèvement)"]/ data['Population'])* data["Dollar"]
    data["Dépense d'équipement / habitant en dollar"] =  ((data["Dépenses d'investissement"] - data["dont Remboursements d'emprunts (Amortissement du capital)"]) / data["Population"])* data["Dollar"]

    #Euro
    data["Recette réelles de fonctionnement en Euro"] = data["Total recettes réelles de fonctionnement"] * data["Euro"]
    data["Dépense reelles de fonctionnement en Euro"] = data["Dépenses de fonctionnement (hors prélèvement)"] * data["Euro"]
    data["Epargne Brute en Euro"] = (data["Total recettes réelles de fonctionnement"] - data["Dépenses de fonctionnement (hors prélèvement)"]) * data["Euro"]
    data["Depenses totales / habitant en Euro"] = ((data["Dépenses de fonctionnement (hors prélèvement)"] + data["Dépenses d'investissement"]) / data["Population"])* data["Euro"]
    data["Recettes réelles fonctionnement / habitant en Euro"] = (data["Total recettes réelles de fonctionnement"]/ data['Population'])* data["Euro"]
    data["Dépenses réelles fonctionnement / habitant en Euro"] = (data["Dépenses de fonctionnement (hors prélèvement)"]/ data['Population'])* data["Euro"]
    data["Dépense d'équipement / habitant en Euro"] =  ((data["Dépenses d'investissement"] - data["dont Remboursements d'emprunts (Amortissement du capital)"]) / data["Population"])* data["Euro"]


    #pourcentage
    data["Frais de personnel / Recettes de fonctionnement"] = data["dont Charges de personnel"] / data["Total recettes réelles de fonctionnement"]
    data["Marge d'autofinancement"] = (data["Dépenses de fonctionnement (hors prélèvement)"] + data["dont Remboursements d'emprunts (Amortissement du capital)"]) / data["Total recettes réelles de fonctionnement"]
    data["Taux de couverture des dépenses de fonctionnement"] = ((data["Total recettes de fonctionnement"] - data["Total Dépenses de fonctionnement"]) - data["dont Remboursements d'emprunts (Amortissement du capital)"]) / data["Total recettes de fonctionnement"]

    
    return data

#group the calculated ratios by country
def groupby_pays(data):

    dp = calculate_ratios(data)
    dp = dp.groupby(["Pays","Annee"])[["Recette réelles de fonctionnement en dollar",
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
                                        "Taux de couverture des dépenses de fonctionnement"]].mean().reset_index()

    
    return dp

#groupby the calculated ratios by region
def groupby_region(data):
    dr = calculate_ratios(data) 
    dr = dr.groupby(["Region","Annee"])[["Recette réelles de fonctionnement en dollar",
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
                                        "Taux de couverture des dépenses de fonctionnement"]].mean().reset_index()
    return dr



   

    