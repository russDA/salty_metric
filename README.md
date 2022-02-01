An application or script which will convert Salty Marshmallow recipes into Metric (g, mL).

This repo will have the three seperate scripts to make this application: 
1-Retrieve and produce ingredient-density dataset. 
2-Functions to manipulate and convert the data scraped on the site.
3-Building the tkinter application

It will also have a copy of the application, and the CSV file which was generated with part 1, which should be saved in the same location from where the script/app is run.
Two PDFs are provided, which are examples of what the app produces when executed properly. They should automatically save to the location where the app or script is run. 

Lastly, I've included a script which concatenates the threee scripts into one, and which should be used when building the .exe file using pyinstaller. Doing otherwise forces the app to include seperate instances of Pandas, Numpy etc. which are all heavy packages. Unfortunately I was able to compile the 3-part files into an .exe, but am having problems with the 'single file'.
Will need to address this, as it *should* reduce the size of the application by about 66%.

There is definitely a way to do this without using pandas, or perhaps by only importing select few pandas methods. This would drastically reduce the size of the application, but would require extensive re-coding. In the meantime, this is a slightly large file, which runs quite fast.
The other issue is that of comparing ingredients to a dataset which has other ingredients with their values. This is likely not the best way, but it was the quickest way I could think of.

Salty Marshmallow has an edgecase on practically every page. I've done my best to handle most, but some will still come through. This is why each .pdf includes the original imperial version, incase a string seems off. 
This was designed with desserts in mind. As they say, cooking is improv, but baking is science. With this in mind, the script might work with other recipes, but it was only designed and tested using desserts. I already don't guarantee precision for baked goods, but even much less for anything else. Caveat Emptor.

I've made this app only generate the units converted. To be crystal clear, my only intention and purpose with this application is to quickly convert the recipes into metric units.

The .pdfs provided are those I generated using this particular recipe:
https://thesaltymarshmallow.com/best-banana-bread-recipe/

Enjoy :)
