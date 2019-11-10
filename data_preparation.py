# Create two Series df1 and df2
df1 = pd.Series(movies['id'],index=range(len(movies['id'])))
df2 = pd.Series(np.zeros(len(movies['id'])),index=range(len(movies['id'])))

# Concatenate two Series
movies_sub = pd.concat([df1, df2], axis=1)
movies_sub = pd.DataFrame(movies_sub)

# Create an id list that contains all ids of awarded movies 
idlist = []
idlist.extend(oscar_movies['id'])
idlist.extend(cannes_movies['id'])
idlist.extend(venice_movies['id'])
idlist.extend(berlin_movies['id'])

# Function to get unique values from a list
def unique(list1): 
    # intilize a null list 
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

unique_idlist = unique(idlist)

# Assign 1 to column [0] if that movie won award
for i in range(len(movies['id'])):
    if movies_sub['id'][i] in unique_idlist:
        movies_sub.iloc[i,1] = 1


# Merge two data frames
new_movies = pd.merge(movies, movies_sub, left_on='id', right_on='id')

# Change column name [0] to ['award']
new_movies=new_movies.rename(columns = {0:'award'})

# Import movie_actors.csv
actors = pd.read_csv(path + 'movie_actors.csv',sep = '\t',encoding='latin1')

# Count the number of actors for each movieId
num_of_actors = actors.groupby(by='movieID',sort = False).size()
num_of_actors = pd.DataFrame(num_of_actors)
num_of_actors

# Create two Series df1 and df2
df3 = pd.Series(movies['id'],index=range(len(movies['id'])))
df4 = pd.Series(np.zeros(len(movies['id'])),index=range(len(movies['id'])))

# Concatenate two Series
movies_sub_2 = pd.concat([df3, df4], axis=1)
movies_sub_2 = pd.DataFrame(movies_sub_2)

# Assign number of actor to column [0]
for i in range(len(new_movies)):
    if num_of_actors.index[i] in new_movies['id']:
        movies_sub_2.iloc[i,1] = num_of_actors.iloc[i,0]
        i += 1
        
movies_sub_2

# Merge two data frames
new_movies = pd.merge(new_movies, movies_sub_2, left_on='id', right_on='id')

# Change column name [0] to 'numbOfActors'
new_movies=new_movies.rename(columns = {0:'numOfActors'})

# Import movie_countries.csv
countries = pd.read_csv(path + 'movie_countries.csv',sep = '\t',encoding='latin1')

# Change column 'movieID' type
countries['movieID']=countries['movieID'].astype(object)

# Merge new_movies and countries data frame
new_movies = pd.merge(new_movies, countries, left_on='id', right_on='movieID')
new_movies

# Delete column 'movieID' because it is the same with column 'id'
del new_movies['movieID']

# Load genres of movie
genres = pd.read_table(path + 'movie_genres.csv',encoding ='ISO-8859-1',header = 0, index_col=0 )

# Change column 'movieID' type
new_movies['id']=new_movies['id'].astype(int)

# Calculate the number of genre of each movies
gnum = genres.groupby(by = 'movieID').count()
new_movies=new_movies.merge(gnum,left_on='id',right_on='movieID',left_index=False)
# Change the new of column genre to numberOfGenres
new_movies=new_movies.rename(columns = {'genre':'numOfGenres'})

# Group genre to to every movieID using '|' as seperator and change column name
genres = genres.groupby('movieID')['genre'].apply('|'.join).reset_index()
genres = genres.rename(index=str, columns={"movieID": "id"})

# Merge genres to new_movies
new_movies = pd.merge(new_movies, genres, on='id')

# change column 'movieID' type
new_movies['id']=new_movies['id'].astype(object)

# Import movie_directors.csv
directors = pd.read_table(path + 'movie_directors.csv', encoding ='ISO-8859-1',header = 0, index_col=1 )

# Count the number of movies directed by each director
num_movie=directors['movieID'].groupby(by='directorID').count()

#Calculate the number of movie each director have
directors['numOfDirectorMovies']=num_movie

# Change column 'movieID' type
new_movies['id']=new_movies['id'].astype(int)

# Merge director into new_movies
new_movies = new_movies.merge(directors, left_on='id',right_on='movieID')

# Change column 'movieID' type
new_movies['id']=new_movies['id'].astype(object)

# Delete column 'movieID' because it is the same with column 'id'
del new_movies['movieID']

# Set 'id' as index 
new_movies = new_movies.set_index('id')
# Print first 5 rows in new_movies 
new_movies.head(3)