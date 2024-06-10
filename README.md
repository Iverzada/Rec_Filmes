# Sistema de Recomendação de Filmes

Este é um sistema de recomendação de filmes que usa duas abordagens diferentes: filtragem colaborativa e filtragem baseada em conteúdo. O sistema foi implementado em Python usando a biblioteca Surprise para a filtragem colaborativa, Pandas para análise de dados, Flask para a criação de uma interface web e fuzzywuzzy para comparação de strings, encontrando correspondências aproximadas.

## Como funciona

O sistema possui duas rotas principais:

1. **Ínicio**: Aparece a página inicial da aplicação web. Aqui, o usuário pode inserir o nome de um filme.

2. **Recomendação**: Quando o usuário insere um nome de filme e confirma, o sistema recomenda 5 filmes semelhantes usando duas abordagens:

   - **Filtragem Colaborativa**: Utiliza o algoritmo SVD (Singular Value Decomposition) da biblioteca Surprise para recomendar filmes com base nas avaliações de usuários semelhantes.
   
   - **Filtragem Baseada em Conteúdo**: Calcula a similaridade entre os gêneros do filme inserido e outros filmes na base de dados para recomendar filmes com gêneros semelhantes.

## Instalação

Para executar o sistema localmente, siga estas etapas:

1. Clone o repositório:
   ```sh
   git clone https://github.com/Iverzada/Rec_Filmes.git
   cd sistema-recomendacao-filmes
   ```
2.Requerimentos:
Instale as Dependências e Bibliotecas: Flask, Pandas, Surprise e fuzzywuzzy
   ```sh
   pip install Flask pandas scikit-surprise fuzzywuzzy
   ```
3. Execute o aplicativo Flask:
Para utilizar esse app, execute o script principal:
   ```sh
   python app.py
   ```
4. Acesse o sistema no seu navegador em [http://localhost:5000](http://localhost:5000)
## Requisitos

- Python 3.x
- Flask
- pandas
- scikit-surprise
- fuzzywuzzy

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

