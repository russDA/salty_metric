#Part of an application to quickly convert Salty Marshmallow baking recipes to metric

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


import ingredient_df as idf

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
    base_table = idf.base_table_3()
    base_table = idf.make_density(base_table)
    
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
        


get_name('https://thesaltymarshmallow.com/caramel-apple-crisp/')


