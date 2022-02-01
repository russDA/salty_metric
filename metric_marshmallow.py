#Part of an application to quickly convert Salty Marshmallow baking recipes to metric

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tkinter as tk
import ingredient_df as idf
import debug_salty_names as dsn

def get_df(url):
    
    df = dsn.into_dataframe(url)
    
    df = dsn.add_cup_vol_col(df)
    
    df = dsn.add_mass(df)
    
    df = dsn.presentable_df(df)
    print('here')
    return df

# =============================================================================
# my_canvas = canvas.Canvas('Hello.pdf')
# my_canvas.drawString(150, 750, test_df.Mass[1])
# my_canvas.save()
# print(test_df.Mass[1])
# =============================================================================

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
    title = dsn.get_name(url_entry.get())
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
    title = dsn.get_name(url_entry.get())
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





















