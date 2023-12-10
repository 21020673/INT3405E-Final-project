import pandas
import numpy as np
import matplotlib.pyplot as plt
# Read in the dataset, and do a little preprocessing,
# mostly to set the column datatypes.
users = pandas.read_csv('./users.dat', sep='::',
                        engine='python',
                        names=['userid', 'gender', 'age', 'occupation', 'zip']).set_index('userid')
ratings = pandas.read_csv('./ratings.dat', engine='python',
                          sep='::', names=['userid', 'movieid', 'rating', 'timestamp'])
movies_train = pandas.read_csv('./movies_train.dat', engine='python',
                         sep='::', names=['movieid', 'title', 'genre'], encoding='latin-1', index_col=False).set_index('movieid')
movies_test = pandas.read_csv('./movies_test.dat', engine='python',
                         sep='::', names=['movieid', 'title', 'genre'], encoding='latin-1', index_col=False).set_index('movieid')                         
movies_train['genre'] = movies_train.genre.str.split('|')
movies_test['genre'] = movies_test.genre.str.split('|')

# Convert the columns to the appropriate type.
users.age = users.age.astype('category')
users.gender = users.gender.astype('category')
users.occupation = users.occupation.astype('category')
ratings.movieid = ratings.movieid.astype('category')
ratings.userid = ratings.userid.astype('category')

movies_train.head()

# Count the occurrences of each genre
genre_counts = dict()
for movie_genres in movies_train.genre:
    for genre in movie_genres:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

# Create a bar plot of the genre counts
plt.figure(figsize=(10,5))
plt.bar(range(len(genre_counts)), genre_counts.values(), align='center')
plt.xticks(range(len(genre_counts)), list(genre_counts.keys()))
plt.ylabel('Number of Movies')
plt.xlabel('Genre')
plt.show()

classes = ["Crime", "Thriller", "Fantasy", "Horror", "Sci-Fi", "Comedy", "Documentary", "Adventure", "Film-Noir", 
           "Animation", "Romance", "Drama", "Western", "Musical", "Action", "Mystery", "War", "Children's"]

# merge movies_train and ratings
movies_train_ratings = movies_train.merge(ratings, on='movieid')[["movieid", "userid", "timestamp"]]
print(movies_train_ratings.value_counts("movieid"))
