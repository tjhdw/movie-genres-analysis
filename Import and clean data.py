# Part 1: Import and clean data
# Import modules and configure settings
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re
import csv
import sys
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

# Prevent warning message, making report more user-friendly
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Import movies.csv data
Import movies.csv data

# Define file path and preview data
path ='/Users/iriswu/'

# Read data to movies using pandas read_csv module
movies = pd.read_csv(path + 'movies.csv',sep = '\t',encoding='latin1')

# Preview the origianl data
movies.head(2)

# Read HTML table using url address
url1 = 'https://www.filmsite.org/bestpics3.html'
df = pd.read_html(url1,index_col=None,header=None,skiprows=2)

# Transform data into pandas dataframe for later manipulation
oscar_best_movies_1 = df[0]

# Scripted data cleaning

# Delete useless columns
del oscar_best_movies_1[3]
del oscar_best_movies_1[4]
del oscar_best_movies_1[5]

# Change column names
col_name = ['Year','Best Academy Award Movie','Film Director']
oscar_best_movies_1.columns = col_name

# Clean column 'Year'
oscar_best_movies_1['Year'] = oscar_best_movies_1['Year'].str.replace('-\d*','')

# Clean column 'Best Academy Award Movie'
oscar_best_movies_1['Best Academy Award Movie'] = oscar_best_movies_1['Best Academy Award Movie'].str.replace('\(\w+\s*\w*\)\s*\w*','')
oscar_best_movies_1['Best Academy Award Movie'] = oscar_best_movies_1['Best Academy Award Movie'].str.replace('\(\w+\s*\w*\s*\w*\s*\w*\)','')

# Clean column 'Film Director'
oscar_best_movies_1['Film Director'] = oscar_best_movies_1['Film Director'].str.replace('\*','')
oscar_best_movies_1['Film Director'] = oscar_best_movies_1['Film Director'].str.replace('\(\D*\)','')

# Remove missing value
oscar_best_movies_1 = oscar_best_movies_1.dropna()
oscar_best_movies_1.head(2)

# Read HTML table using url address
url2 = 'https://www.filmsite.org/bestpics4.html'
df = pd.read_html(url2,index_col=None,header=None,skiprows=2)

# Transform into data frame
oscar_best_movies_2 = df[0]

# Delete useless columns
del oscar_best_movies_2[3]
del oscar_best_movies_2[4]
del oscar_best_movies_2[5]

# Change column names
col_name = ['Year','Best Academy Award Movie','Film Director']
oscar_best_movies_2.columns = col_name

# Clean column ['Film Director']
oscar_best_movies_2['Film Director'] = oscar_best_movies_2['Film Director'].str.replace('\*','')
oscar_best_movies_2['Film Director'] = oscar_best_movies_2['Film Director'].str.replace('and\s\w*\s\w*','')

# Concatenate two oscar dataframes
oscar_best_movies = pd.concat([oscar_best_movies_1, oscar_best_movies_2], ignore_index=True)

# Merge oscar_best_movies with movies dataframe for later usage
oscar_movies = pd.merge(oscar_best_movies, movies, left_on='Best Academy Award Movie', right_on='title')

# Delete wrong data
oscar_movies = oscar_movies.drop(oscar_movies.index[[14,15,19,69]])

# Delete useless columns
oscar_movies = oscar_movies.drop(columns=['title','Year'])

# Drop missing values
oscar_movies = oscar_movies.dropna()

# Read HTML table using url address
url3 = 'https://en.wikipedia.org/wiki/Golden_Lion#Golden_Lion_Honorary_Award'
df = pd.read_html(url3,index_col=None,header=None,skiprows=3)

# Transform into dataframe
venice_best_movies = df[1]

# Delete useless columns
del venice_best_movies[4]
del venice_best_movies[3]
del venice_best_movies[2]

# Change columns name
col_name = ['Year','Golden Lion Award Movie']
venice_best_movies.columns = col_name

# Clean columns ['Year']
venice_best_movies = venice_best_movies.drop(venice_best_movies.index[venice_best_movies[venice_best_movies['Year'].str.contains('t')].index])
venice_best_movies = venice_best_movies.dropna()

# Clean columns ['Golden Lion Award Movie'] 
index_list = list(venice_best_movies[venice_best_movies['Golden Lion Award Movie'].str.contains('No award')].index)
venice_best_movies = venice_best_movies.drop(index_list)

index_list_1 = list(venice_best_movies[venice_best_movies['Golden Lion Award Movie'].str.contains('\(tie')].index)
venice_best_movies = venice_best_movies.drop(index_list_1)

# Split rows to Year 2011
venice_best_movies = venice_best_movies.loc[:67,:]

# Merge venice_best_movies with movies dataframe
venice_movies = pd.merge(venice_best_movies, movies, left_on='Golden Lion Award Movie', right_on='title')

# Delete wrong data
venice_movies = venice_movies.drop(venice_movies.index[[0]])

# Delete useless columns
venice_movies = venice_movies.drop(columns=['title','Year'])


# Reading award data using URL
url4 = 'https://en.wikipedia.org/wiki/Golden_Bear'
berlin_best_movies = pd.read_html(url4,index_col=None,header=None,skiprows=3)[1]

# Delete useless columns
del berlin_best_movies[4]
del berlin_best_movies[3]
del berlin_best_movies[2]

# Change columns name
col_name = ['Year','Golden Bear Award Movie']
berlin_best_movies.columns = col_name

# Split rows to 2011
berlin_best_movies =  berlin_best_movies.loc[:81,:]

# Clean columns ['Year']
berlin_best_movies = berlin_best_movies.drop(berlin_best_movies.index[list(berlin_best_movies[berlin_best_movies['Year'].str.contains('\d{4}s')].index)])
berlin_best_movies = berlin_best_movies.drop(berlin_best_movies.index[list(berlin_best_movies[berlin_best_movies['Year'].str.contains('\d{4}\-')].index)])

# Set new index
new_index = pd.Series(list(range(len(berlin_best_movies))))
berlin_best_movies.set_index(new_index)

# Correct disordered data
for i in range(len(berlin_best_movies)):
    if berlin_best_movies.iloc[i,0].isdigit() == False:
        berlin_best_movies.iloc[i,1] = berlin_best_movies.iloc[i,0]
        berlin_best_movies.iloc[i,0] = berlin_best_movies.iloc[i-1,0]
        i += 1  
        
# Clean columns ['Golden Bear Award Movie']
berlin_best_movies['Golden Bear Award Movie'] = berlin_best_movies['Golden Bear Award Movie'].str.replace('\(\w*\s*\w*\s*\w*\s*\&*\s*\w*\)','')

# Merge berlin_best_movies with movies dataframe
berlin_movies = pd.merge(berlin_best_movies, movies, left_on='Golden Bear Award Movie', right_on='title')

# Delete useless columns
berlin_movies = berlin_movies.drop(columns=['title','Year'])

# Delete wrong data
berlin_movies = berlin_movies.drop(berlin_movies.index[[1]])

# Reading award data using URL
url5 = 'https://en.wikipedia.org/wiki/Palme_d%27Or'
cannes_best_movies = pd.read_html(url5,index_col=None,header=None,skiprows=3)[1]

# Delete useless columns
del cannes_best_movies[4]
del cannes_best_movies[3]
del cannes_best_movies[2]

# Change columns name
col_name = ['Year','Palme dOr Award Movie']
cannes_best_movies.columns = col_name

# Split rows to Year 2011
cannes_best_movies =  cannes_best_movies.loc[:96,:]

# Clean columns ['Year']
cannes_best_movies = cannes_best_movies.drop(cannes_best_movies.index[list(cannes_best_movies[cannes_best_movies['Year'].str.contains('–')].index)])
cannes_best_movies = cannes_best_movies.drop(cannes_best_movies.index[list(cannes_best_movies[cannes_best_movies['Year'].str.contains('\d{4}s')].index)])

cannes_best_movies['Year'] = cannes_best_movies['Year'].str.replace('1939\s\W','1939')

# Drop missing data
cannes_best_movies = cannes_best_movies.dropna()

# Correct the data
for i in range(len(cannes_best_movies)):
    if cannes_best_movies.iloc[i,0].isdigit() == False:
        cannes_best_movies.iloc[i,1] = cannes_best_movies.iloc[i,0]
        cannes_best_movies.iloc[i,0] = cannes_best_movies.iloc[i-1,0]
        i += 1  

# Clean columns ['Palme dOr Award Movie']
cannes_best_movies['Palme dOr Award Movie'] = cannes_best_movies['Palme dOr Award Movie'].str.replace('\s\§','')

# Merge cannes_best_movies with movies dataframe
cannes_movies = pd.merge(cannes_best_movies, movies, left_on='Palme dOr Award Movie', right_on='title')

# Delete useless columns
cannes_movies = cannes_movies.drop(columns=['title','Year'])

# Delete wrong data
cannes_movies = cannes_movies.drop(cannes_movies.index[[0]])