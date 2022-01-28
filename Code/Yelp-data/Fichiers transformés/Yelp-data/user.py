# -*- coding: cp1252 -*-
import nltk
import time
import datetime
from datetime import date
from nltk import re
from nltk import FreqDist
from operator import itemgetter
from nltk import defaultdict

class User(object):
    user_id = ""
    name = ""
    friends = ""
    yelping_since =  datetime.date(1900,1,1)


    def __init__(self, user_id, name, friends, yelping_since):
        self.user_id = user_id
        self.name = name
        self.friends = friends
        self.yelping_since = yelping_since

        
def make_user(user_id, name, friends, yelping_since):
    user = User(user_id, name, friends, yelping_since)
    return user

def convertir_date(date):
    Liste_entier = date.split("-")
    a = int(Liste_entier[0])
    m = int(Liste_entier[1])
    return datetime.date(a,m,1)

def ecrire_dans_fichier(user,fichier):
    fichier.write(user.user_id+"|"+user.name+"|"+user.friends+"|"+str(user.yelping_since.year)+"-"+str(user.yelping_since.month)+"\n")


def Filtrer(friends,Liste_users_id_all):                                                                 # Supprimer de la liste d'amis, les utilisateurs qui n'éxistent pas apres prétraitement
    Liste_friends = friends.split(",")
    Filtrer_Liste_friends = [idf for idf in Liste_friends if idf in Liste_users_id_all]
    Chaine_friends = (",").join(Filtrer_Liste_friends)
    return Chaine_friends

Liste_users_id_all = open("users_id.txt","rU").read().split("\n")                                        # Ouverture du fichier en lecture

Liste_users = open("yelp_academic_dataset_user.json","rU").readlines()                                   # Ouverture du fichier user en lecture

fichier = open("users.txt","w")                                                                          # Ouverture du fichier users en écriture

fichier2 = open("C:\Users\Mounira\Desktop\App Finale PFE\PFE3\Input\users.txt","w")                 # Ouverture du fichier users en écriture

pattern = r"""(?x)                                                                                                    
          "user_id":\s"(.+?)"
"""

pattern1 = r"""(?x)                                                                                                    
          "name":\s"(.+?)"
"""

pattern2 = r"""(?x)                                                                                                    
          "review_count":\s(\d+)
"""

pattern3 = r"""(?x)                                                                                                    
          "average_stars":\s(.*?)\,
"""

pattern4 = r"""(?x)                                                                                                    
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

pattern5 = r"""(?x)                                                                                                    
          "friends":\s\[(.*?)\]
"""

pattern6 = r"""(?x)                                                                                                    
          "yelping_since":\s"(.*?)"
"""

Compt = 0

Liste_users_final = []

for line in Liste_users:
    user_id = re.findall(pattern,line)[0]
    if (user_id in Liste_users_id_all) :
        name = re.findall(pattern1,line)[0]
        review_count = re.findall(pattern2,line)[0]
        average_stars = re.findall(pattern3,line)[0]
        votes = re.findall(pattern4,line)[0]
        funny = re.findall(pattern7,votes)[0]
        useful = re.findall(pattern8,votes)[0]
        cool = re.findall(pattern9,votes)[0]
        friends = re.findall(pattern5,line)[0]
        friends = re.sub(r"\s+|\"","",friends)
        friends = Filtrer(friends,Liste_users_id_all)                                                   # Supprimer de la liste d'amis les utilisateurs ne vérifiant pas les critéres
        yelping_since = re.findall(pattern6,line)[0]
        date_final = convertir_date(yelping_since)
        u = make_user(user_id, name, friends, date_final)
        Liste_users_final.append(u)
        fichier.write(line)
        Compt = Compt +1

fichier.close()

sorted_Liste_users = sorted(Liste_users_final, key=lambda x: x.yelping_since)                           # Trier les utilisateurs par date d'inscription
for user in sorted_Liste_users:
    ecrire_dans_fichier(user,fichier2)
fichier2.close()


print "\nNombre d'users : %d"%(Compt)                                                                   # Affichage du nombre d'utilisateurs
