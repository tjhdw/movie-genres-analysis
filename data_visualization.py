# Set the style, axes and figure of our plot
sns.set_style('white')
fig, axes = plt.subplots(1, 3)
# Set figure size
fig.set_size_inches(22, 8)
# Set font size
sns.set(font_scale=3)

# Plot distribution of 'rtAudienceScore', 'rtTopCriticsScore', 'rtAllCriticsScore' using histgram
m1 = sns.distplot(new_movies.rtAudienceScore,15,ax=axes[0],color='gold')
m2 = sns.distplot(new_movies.rtTopCriticsScore,15,ax=axes[1],color='lightseagreen')
m3 = sns.distplot(new_movies.rtAllCriticsScore,15,ax=axes[2],color='sandybrown')

plt.tight_layout()


# Visualize the statistical value comparasion of 'rtAudienceScore',
#'rtAllCriticsScore','rtTopCriticsScore'

# Set style and figure size
sns.set_style('white')
plt.figure(figsize = (12, 6))
# Plot boxplot for three score
new_movies.boxplot(column=['rtAudienceScore','rtAllCriticsScore',
                           'rtTopCriticsScore'],showmeans=True, 
                   flierprops={'marker': '*'}, vert=False, grid=False)
# Set label of x axes and yaxes
plt.xlabel('Score')
plt.ylabel('Type of Score')
plt.title('Boxplot of Score of Audience, Top Critics And All Critics');


# Group the new_movies data by award, show number mean and max of three scores
award_table = pd.DataFrame(new_movies.groupby(by='award').agg({'rtAudienceScore':['count','mean','max'],'rtAllCriticsScore':['mean','max'],'rtTopCriticsScore':['mean','max']}))

# Sort valye by audience score and then count
award_table.sort_values(by=[('rtAudienceScore','count')], ascending = False)

# Subplot distribution of audience score of awarded movies 
# and unawarded movies
sns.set_style('white')
fig = plt.figure(figsize = (12, 6))
title = fig.suptitle("Audience Score of award and unaward movies", fontsize=14)
fig.subplots_adjust(top=0.85, wspace=0.3)

# Subplot for awarded movies
ax1 = fig.add_subplot(1,2, 1)
ax1.set_title("awarded movies")
ax1.set_xlabel("audience score")
ax1.set_ylabel("density") 
sns.kdeplot(new_movies[new_movies['award']==1]['rtAudienceScore'], ax=ax1, shade=True, color='r')

# Subplot for unawarded movies
ax2 = fig.add_subplot(1,2, 2)
ax2.set_title("unawarded movies")
ax2.set_xlabel("audience score")
ax2.set_ylabel("density") 
sns.kdeplot(new_movies[new_movies['award']==0]['rtAudienceScore'], ax=ax2, shade=True, color='y')
plt.show()


# Set bins
bins=[1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]
h = genres.join(movies[['year','rtAudienceScore']])
h['cut'] = pd.cut(h['year'],bins)
sns.set_style('white')
a=h[['cut','rtAudienceScore']].groupby('cut').mean()

# Plot
f, ax= plt.subplots(figsize = (14, 8))
a.plot(grid=False,marker='o',color='#fee8c8',markersize=12,linewidth=4,legend=False,markerfacecolor='#ff796c',ax=ax)
plt.xticks(range(0,11),['1910s','1920s','1930s','1940s','1950s','1960s','1970s','1980s','1990s','2000s']);
plt.ylim=(0,100);
plt.xlabel('Year')
plt.ylabel('Audience Score')
plt.title('Mean Audience Score Over Decades');

# Read genres dataset for further analysis
genres = pd.read_table(path + 'movie_genres.csv',encoding ='ISO-8859-1',header = 0, index_col=0 )

# Join year and audience score into genres table
h = genres.join(movies[['year','rtAudienceScore']])

# Create bins using 10 years
bins=[1910,1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]
h['cut'] = pd.cut(h['year'],bins)

# Group by genre and year to create table contain the apperance of each genre in each year
b=h[['genre','year']].groupby(['genre','year']).count().reset_index().sort_values(by='year')

# Set figure size
plt.figure(figsize=(13,8))

# Plot the scatter plot
sns.scatterplot(x='year', y='genre', data=b, marker='s', hue = 'genre',legend=False, s = 80);

# Set vertical timeline
plt.axvline(1920, color='0.8');

# Set title of this plot
plt.title('The Development Of Genres');

# Create a new dataframe called genres_unique to store all the unique geners in our dataset
genres_unique = pd.DataFrame(new_movies.genre.str.split('|').tolist()).stack().unique()
genres_unique = pd.DataFrame(genres_unique, columns=['genre'])

# Set style, figure of our plot
sns.set_style('white')
plt.figure(figsize=(14,8))

# Create a dataframe to store the accumulative number of movie of each genres in each year
dftmp = new_movies.reset_index()[['id', 'year']].groupby('year')
df = pd.DataFrame({'All_movies' : dftmp.id.nunique().cumsum()})
# Use for loop to iterator each genre in our dataset and count their numbers
for genre in genres_unique.genre:
    dftmp =new_movies[new_movies['genre'].str.find(genre)!=-1].reset_index()[['id', 'year']].groupby('year')
    df[genre]=dftmp.id.nunique().cumsum()
df.fillna(method='ffill', inplace=True)

# Plot histogram for each individual genre
df.loc[:,df.columns!='All_movies'].plot.area(stacked=True, figsize=(15,9), 
                                 color = ['#e6194b', '#3cb44b', '#ffe119',
                                '#4363d8', '#f58231', '#911eb4', 
                                '#46f0f0', '#f032e6', '#bcf60c', 
                                '#fabebe', '#008080', '#e6beff', 
                                '#9a6324', '#fffac8', '#800000', 
                                '#aaffc3', '#808000', '#ffd8b1', 
                                '#000075', '#808080', '#ffffff', 
                                '#000000'])

# Plot histogram for all_movies accumulative number
plt.plot(df['All_movies'], marker='o', markerfacecolor='black')
# Set labels of x axes and y axes
plt.xlabel('Year')
plt.ylabel('Cumulative number of movies in genres')
# Set title of our plot
plt.title('Total Number Of Movie In Each Genre') 
# Set legend of our plot
plt.legend(loc=(1.02,0), ncol=1)
plt.axvline(1980, color='0.8')
plt.show();

# Plot the number of movies of Sci-Fi and Western movies
sns.set_style('white')
g=df[['Sci-Fi','Western']].plot(figsize=(12,8),linewidth=4)
plt.ylabel('Number of Movie')
plt.title('Number of Western Movies and Sci-Fi Movies')
plt.axvline(1980, color='0.8')
plt.show()

# Set figure of plot
plt.figure(figsize=(20,14))

# Plot top 10 genres of each 10 year
sns.barplot(x='cut', y='rtAudienceScore', hue='genre', palette='Paired', 
            hue_order=['Drama','Comedy','Thriller','Romance','Action',
                       'Crime','Adventure','Horror','Sci-Fi','Fantasy'],
            ci=None, data=h);

# Set limitation of Y axes
plt.ylim=(0,100)
plt.grid(b=True, axis='y', which='both', alpha=0.5);

# Set title label legend and xtickers
plt.title('Audience Score of Different Genres')
plt.xlabel('Year')
plt.ylabel('Audience Score')
plt.xticks(range(0,11),['1910s','1920s','1930s','1940s','1950s','1960s','1970s','1980s','1990s','2000s'])
plt.legend(title= 'Genres',loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.);


# Create subset of our data set to select country data
country_bin=new_movies[['country','year']]
country_bin['cut']=pd.cut(country_bin['year'],bins)
df1=country_bin.groupby(by=['cut','country']).count().reset_index()
USA = df1[df1['country']=='USA']
UK = df1[df1['country']=='UK']
France = df1[df1['country']=='France']
Canada = df1[df1['country']=='Canada']
Italy = df1[df1['country']=='Italy']
Japan = df1[df1['country']=='Japan']

# Set the style, axes and figure of our plot
sns.set_style('white')
fig, axes = plt.subplots(2, 3)
# Set figure size
fig.set_size_inches(12, 8)
# Set font size
sns.set(font_scale=1.5)

# Plot distribution of 'rtAudienceScore', 'rtTopCriticsScore', 'rtAllCriticsScore' using histgram
d1 = sns.barplot(x='cut',y='year',ax=axes[0,0],color='#46f0f0',data=USA)
d1.title.set_text('USA')
d1.set_xticks([])
d1.set_xlabel('year')
d1.set_ylabel('number of movies')

d2 = sns.barplot(x='cut',y='year',ax=axes[0,1],color='#008080',data=UK)
d2.title.set_text('UK')
d2.set_xticks([])
d2.set_xlabel('year')
d2.set_ylabel('number of movies')

d3 = sns.barplot(x='cut',y='year',ax=axes[0,2],color='#808000',data=France)
d3.title.set_text('France')
d3.set_xticks([])
d3.set_xlabel('year')
d3.set_ylabel('number of movies')

d4 = sns.barplot(x='cut',y='year',ax=axes[1,0],color='#aaffc3',data=Canada)
d4.title.set_text('Canada')
d4.set_xticks([])
d4.set_xlabel('year')
d4.set_ylabel('number of movies')

d5 = sns.barplot(x='cut',y='year',ax=axes[1,1],color='#f58231',data=Italy)
d5.title.set_text('Italy')
d5.set_xticks([])
d5.set_xlabel('year')
d5.set_ylabel('number of movies')

d6 = sns.barplot(x='cut',y='year',ax=axes[1,2],color='#3cb44b',data=Japan)
d6.title.set_text('Japan')
d6.set_xticks([])
d6.set_xlabel('year')
d6.set_ylabel('number of movies')


plt.tight_layout()