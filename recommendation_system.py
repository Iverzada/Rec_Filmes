from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import urllib.parse

logging.basicConfig(level=logging.DEBUG)

# Carregar os dados
filmes = pd.read_csv('Filmes.csv', sep=',')
notas = pd.read_csv('Notas.csv', sep=';')
dados = pd.read_csv('Dados.csv')
tags = pd.read_csv('Tags.csv')

logging.debug('CSV files loaded successfully')

# Preprocessamento dos dados
filmes['movieId'] = filmes['movieId'].apply(lambda x: str(x))
df2 = filmes.merge(dados, left_on='title', right_on='Name', how='left')
df2 = df2.merge(tags, left_on='movieId', right_on='movieId', how='left')

# Garantir que todas as colunas utilizadas sejam strings e tratar NaNs
df2['genres'] = df2['genres'].fillna('').astype(str)
df2['Directors_Cast'] = df2['Directors_Cast'].fillna('').astype(str)
df2['Discription'] = df2['Discription'].fillna('').astype(str)
df2['tag'] = df2['tag'].fillna('').astype(str)

# Criar coluna 'Infos'
df2['Infos'] = df2['genres'] + df2['Directors_Cast'] + df2['Discription'] + df2['tag']

# Vetorização e cálculo de similaridade
vec = TfidfVectorizer()
tfidf = vec.fit_transform(df2['Infos'].apply(lambda x: np.str_(x)))
sim = cosine_similarity(tfidf)
sim_df2 = pd.DataFrame(sim, columns=df2['title'], index=df2['title'])

logging.debug('Similarity matrix computed')

def get_recommendations(movie_title):
    logging.debug(f'Searching recommendations for: {movie_title}')
    # Converter o título do filme inserido pelo usuário para minúsculas
    movie_title_lower = movie_title.lower()
    
    # Verificar se o título do filme está no DataFrame
    sim_df2_lower = sim_df2.index.str.lower()
    if movie_title_lower not in sim_df2_lower.values:
        logging.debug('Movie not found in dataset')
        return [("Nenhum filme encontrado com esse título.", "#")]
    
    # Obter as recomendações para o filme inserido
    final_df = sim_df2.loc[sim_df2_lower == movie_title_lower]
    
    # Ordenar as recomendações por similaridade
    sorted_indices = final_df.values.argsort(axis=1)[:, ::-1].flatten()
    
    # Garantir que os índices estejam dentro dos limites do DataFrame
    sorted_indices = sorted_indices[(sorted_indices >= 0) & (sorted_indices < len(final_df.columns))]
    
    # Obter os títulos dos filmes recomendados e formatá-los corretamente
    recommendations = final_df.columns[sorted_indices].tolist()
    recommendations = [title if not isinstance(title, str) else title[:-5] + ', The' if title.endswith(', The') else title for title in recommendations]
    
    logging.debug(f'Recommendations before formatting: {recommendations}')  # Adiciona este log
    
    # Convertendo para um conjunto para remover duplicatas e mantendo a ordem original
    seen = set()
    recommendations = [x for x in recommendations if not (x in seen or seen.add(x))]
    
    # Remover o filme original das recomendações, se presente
    recommendations = [rec for rec in recommendations if isinstance(rec, str) and rec.lower() != movie_title_lower]
    
    logging.debug(f'Recommendations after formatting: {recommendations}')  # Adiciona este log
    
    # Limitar a 5 recomendações
    if len(recommendations) > 5:
        recommendations = recommendations[:5]
    
    # Criar links para as páginas do Google dos filmes recomendados
    google_links = []
    for movie in recommendations:
        google_search_url = f"https://www.google.com/search?q={urllib.parse.quote(movie)}"
        google_links.append(google_search_url)
    
    # Retorna uma lista de tuplas contendo o filme e seu link para o Google
    recommendations_with_links = list(zip(recommendations, google_links))
    return recommendations_with_links
