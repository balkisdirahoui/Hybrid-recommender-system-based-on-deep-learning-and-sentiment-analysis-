# -*- coding: cp1252 -*-
import nltk
import time
import datetime
from datetime import date
from nltk import re
from nltk import FreqDist
from operator import itemgetter
from nltk import defaultdict

class Review(object):
    idf_review = ""
    idf_user = ""
    idf_buisness = ""
    stars = 0
    date =  datetime.date(1900,1,1)
    funny = 0
    useful = 0
    cool = 0

    def __init__(self, idf_review, idf_user, idf_buisness, stars, date, funny, useful, cool):
        self.idf_review = idf_review 
        self.idf_user = idf_user
        self.idf_buisness = idf_buisness
        self.stars = stars
        self.date = date
        self.funny = funny
        self.useful = useful
        self.cool = cool
        
def make_review(idf_review, idf_user, idf_buisness, stars, date, funny, useful, cool):
    review = Review(idf_review, idf_user, idf_buisness, stars, date, funny, useful, cool)
    return review

def convertir_date(date):
    Liste_entier = date.split("-")
    a = int(Liste_entier[0])
    m = int(Liste_entier[1])
    j = int(Liste_entier[2])
    return datetime.date(a,m,j)

def ecrire_dans_fichier(review,fichier):
    fichier.write(review.idf_review+"|"+review.idf_user+"|"+review.idf_buisness+"|"+review.stars+"|"+str(review.date)+"|"+review.funny+"|"+review.useful+"|"+review.cool+"\n")


fichier = open("restaurants.txt","rU").read()                                                # Ouverture du fichier restaurants en lecture

pattern = r"""(?x)                                                                                                    
          "business_id":\s"(.+?)"
"""

pattern2 = r"""(?x)                                                                                                    
          "user_id":\s"(.+?)"
"""

pattern3 = r"""(?x)                                                                                                    
          "review_id":\s"(.+?)"
"""

pattern4 = r"""(?x)                                                                                                    
          "stars":\s(\d+)
"""

pattern5 = r"""(?x)                                                                                                    
          "date":\s"(.*?)"
"""

pattern6 = r"""(?x)                                                                                                    
          "votes":\s({.*?})
"""

pattern7 = r"""(?x)                                                                                                    
          "funny":\s(\d+)
"""

pattern8 = r"""(?x)                                                                                                    
          "useful":\s(\d+)
"""

pattern9 = r"""(?x)                                                                                                    
          "cool":\s(\d+)
"""

Liste_id_restaurant = re.findall(pattern,fichier)                                        # Récuperer les Identifiants des restaurants

print "\nNombre de restaurants : %d"%(len(Liste_id_restaurant))                          # Affichage du nombre de restaurants

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

fichier2 = open("yelp_academic_dataset_review.json","rU").readlines()                    # Ouverture du fichier review en lecture

fichier3 = open("reviews.txt","w")                                                       # Ouvrir le fichier en écriture

fichier4 = open("users_id.txt","w")                                                      # Ouvrir le fichier en écriture

dic_eval = defaultdict(int)                                                              # Dictionnaire d'entier : clé : ID user , valeurs : NB d'évaluations sur des restaurant

ligne_restaurant = []                                                                    # Sauvegarder les lignes de restaurants

Liste_users=[]                                                                           # IDFs des users ayant fait un nombre d'évaluation > Seuil

compt2 = 0                                                                               # Nombre d'évaluations sur des restaurants

for ligne in fichier2:                                                                   # Parcourir les instances d'évaluations
    idf_buisness = re.findall(pattern, ligne)
    if idf_buisness[0] in Liste_id_restaurant:
        compt2 = compt2+1
        ligne_restaurant.append(ligne)
        idf_user = re.findall(pattern2, ligne)
        dic_eval[idf_user[0]] = dic_eval[idf_user[0]]+1
        
compt3 = len(dic_eval.keys())

print "\nNombre d'évaluations sur des restaurants : %d"%(compt2)                         # Affichage du nombre d'évaluations sur des restaurants 

print "\nNombre d'users ayant fait des évaluations sur des restaurants  : %d"%(compt3)   # Affichage du nombre d'users ayant fait des évaluations sur des restaurants

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

compt5=0                                                                                 # Nombre de reviews d'utilisateurs ayant fait un nb d'évaluations sur des restaurants > Seuil

for id_user in dic_eval:                                                                 # Sauvegarder les users ayant fait plus de 4 évaluation
    if dic_eval[id_user]>9:
        Liste_users.append(id_user)
        compt5=compt5+dic_eval[id_user]
        
compt4 = len(Liste_users)                                                                # Nombre d'users ayant fait un nb d'évaluations sur des restaurants > Seuil

print "\nNombre de reviews d'utilisateurs ayant fait un nb d'évaluations sur des restaurants > Seuil  : %d"%(compt5)   
       
print "\nNombre d'users ayant fait un nb d'évaluations sur des restaurants > Seuil  : %d"%(compt4)   

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

for id_user in Liste_users:
    fichier4.write(id_user+"\n")                                                        # Inserer les instances d'users ayant fait des reviews sur restaurant dans le fichier user_id_all

fichier4.close()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

Liste_reviews_all = []

for ligne in ligne_restaurant:                                                           # Parcourir les instances d'évaluations
    idf_user = re.findall(pattern2, ligne)[0]
    if (idf_user in Liste_users):
        idf_buisness = re.findall(pattern, ligne)[0]
        idf_review = re.findall(pattern3, ligne)[0]
        stars = re.findall(pattern4, ligne)[0]
        date = re.findall(pattern5, ligne)[0]
        votes = re.findall(pattern6, ligne)[0]
        funny = re.findall(pattern7,votes)[0]
        useful = re.findall(pattern8,votes)[0]
        cool = re.findall(pattern9,votes)[0]
        fichier3.write(ligne)
        date_final = convertir_date(date)
        u = make_review(idf_review, idf_user, idf_buisness, stars, date_final, funny, useful, cool)
        Liste_reviews_all.append(u)
fichier3.close()

sorted_Liste_reviews_all = sorted(Liste_reviews_all, key=lambda x: x.date)               # Trier les évaluations par date
fichier5 = open("C:\Users\Mounira\Desktop\App Finale PFE\PFE3\Input/reviews.txt","w")
for review in sorted_Liste_reviews_all:
    ecrire_dans_fichier(review,fichier5)
fichier5.close()
