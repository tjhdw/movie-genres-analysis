# movie-genres-analysis

## Background
You probably know "rotten tomatoes" -- because when you and your friends argue about whether an American movie is rotten, your friends may often end up the debate with "check rotten tomatoes!".

So, what is Rotten Tomatoes?

Rotten Tomatoes is an American review-aggregation website for film and television. Rotten Tomatoes and the Tomatometer score are the world’s most trusted recommendation resources for quality entertainment. As the leading online aggregator of movie and TV show reviews from critics, Rotten Tomatoes provide fans with a comprehensive guide to what’s Fresh – and what’s Rotten – in theaters and at home. Thus, analyzing movies popularity on Rotten Tomatoes has a significant referential value for movie industry.

## Objective
We will analyze the change of movie genres in the past 100 years. Our dataset includes movies basic information and its relavant rotten tomatoses scores information. Also, we think it would be interesting to predict audience score of movies without any financial information to see what affects audience score of one movie. Thus, our goal is to provide valuable insights on what affects movie popularity and how to improve movie popularity, as well as to offer a good performing model to preidct movie audience score on Rotten Tomatoes.


## Data Context
The movie information comes from an extension of MovieLens10M database, published by GroupLeans research group as well as from website. We also import data from website to gain more information.
After data preprocessing, there are 16 variables in our data set:
* id: the unique identity of movie
* title: the title of movie
* year: the year that movie published
* rtAllCriticsNumReviews: the number of critics reviews for a movie
* rtAllCriticsScore: the critics score for a movie
* rtTopCriticsNumReviews: the number of top critics reviews for a movie
* rtTopCriticsScore: the top critics score for a movie
* rtAudienceNumRatings: the number of audience ratings for a movie
* rtAudienceScore: the audience score for a movie
* award: whether a movie is awarded or not (0 means unawarded, 1 means awarded)
* numOfActors: the number of actors for a movie
* country: the country that movie made
* numOfGenres: the number of genres for a movie
* genre: the genre(s) for a movie
* directorName: the director name of a movie
* numOfDirectorMovies: the number of movies directed by a director




