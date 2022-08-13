# -*- coding: utf-8 -*-
"""Analisando_os_Dados_do_Airbnb_Amsterdam.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dFK8LSNQrWfxSiNRIlHFG7WcNlZZwx4E

<center><img src="http://sigmoidal.ai/wp-content/uploads/2019/08/logo_color.png" height="40px"></center>

# Análise dos Dados do Airbnb - Amsterdam

O [Airbnb](https://www.airbnb.com.br/) já é considerado como sendo a **maior empresa hoteleira da atualidade**. Ah, o detalhe é que ele **não possui nenhum hotel**!

Conectando pessoas que querem viajar (e se hospedar) com anfitriões que querem alugar seus imóveis de maneira prática, o Airbnb fornece uma plataforma inovadora para tornar essa hospedagem alternativa.

No final de 2018, a Startup fundada 10 anos atrás, já havia **hospedado mais de 300 milhões** de pessoas ao redor de todo o mundo, desafiando as redes hoteleiras tradicionais.

Uma das iniciativas do Airbnb é disponibilizar dados do site, para algumas das principais cidades do mundo. Por meio do portal [Inside Airbnb](http://insideairbnb.com/get-the-data.html), é possível baixar uma grande quantidade de dados para desenvolver projetos e soluções de *Data Science*.

<center><img alt="Analisando Airbnb" width="10%" src="https://www.area360.com.au/wp-content/uploads/2017/09/airbnb-logo.jpg"></center>

**Neste *notebook*, iremos analisar os dados referentes à cidade de Amsterdam, e ver quais insights podem ser extraídos a partir de dados brutos.**

## Obtenção dos Dados
"""

# Commented out IPython magic to ensure Python compatibility.
# importar os pacotes necessarios

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %matplotlib inline

# importar o arquivo listings.csv para um DataFrame

df = pd.read_csv("http://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/2022-06-05/visualisations/listings.csv")

"""## Análise dos Dados

**Dicionário das variáveis**

* `id` - número de id gerado para identificar o imóvel
* `name` - nome da propriedade anunciada
* `host_id` - número de id do proprietário (anfitrião) da propriedade
* `host_name` - Nome do anfitrião
* `neighbourhood_group` - esta coluna não contém nenhum valor válido
* `neighbourhood` - nome do bairro
* `latitude` - coordenada da latitude da propriedade
* `longitude` - coordenada da longitude da propriedade
* `room_type` - informa o tipo de quarto que é oferecido
* `price` - preço para alugar o imóvel
* `minimum_nights` - quantidade mínima de noites para reservar
* `number_of_reviews` - número de reviews que a propriedade possui
* `last_review` - data do último review
* `reviews_per_month` - quantidade de reviews por mês
* `calculated_host_listings_count` - quantidade de imóveis do mesmo anfitrião
* `availability_365` - número de dias de disponibilidade dentro de 365 dias

Antes de iniciar qualquer análise, vamos verificar a cara do nosso *dataset*, analisando as 5 primeiras entradas.
"""

# mostrar as 5 primeiras entradas

df.head()

"""### **Q1. Quantos atributos (variáveis) e quantas entradas o nosso conjunto de dados possui? Quais os tipos das variáveis?**"""

# identificar o volume de dados do DataFrame

print("Entradas:\t {}".format(df.shape[0]))
print("Variáveis:\t {}\n".format(df.shape[1]))

# verificar os tipos de entradas do dataset

display(df.dtypes)

"""### **Q2. Qual a porcentagem de valores ausentes no *dataset*?**"""

# ordenar em ordem decrescente as variáveis por seus valores ausentes

(df.isnull().sum() / df.shape[0]).sort_values(ascending=False)

"""### **Q3. Qual o tipo de distribuição das variáveis?** """

# plotar o histograma das variáveis numéricas

#Falar um pouco sobre outliers

df.hist(bins=15, figsize=(15,10));

"""**3.1 Outliers**

Pela distribuição do histograma, é possível verificar indícios da presença de outliers. Olhe por exemplo as variáveis price, minimum_nights e calculated_host_listings_count.

Os valores não seguem uma distruição, e distorcem toda a representação gráfica. Para confirmar, há duas maneiras rápidas que auxiliam a detecção de outliers. São elas:

Resumo estatístico por meio do método describe()
Plotar boxplots para a variável.
"""

# ver o resumo estatístico das variáveis numéricas
df[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
    'calculated_host_listings_count', 'availability_365']].describe()

"""Olhando o resumo estatístico acima, podemos confirmar algumas hipóteses como:

A variável price possui 75% do valor abaixo de 240, porém seu valor máximo é 2500.
A quantidade mínima de noites (minimum_nights) está acima do limite real de 365 dias no ano.

## **3.1.1 Boxplot para minimum_nights**
"""

# minimum_nights
df.minimum_nights.plot(kind='box', vert=False, figsize=(15, 3))
plt.show()

# ver quantidade de valores acima de 30 dias para minimum_nights
print("minimum_nights: valores acima de 30:")
print("{} entradas".format(len(df[df.minimum_nights > 30])))
print("{:.4f}%".format((len(df[df.minimum_nights > 30]) / df.shape[0])*100))

"""# **3.1.2 Boxplot para price**"""

# price
df.price.plot(kind='box', vert=False, figsize=(15, 3),)
plt.show()

# ver quantidade de valores acima de 1000 para price
print("\nprice: valores acima de 1000")
print("{} entradas".format(len(df[df.price > 1000])))
print("{:.4f}%".format((len(df[df.price > 1000]) / df.shape[0])*100))

"""# **3.1.3 Histogramas sem outliers**"""

# remover os *outliers* em um novo DataFrame
df_clean = df.copy()
df_clean.drop(df_clean[df_clean.price > 1000].index, axis=0, inplace=True)
df_clean.drop(df_clean[df_clean.minimum_nights > 30].index, axis=0, inplace=True)

# remover `neighbourhood_group`, pois está vazio
df_clean.drop('neighbourhood_group', axis=1, inplace=True)

# plotar o histograma para as variáveis numéricas
df_clean.hist(bins=15, figsize=(15,10));



"""### **Q4. Qual a média dos preços de aluguel?**"""

# ver a média da coluna `price``
# ver o resumo estatístico das variáveis numéricas
df_clean[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
    'calculated_host_listings_count', 'availability_365']].describe()

"""### **Q4. Qual a correlação existente entre as variáveis**"""

# criar uma matriz de correlação
corr = df_clean[['price', 'minimum_nights', 'number_of_reviews', 'reviews_per_month',
    'calculated_host_listings_count', 'availability_365']].corr()

# mostrar a matriz de correlação
display(corr)

# plotar um heatmap a partir das correlações
sns.heatmap(corr, cmap='RdBu', fmt='.2f', square=True, linecolor='white', annot=True);

"""### **Q5. Qual o tipo de imóvel mais alugado no Airbnb?**"""

# mostrar a quantidade de cada tipo de imóvel disponível
df_clean.room_type.value_counts()

df_clean.room_type.value_counts().plot(x="Tipo", y="Quantidade", kind="bar")
plt.show()

# mostrar a porcentagem de cada tipo de imóvel disponível
df_clean.room_type.value_counts() / df_clean.shape[0]

"""### **Q6. Qual a localidade mais cara do dataset?**


"""

# ver preços por bairros, na média
precos_por_bairro = df_clean.groupby(['neighbourhood']).price.mean().sort_values(ascending=False)[:10]
print(precos_por_bairro)

precos_por_bairro_dict = dict(precos_por_bairro)

fig, ax = plt.subplots()
ax.barh(list(precos_por_bairro_dict.keys()), list(precos_por_bairro_dict.values()))

locais = dict(df_clean.groupby(['neighbourhood']).price.mean().sort_values(ascending=False)[:10])
print(locais)

locais.keys()

for local in locais.keys():
  print(df_clean[df_clean.neighbourhood == local].shape)
  df_clean[df_clean.neighbourhood == local].value_counts()

# plotar os imóveis pela latitude-longitude
df_clean.plot(kind="scatter", x='longitude', y='latitude', alpha=0.4, c=df_clean['price'], s=8,
              cmap=plt.get_cmap('jet'), figsize=(12,8));

"""### **Qual a localidade mais barata do dataset?**"""

# ver preços por bairros, na média
precos_por_bairro = df_clean.groupby(['neighbourhood']).price.mean().sort_values(ascending=False)[10:]
print(precos_por_bairro)

precos_por_bairro_dict = dict(precos_por_bairro)

fig, ax = plt.subplots()
ax.barh(list(precos_por_bairro_dict.keys()), list(precos_por_bairro_dict.values()))

"""### **Qual a estadia mais barata em Centrum Oost?**"""

df_clean.head()

df_clean[df_clean['neighbourhood'] == 'Centrum-Oost'].sort_values(by="price")[3:13]



"""### **Q7. Qual é a média do mínimo de noites para aluguel (minimum_nights)?**"""

# ver a média da coluna `minimum_nights``

df_clean[['minimum_nights']].describe()

"""## Conclusões

Foi feita apenas uma análise superficial na base de dados do Airbnb, porém já se percebeu que existem outliers em algumas das variáveis.

Também se notou que em algumas localidades há poucos imóveis disponíveis, o que pode distorcer as informações estatísticas de alguns atributos.

Por fim, lembra-se que este dataset é uma versão resumida, ideal apenas para uma abordagem inicial. Recomenda-se que seja usado, em uma próxima análise exploratória, o conjunto de dados completos, com 106 atributos disponíveis.
"""