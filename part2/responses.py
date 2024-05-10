import pandas as pd
from random import choice, sample, shuffle, randint

# load and clean the dataset
df = pd.read_csv('top-500-movies.csv', dtype={'Title': str})
df = df.dropna()
df['year'] = df['year'].astype(int)

def guess_rank():
    movies = sample(df.index.tolist(), 1)
    movie = df.iloc[movies[0]]
    prompt = f"Guess the rank of {movie['title']} if its worldwide gross was {movie['worldwide_gross']} (1-500)"
    correct_answer = movie['rank']
    return prompt, correct_answer

def compare_wordlwide_gross():
    movies = movies = sample(df.index.tolist(), 2)
    movie1, movie2 = df.iloc[movies[0]], df.iloc[movies[1]]
    prompt = f"Which movie had the higher worldwide gross? {movie1['title']} or {movie2['title']}?"
    if movie1['worldwide_gross'] > movie2['worldwide_gross']:
        correct_answer = movie1['title']
    else:
        correct_answer = movie2['title']
    return prompt, correct_answer

def guess_movie_age():
    movies = sample(df.index.tolist(), 1)
    movie = df.iloc[movies[0]]
    prompt = f"Guess the age of {movie['title']}"
    correct_age = 2024 - movie['year']
    return prompt, str(correct_age)

def get_response(user_input: str, user_response=None):
    if user_input == '!guessrank':
        prompt, correct_answer = guess_rank()
        return prompt, correct_answer # Since there's no need for an answer tuple
    elif user_input == '!age':
        prompt, correct_answer = guess_movie_age()
        return prompt, correct_answer
    elif user_input == '!comparegross':
        prompt, correct_answer = compare_wordlwide_gross()
        return prompt, correct_answer
    elif user_input == '!help':
        return " Welcome to TriviaBot! Your ultimate game to explore and compare movies!\n \
        There are three commands you can choose from:\n \
        !calc - Calculate the average production cost of movies with a specific name\n \
        !age - Guess the age of the given movie\n \
        !comparegross - Guess which movie has a higher worldwide gross\n \
        ", None
    elif user_input[0] == '!':
        return "Unknown command. Try !help for a list of commands.", None
    return