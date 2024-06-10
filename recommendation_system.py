import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import urllib.parse
from fuzzywuzzy import process

# Carregar os dados
notas = pd.read_csv('Notas.csv', sep=';')
filmes = pd.read_csv('Filmes.csv', sep=',')

# Preprocessar os dados para o formato necessário pelo Surprise
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(notas[['userId', 'movieId', 'rating']], reader)

# Dividir os dados em conjunto de treino e teste
trainset, testset = train_test_split(data, test_size=0.2)

# Treinar o modelo SVD
algo = SVD()
algo.fit(trainset)

# Avaliar o modelo
predictions = algo.test(testset)
print(f"RMSE: {accuracy.rmse(predictions)}")

def get_collaborative_recommendations(user_id, n_recommendations=5):
    # Obter todos os IDs de filmes
    movie_ids = notas['movieId'].unique()
    
    # Obter filmes que o usuário ainda não avaliou
    watched_movie_ids = notas[notas['userId'] == user_id]['movieId'].unique()
    movies_to_predict = [mid for mid in movie_ids if mid not in watched_movie_ids]
    
    # Prever avaliações para filmes não assistidos
    predictions = [algo.predict(user_id, mid) for mid in movies_to_predict]
    
    # Ordenar as previsões por nota prevista
    predictions.sort(key=lambda x: x.est, reverse=True)
    
    # Obter os top N filmes recomendados
    top_predictions = predictions[:n_recommendations]
    
    # Converter IDs para títulos dos filmes
    top_movie_ids = [pred.iid for pred in top_predictions]
    top_movies = filmes[filmes['movieId'].isin(top_movie_ids)]['title'].values
    
    # Criar links para as páginas do Google dos filmes recomendados
    google_links = []
    for movie in top_movies:
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(movie)}"
        google_links.append(google_search_url)
    
    # Retorna uma lista de tuplas contendo o filme e seu link para o Google
    recommendations_with_links = list(zip(top_movies, google_links))
    return recommendations_with_links

def find_closest_movie_title(query, movie_titles):
    closest_match = process.extractOne(query, movie_titles)
    return closest_match[0] if closest_match else None

def get_content_based_recommendations(movie_id):
    # Obter o gênero do filme base
    base_movie_genres = filmes[filmes['movieId'] == movie_id]['genres'].values[0]
    base_movie_genres_set = set(base_movie_genres.split('|'))
    
    # Calcular a similaridade de gêneros com outros filmes
    def genre_similarity(movie_genres):
        movie_genres_set = set(movie_genres.split('|'))
        return len(base_movie_genres_set & movie_genres_set) / len(base_movie_genres_set | movie_genres_set)
    
    # Ordenar os filmes pela similaridade de gêneros
    filmes['similarity'] = filmes['genres'].apply(genre_similarity)
    recommended_movies = filmes.sort_values(by='similarity', ascending=False).head(5)
    
    recommended_movie_ids = recommended_movies['movieId'].values
    recommended_titles = recommended_movies['title'].values
    google_links = [f"https://www.google.com/search?q={urllib.parse.quote(movie)} movie" for movie in recommended_titles]
    return list(zip(recommended_titles, google_links))

def get_recommendations(movie_title):
    # Encontre o título mais próximo
    movie_titles = filmes['title'].values
    closest_title = find_closest_movie_title(movie_title, movie_titles)
    
    if closest_title:
        # Obtenha o ID do filme correspondente
        movie_id = filmes[filmes['title'] == closest_title]['movieId'].values[0]
        
        # Aqui você pode continuar com a lógica de recomendação baseada em conteúdo
        print(f"Título mais próximo encontrado: {closest_title}")
        
        # Obter recomendações baseadas em conteúdo
        recommendations = get_content_based_recommendations(movie_id)
        return recommendations
    else:
        print("Nenhum título correspondente encontrado.")
        return []

# Exemplo de uso
movie_query = "The Godfatr"  # O usuário pode errar o título
recommendations = get_recommendations(movie_query)
for movie, link in recommendations:
    print(f"Filme: {movie}, Link: {link}")
