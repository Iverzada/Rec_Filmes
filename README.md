# Sistema de Recomendação de Filmes

Este é um sistema de recomendação de filmes que usa duas abordagens diferentes: filtragem colaborativa e filtragem baseada em conteúdo. O sistema foi implementado em Python usando a biblioteca Surprise para a filtragem colaborativa e Flask para a criação de uma interface web.

## Como funciona

O sistema possui duas rotas principais:

1. **Ínicio**: Aparece a página inicial da aplicação web. Aqui, o usuário pode inserir o nome de um filme.

2. **Recomendação**: Quando o usuário insere um nome de filme e envia o formulário, o sistema recomenda filmes semelhantes usando duas abordagens:

   - **Filtragem Colaborativa**: Utiliza o algoritmo SVD (Singular Value Decomposition) da biblioteca Surprise para recomendar filmes com base nas avaliações de usuários semelhantes.
   
   - **Filtragem Baseada em Conteúdo**: Calcula a similaridade entre os gêneros do filme inserido e outros filmes na base de dados para recomendar filmes com gêneros semelhantes.

## Instalação

Para executar o sistema localmente, siga estas etapas:

1. Clone este repositório:


1. Clone o repositório:
   ```sh
   git clone https://github.com/Iverzada/Rec_Filmes.git
   cd Rec_filmes
2.Requerimentos:
Bibliotecas: Pandas, Surprise e fuzzywuzzy
   ```sh
   pip install pandas scikit-surprise fuzzywuzzy
```
3. Uso
Para utilizar esse app, execute o script principal:
   ```sh
   python app.py

