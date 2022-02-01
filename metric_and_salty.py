#Part of an application to quickly convert Salty Marshmallow baking recipes to metric

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tkinter as tk

#Relic values, don't want to sift through code to see where I used these and replace with something better.....
#
COL_NAMES = ['Ingredient', 'Vol(mL)', 'Mass(g)']

CUPS_FROM_ANY = 'Cups'

CUPS_TO_ML = 236.55
# =============================================================================
# This is a copy of the file to generate external ingredients. Pasted into this file for the purposes of reducing tkinter app build.
# =============================================================================
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

# =============================================================================
# End of the first file, the external ingredient file   
# =============================================================================

# =============================================================================
# Beginning of second file, most important functions in here
# =============================================================================

# =============================================================================
# Converts a columns strings into lower case alphabetic characters only, to compare against another df
# =============================================================================
def search_name(df, col_name):
    searchable_names = []
    for string in df[col_name]:
        string = string.lower()
        string = ''.join(filter(str.isalnum, string))
        searchable_names.append(string)
    df['searching'] = searchable_names
    return df

# =============================================================================
# Access the soup once, which will be give nto each individual function searching for name, amount, etc
# =============================================================================
def get_salty_soup(url):
    website = requests.get(url)
    soup = BeautifulSoup(website.text, features = 'lxml')
    return soup

# =============================================================================
# Go through URL, and make an np array of the amounts values
# =============================================================================
def get_amount_array(url):
    #List of the fraction values used in salty marshmallow
    #
    fractions = ['⅛', '¼', '½', '¾', '⅓', '⅔']
    decimals = [' 0.125', ' 0.25', ' 0.5', ' 0.75', ' 0.33', ' 0.67']
    frac_to_deci = dict(zip(fractions, decimals))
    
    """
    #Obtaining the names, yes yes sweary name, but I got really fed up debugging, because there were so many damn edge cases....
    #
    soup = get_salty_soup(url)
    fuckers = soup.find_all('span', {'class':'wprm-recipe-ingredient-amount'})
    """
    
    soup = get_salty_soup(url)
    fuckers = soup.find_all('li', {'class':'wprm-recipe-ingredient'})
    fucker = []
    for f in fuckers:
        fucker.append(f.find('span', {'class':'wprm-recipe-ingredient-amount'}))
    
    
    #Empty list, run through, and handle all cases, then make array at end
    #
    amounts = []
    for f in fucker:
       if f == None:
           amounts.append(-1)
           continue
       amount = f.text
       #Fractions always at the end, be they alone or string of characters
       #
       if amount[-1] in fractions:
          
           #Getting the fraction, converting to decimal preceded with ' '
           #If it's only character, the ' ' will be stripped at the end, otherwise it's there in case the numbers are scrunched
           #
           for frac, deci in frac_to_deci.items():
               x = amount[-1]
               x = x.replace(frac, deci)
               amount = amount[:-1]
               amount +=x
               amount = amount.lstrip()
       
       #If it has a space in the middle, I need to seperate and add the fraction with int
       #
       if ' ' in amount:
           summing = amount.split()
           summing = float(summing[0].strip()) + float(summing[1].strip())
           amount = str(summing)
       
       # Sometimes things like 2-3 tbsp, so get these, and take average
       #
       if '-' in amount:
           average = amount.split('-')
           if average[0] in fractions:
               x = average[0]
               for f, d in frac_to_deci.items():
                   x = x.replace(f, d)
                   x = x.strip()
                   if len(x)>1:
                       x = float(x)
                       average[0] = x 
                       break
                    
           if average[1] in fractions:
               x = average[1]
               for f, d in frac_to_deci.items():
                   x = x.replace(f, d)
                   x = x.strip()
                   if len(x)>1:
                       x = float(x)
                       average[1] = x
                       break
                     
           average = (float(average[0]) + float(average[1]))/2
           amount=str(average)
           
       #After checking most edge cases, add to list
       #
       amounts.append(amount)
    
    #Return as an np array
    #
    return np.array(amounts).astype(float)

# =============================================================================
# Go through URL, find the name of each and append, will have to handle things such as quantities integrrated in name
# =============================================================================
def into_dataframe(url):
    soup = get_salty_soup(url)
    fuckers = soup.find_all('li', {'class':'wprm-recipe-ingredient'})
    
    amounts = get_amount_array(url) #Need live, since sometimes I must make modifications based on name (e.g. name describes a multiplic.)
    
# =============================================================================
# Empty arrays, will add concurrently, since these two variables are often entangled
# =============================================================================
    units = []
    names = []
    ingredient_no = 0 #Sometimes, name affects the qty in amount, so I will keep index, and modify amounts if need be
    
    for f in fuckers: #Iterating per ingredient, and adding to both arrays at once
        
        unit = f.find('span', {'class':'wprm-recipe-ingredient-unit'}) #Won't call .text method, because sometimes this is None
        name = f.find('span', {'class':'wprm-recipe-ingredient-name'}).text
        name = name.lower()
        print(f'The name is {name}')
# =============================================================================
# first thing to handle will be if the name describes a modification to the amount, this could be addition: '& ½',
# =============================================================================
        
        
        if '& ' in name[:3].lower(): #Handling any addition of this type in the name. Quite preposterous that this happens...
            name = name.split('& ')[-1].lower() # Breaking name live, and keeping only what comes next, with first char the fraction
            
            #Conversion tools
            fractions = ['⅛', '¼', '½', '¾', '⅓', '⅔']
            decimals = ['0.125', '0.25', '0.5', '0.75', '0.33', '0.67']
            frac_to_deci = dict(zip(fractions, decimals))
            
            #Assuming the fraction will come as a single-char-fraction, and the ' ' seperates the & and the fraction
            for f, d in frac_to_deci.items():
                
# =============================================================================
# Process: get the 0th char from name(fraction). Replace to decimal, convert to float after stripping whitespace. Then add to unit[ingredient_no] amount                
# =============================================================================
                x = name[0]
                x = x.strip()
                x = x.replace(f, d)
                if len(x)>1:
                    break
            x = float(x.strip())
            amounts[ingredient_no] +=x
        
        if unit == None: #Things like bananas in b.bread is simply amount:3, unit:None, name:Large bananas
            unit = 'Unit(s)'
            
            #There's a case where the unit is put in the name... a pesky edge-case, will try to handle all possibilities
            #If this is the name, will change name to no longer include the unit and what comes before
            #
            if 'cup' in name.lower(): 
                unit = 'Cup'
                name = name.lower().split('cup')[-1][1:]
            if 'spoon' in name.lower() and 'table' in name.lower():
                unit = 'Tablespoon'
                name = name.lower().split('spoon')[-1][1:]
            if 'spoon' in name.lower() and 'tea' in name.lower():
                unit = 'Teaspoon'
                name = name.lower().split('spoon')[-1][1:]
        else: #Unit is not None, so it's properly entered in table
            unit = unit.text
            
            if 'stick' in unit.lower(): #This SHOULD only be an issue for stick, will only handle that, too many edgecases otherwise
                print('here')
                amounts[ingredient_no] *= 0.5
                unit = 'Cup'
        
        #Handled all cases, now append...
        units.append(unit)
        names.append(name)
        
        #End of loop, increment for next ingredient amount, most cases should have been handled
        #
        print(ingredient_no)
        ingredient_no+=1
    
    return pd.DataFrame({'Amount':amounts, 'Unit':units, 'Names':names})
        
# =============================================================================
# Take a dataframe and add the metric columns, and return the new dataframe, should be used on a into_dataframe df
# =============================================================================
def add_cup_vol_col(df):
    # =============================================================================
    # Make a column which only accepts values if Unit column isn't unit(s)
    # =============================================================================
    conditions = [
        df['Unit'] == 'Unit(s)',
        df['Unit'] == 'Large',
        df['Unit'].str.startswith('Pound'),
        df['Unit'].str.startswith('pound'),
        df['Unit'].str.startswith('Ounc'),
        df['Unit'].str.startswith('ounc'),
        df['Unit'].str.startswith('Cup'),
        df['Unit'].str.startswith('cup'),
        df['Unit'].str.startswith('tea'),
        df['Unit'].str.startswith('Tea'),
        df['Unit'].str.startswith('tab'),
        df['Unit'].str.startswith('Tab'),
        df['Unit'].str.startswith('tsp'),
        df['Unit'].str.startswith('Tsp'),
        df['Unit'].str.startswith('tbs'),
        df['Unit'].str.startswith('Tbs'),
        ]

    choices = [
        df['Amount']*(-1),
        df['Amount']*(-1),
        df['Amount']*2,
        df['Amount']*2,
        df['Amount']/8,
        df['Amount']/8,
        df['Amount'],
        df['Amount'],
        df['Amount']/48,
        df['Amount']/48,
        df['Amount']/16,
        df['Amount']/16,
        df['Amount']/48,
        df['Amount']/48,
        df['Amount']/16,
        df['Amount']/16,
        ]

    df['Cups'] = (np.select(conditions, choices, default=None)).astype(float)
    df['Vol(mL)'] = (df['Cups']*236.55).where(df['Cups']>=0, -1)
    return df
    
# =============================================================================
# Makes mass col from vol col, using ingredient df comparison. should only be used with add_cup_vol_col
# =============================================================================
def add_mass(df):
    
    #start by importing the most updated base table from idf
    #
    base_table = base_table_3()
    base_table = make_density(base_table)
    
    base_table = search_name(base_table, 'Ingredient')
    df = search_name(df, 'Names')
    
    # =============================================================================
    # Looping through entire databse to find the right ingredient. 
    # Technically an m*n complexity, but m(recipe legnth) is always really small. 
    # And many of the most popular, common ingredients are at beginning of n (sugar, butter, etc), and relatively small anyways...
    # =============================================================================

    # =============================================================================
    # Using indexing to multiply when found, could have used for the names too, but the iterable name makes it more readable
    # =============================================================================
    recipe_index = 0
    recipe_grams = []

    for recipe_ingredient in df['searching']:
        found = False
        table_index=0
        for table_ingredient in base_table['searching']:
            if recipe_ingredient == table_ingredient:
                vol = df['Vol(mL)'][recipe_index]
                den = base_table['Density (g/mL)'][table_index]
                recipe_g = vol*den
                recipe_grams.append(recipe_g)
                recipe_index+=1
                found=True
                break
            else: #Not the same, increment table
                table_index +=1
            
        #If you never found, append -1
        if(not found):
            recipe_grams.append(-1)
            recipe_index+=1
        
    # =============================================================================
    #     Will hyandle a couple of generic cases where the value is -1
    #     Will keep value as negative value of rough estimate
    #     When making the deliverable, if the value is negative, and magnitude(value) > 1, will display the absolute value, and append roughly
    #     
    #     Going to handle oil, sugar, water, cream/milk, powder, and ground. These are estimates I'm taking, based on averages
    # =============================================================================
        
    # =============================================================================
    # Value appended must be -1, and also, the modulo of cups can't be zero. 
    # If it is, it's because it was 'unit' or 'large', and I don't want to target these
    # =============================================================================
        if (recipe_grams[-1] == -1 and df['Vol(mL)'][recipe_index-1]%1 !=0):
           
            if 'sugar' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.83
            if 'cream' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1
            if 'flour' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*50
            if 'oil' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.92
            if 'water' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1
            if 'milk' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.03
            if 'powder' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.1
            if 'nut' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.5
            if 'ground' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.55
            if 'oat' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.38
            if 'butter' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.043 
            if 'spice' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.43
            if 'zest' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.45
            if 'juice' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.25
            if 'liqueur' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.04
            if 'vodka' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.79
            if 'cand' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.77
            if 'almond' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*0.5
            if 'cider' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.048
            if 'syrup' in recipe_ingredient:
                recipe_grams[-1] *= df['Vol(mL)'][recipe_index-1]*1.15

    df['Mass(g)'] = np.array(recipe_grams).round(2)
    
    return df

# =============================================================================
# Making a pretty df that has the strings of all I want and need for something like tkinter
# =============================================================================
def presentable_df(df):
    
    #Capitalize first letter of name, readibality
    #
    df['Names'] = df['Names'].str.capitalize()
    
    #Conditions for string formatting
    #
    conditions = [
        df['Mass(g)'] == (-1),
        df['Mass(g)'] < (-1),
        df['Mass(g)'] > (-1)
        ]
    results = [
        df['Amount'].abs().astype(str) + ' unit(s) of: ' + df.Names,
        (df['Mass(g)']*(-1)).abs().astype(str) + ' grams(roughly) of: ' + df.Names,
        df['Mass(g)'].abs().astype(str) + ' grams of: ' + df.Names
        ]
    
    #Making the strings from the individuals pieces
    #
    df['Mass'] = np.select(conditions, results, default=None)
    df['Vol'] = (df['Vol(mL)'].abs().round(2).astype(str) + ' mL of: ' + df.Names).where(df['Vol(mL)'].abs()%1 !=0, df['Amount'].astype(str) + ' unit(s) of: ' + df.Names)
    df['Imperial'] = df.Amount.abs().astype(str) + ' ' + df.Unit + ' of: ' + df.Names

    df_pretty = df[['Mass', 'Vol', 'Imperial']]
    return df_pretty

# =============================================================================
# Finding title and subnames of title
# =============================================================================
def get_name(url):
    website = requests.get(url)
    soup = BeautifulSoup(website.text, features = 'lxml')
    title = soup.find('h1', {'class':'entry-title'}).text
    return title
        

# =============================================================================
# End of the file which held most of the important functions in terms of generating and handling the datadrames
# =============================================================================

# =============================================================================
# Main file used to generate the tkinter
# =============================================================================
"""
    
    This is the building of the tkinter app
    
"""
# =============================================================================
# Basically calling all the important functions from the second file
# =============================================================================
def get_df(url):
    df = into_dataframe(url)
    
    df = add_cup_vol_col(df)
    
    df = add_mass(df)
    
    df = presentable_df(df)
    
    return df

#Setup and welcome message
#
root = tk.Tk()
root.title('Metric Marshmallow')
root.geometry('790x400')


welcome_msg = tk.Label(root, text='Welcome! I\'m an application which will convert Imperial recipes to Metric(mL and g)\n' + 
                        '\nI scraped websites for densities. This is not rigorous science. It is, however, an indictement on imperial measures. \n\n', font=16)
welcome_msg.grid(row = 1, column = 1)

#Getting the URL
url_label = tk.Label(root, text='Enter the URL of the recipe you wish to have converted:')
url_label.grid(row = 2, column = 1)
url_entry = tk.Entry()
url_entry.grid(row = 3, column = 1)
space_label = tk.Label(root, text=' ')
space_label.grid(row = 4, column = 1)

def get_vol():
    
    df = get_df(url_entry.get())
    title = get_name(url_entry.get())
    #Setup canvas, set top, which will leave space for title
    #
    vol_canvas = canvas.Canvas('Volume Recipe.pdf', pagesize=letter)
    top_of_canvas = 700
    
    # =============================================================================
    #     appending each ing in vol, then in imperial
    # =============================================================================
    vol_canvas.drawString(100, 730, title)
    vol_canvas.drawString(180, 715, 'Here are the ingredients in Metric Volume(mL)')
    top_of_canvas-=30
    for ing in df.Vol:
        vol_canvas.drawString(100, top_of_canvas, ing)
        top_of_canvas-=15
    
    top_of_canvas -=15
    vol_canvas.drawString(150, top_of_canvas, 'Here are the ingredients in Imperial')
    top_of_canvas-=30
    for ing in df.Imperial:
        vol_canvas.drawString(100, top_of_canvas, ing)
        top_of_canvas-=15
        
    
        
    vol_canvas.save()
    
vol_button = tk.Button(root, text='Make PDF of Volume', command=get_vol)
vol_button.grid(row = 5, column = 1)

def get_mass():
    
    df = get_df(url_entry.get())
    title = get_name(url_entry.get())
    #Setup canvas, set top, which will leave space for title
    #
    mass_canvas = canvas.Canvas('Mass Recipe.pdf', pagesize=letter)
    top_of_canvas = 700
    
    # =============================================================================
    #     appending each ing in mass, then in imperial
    # =============================================================================
    mass_canvas.drawString(100, 730, title)
    mass_canvas.drawString(180, 715, 'Here are the ingredients in Metric Mass(g)')
    top_of_canvas-=30
    for ing in df.Mass:
        mass_canvas.drawString(100, top_of_canvas, ing)
        top_of_canvas-=15
    
    top_of_canvas -=15
    mass_canvas.drawString(150, top_of_canvas, 'Here are the ingredients in Imperial')
    top_of_canvas-=30
    for ing in df.Imperial:
        mass_canvas.drawString(100, top_of_canvas, ing)
        top_of_canvas-=15
     
    mass_canvas.save()

mass_button = tk.Button(root, text='Make PDF of Mass', command=get_mass)
mass_button.grid(row = 6, column = 1)

# =============================================================================
# Notes and comments and legal and that jazz
# =============================================================================
notes_label = tk.Label(root, text='\n*IMPORTANT*\n\n'+
                       'Keep in mind that these calculations are derived from values found on the internet.\n' +
                       'I found densities on a few websites, and aggregated a table to compare Salty Marshmallow\'s ingredients.\n' +
                       'The imperial measure is on both copies for reference.\n'+
                       'Not every page on Salty Marshmallow is filled out the same, and so the scraper doesn\'t handle all possible cases.\n'+
                       'The .pdf files will appear in the same location where you\'ve saved the app, or run the code.')
notes_label.grid(row = 7, column = 1)

legal_label = tk.Label(root, text='\n*ALSO IMPORTANT*\n'+
                       'I love Salty Marshmallow and all her recipes, but I\'m not good with imperial.... I\'m a poutine-loving canadian who cooks in mL and grams...\n'+
                       'This application is *purely* and *only* a tool to quickly convert a recipe into metric units. All credit and love goes to Nichole & Salty Marshmallow :)')
legal_label.grid(row = 8, column = 1)

root.mainloop()

# =============================================================================
# END OF TKINTER BUILD AND EVERYTHING FOR THIS FILE TO BE MADE INTO AN APP WITH PYINSTALLER
# =============================================================================
