#Part of an application to quickly convert Salty Marshmallow baking recipes to metric

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

#Simply makes a df which has very many baking ingredients in imperial, and gives their metric (volume(mL) and weight(g)) counterpart. Always assumes 1 cup of the item
#

#Format will be a dictionary {'Ingredient' : ['Volume', 'Weight']}
#
COL_NAMES = ['Ingredient', 'Vol(mL)', 'Mass(g)']

CUPS_FROM_ANY = 'Cups'

CUPS_TO_ML = 236.55

def add_ingredient(ingr, vol, mass):
    entry = [ingr, vol, mass]
    return entry
    
def update_table(df):
    #Will loop in a while, as long as user wants to add ingredients
    #
    again = True
    
    #Creating empty list to house all the ingredients and their respective vol and mass (from 1 cup)
    #
    ingredients = []
    
    while(again):
        
        #Taking in user values
        #
        ing = input('Add an ingredient(not case sensitive): \n')
        v = input('Add the volume in mL (for 1 cup): \n')
        m = input('Add the mass in g (for 1 cup): \n')
        
        #formatting values for my uses
        #
        ing = str.lower(ing)
        v = int(v)
        m = int(m)
        
        #Appending to list of ingredients
        #
        ingredients.append(add_ingredient(ing, v, m))
        
        #Test whther user wants to add another, with 1 or 0, will NOT handle exceptions, user must enter '0' to exit
        #
        x = input('Would you like to add another ingredient? 1 for \'yes\', and 0 for \'no\'')
        x = int(x)
        
        if x==0:
            again=False
            
        #End of while loop
        
    
    update = pd.DataFrame(ingredients)
    update.rename(dict(zip(list(update), COL_NAMES)), axis='columns', inplace=True)
    return pd.concat([df, update], ignore_index=True) 
  


#Function to have a base table when quickly building a base, can be modified if the site ever switches, or a better is found
#
def base_table():
    
#Run to generate a base table from madamgrecip.com, once run, saves as a csv called 'Base Values.csv'
#Place this file in your directory to automatically load and use as this file's base 
#One advantage of this method is we don't have to handle string conversion, when we re-read from the csv, it converts values to floats and ints. 
#
# =============================================================================
# 
# 
# #Scraping from a site which already has some densities
# #
# url = requests.get(r'https://madamngrecipe.com/convert-grams-to-ml-milliliters/') 
# 
# soup = BeautifulSoup(url.text, features='lxml')
# 
# #Find the table, and its elements 'tr'
# table_data = soup.find('figure', {'class':'wp-block-table is-style-stripes'})
# 
# elements = table_data.find_all('tr')
# 
# #create empty ingreidents list, then cycle through elements to place values in our table
# #
# ingredients = []
# for e in elements:
#     individual = e.find_all('td')
#     #print('about to begin an x in individual')
#     ingredients.append(add_ingredient(individual[0].text, individual[3].text.rstrip(' mL'), individual[2].text.rstrip(' g')))
#     
# #Make df, drop first since it's the col names but dirty, then rename
# #    
# df = pd.DataFrame(ingredients)[1:]
# df.rename(dict(zip(list(df), COL_NAMES)), axis='columns', inplace=True)
# 
# #Unique to this imported data set, for cleanliness, will str.tolower when searching though, so kinda useless...
# df['Ingredient'] = df['Ingredient'].str.capitalize()
# 
# #Makes the csv file, incase you need to newly generate it, again, if website changes, or a better is found
# #
# df.to_csv('Base Values.csv', index=False)
#  
# 
#    
# =============================================================================

    #Return whatever is scraped from the previous code
    #
    return pd.read_csv('Base Values.csv')
    
#Makes a density column of your table, will be used to calculate afterwards
#
def make_density(df):
    df['Density (g/mL)'] = df['Mass(g)']/df['Vol(mL)']
    df['Density (g/mL)'] = df['Density (g/mL)'].where(df['Density (g/mL)']>0, -1)
    
    return df

#Make a Cup -> mL column. All values from the salty marshmallow will be assumed to be in volume CUPS
#Will convert the Cups to mL in a column
#
def cup_to_ml(df):
    #df = make_density(df)
    df['mL'] = df['Cups']*CUPS_TO_ML
    
    return df


def base_table_2():
    
# =============================================================================
#     # =============================================================================
#     # Get new site, many more ingredients
#     # =============================================================================
#     site = requests.get(r'https://www.kingarthurbaking.com/learn/ingredient-weight-chart')
#     soup = BeautifulSoup(site.text, features='lxml')
#     
#     # =============================================================================
#     # Find table individualk elements
#     # =============================================================================
#     ingredients = soup.find_all('tr')
#     
#     elements = []
#     for ingredient in ingredients[1:]:
#         
#         print(ingredient.prettify())
#         #Name is simplest element to get
#         #
#         name = ingredient.find('th').text
#         
#         #Values are awkwardly contained, will have to sort through the 3 td tags of each.
#         #Discard ounce, and convert volume row to float of cup amount in mL. grams is easy
#         #
#         vol_ounce_gram = ingredient.find_all('td')
#         grams = vol_ounce_gram[2].text
#         if 'to' in grams:
#             grams = float(grams.split(' to ')[0]) * 1.05
#         else: #There is no stupid 'x to y grams' as a damn weight...
#             grams = float(grams)
#         
#         #Handling name is quite the thing...
#         #This first part, I'm taking the 0th element of vol_ounce_gram, splitting the text by ' ', and taking the 0th element, which is always the number
#         #
#         name_num = vol_ounce_gram[0].text.split(' ')[0]
#         
#         #If the number is a division, which they indicate with int/int, I will do division here, and return the float into the value
#         number=0
#         if '/' in name_num:
#             numer = int(name_num.split('/')[0])
#             denom = int(name_num.split('/')[1])
#             number = numer/denom
#         else: #It's not a fraction
#             number = int(name_num)
#             
#         met_type = vol_ounce_gram[0].text.split(' ')[1].lower()
#         
#     #Convert depending on what it is, or else return -1 to indicate that it's a 'unit'
#         if 'cup' in met_type:
#             number *= CUPS_TO_ML
#         elif 'tab' in met_type:
#             number *= CUPS_TO_ML/16
#         elif 'tea' in met_type:
#             number *= CUPS_TO_ML/48
#         else: #Not one of these, so unit
#             number = -1
#             
#         #Append the element, to then put into df
#         #
#         elements.append(add_ingredient(name, number, grams))
#         
#     new_data=pd.DataFrame(elements)
#     
#     new_data.rename(dict(zip(list(new_data), COL_NAMES)), axis='columns', inplace=True)
#     
#     df2 = base_table()
#     
#     table_2 = pd.concat([new_data, df2], ignore_index=True)
#         
#     table_2.to_csv('Table 2.0.csv', index=False)
# =============================================================================
    
    
    
    #Code is above was to generate the now saved csv
    #
    return pd.read_csv('Table 2.0.csv')
    
    
def base_table_3():
# =============================================================================
#     # =============================================================================
#     # Getting site with over 1600 'ingredients', a lot of them aren't, but wtv'
#     # =============================================================================
#     site = requests.get('https://hapman.com/news-and-knowledge/bulk-material-density-guide/')
#     soup = BeautifulSoup(site.text, features='lxml')
#     ingredients = soup.find_all('tr', {'class':'row-item'})
#     
#     #Empty list to append each item, nicely laid out for me
#     #
#     big_list = []
#     for ing in ingredients[1:]:
#         
#         #Make a 3-list of the tds of each ingredient, it gives the name, the imperial density, and metric density(this last one is extrememeely convenient)
#         #With density in g/cm**3 (cm**3 = mL) we can just assert that 1 mL is that value in grams (def. of density)
#         #
#         name_imperial_metric = ing.find_all('td')
#         name = name_imperial_metric[0].text
#         if name == 'Gum Premix': #Handling this one case because useless anyways
#             continue
#         grams = float(name_imperial_metric[2].text)
#         ml = 1
#         big_list.append(add_ingredient(name, ml, grams))
#         
#     df_3 = pd.DataFrame(big_list)
#     df_3.rename(dict(zip(list(df_3), COL_NAMES)), axis='columns', inplace=True)
#     
#     base_table_2 = pd.read_csv('Table 2.0.csv')
#     
#     df_3 = pd.concat([base_table_2, df_3])
#     
#     df_3.to_csv('Table 3.0.csv')
# =============================================================================

    return pd.read_csv('Table 3.0.csv')

































    
              
    