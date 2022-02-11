import requests
from bs4 import BeautifulSoup


url = 'https://imoveis.mercadolivre.com.br/apartamentos/venda/rio-de-janeiro/rio-de-janeiro-zona-oeste/barra-da-tijuca/'
n_pages = 42 #quantidade de paginas para essa pesquisa

resultados = []
for page in range(n_pages):
    response = requests.get(url, timeout=5) #faz o request da url
    soup = BeautifulSoup(response.content) #coloca o request na biblioteca do BeautifulSoup
    
    lista_de_urls = soup.find_all("a", class_="ui-search-result__content ui-search-link") #seleciona todos os urls da pagina
    lista_de_urls = [w["href"] for w in lista_de_urls]
    
    lista_precos = soup.find_all('span', class_="price-tag-fraction") #achando todos os preços da pagina
    lista_precos = [w.text for w in lista_precos] #organizando os preços em uma lista
    
    lista_nomes = soup.find_all('h2', class_="ui-search-item__title ui-search-item__group__element") #achando os títulos de venda dos aptos
    lista_nomes = [w.text for w in lista_nomes] #organizando os nomes em uma lista
    
    lista_enderecos = soup.find_all('span', class_="ui-search-item__group__element ui-search-item__location") #achando os endereços de cada apto a venda
    lista_enderecos = [w.text for w in lista_enderecos] #organizando os endereços em uma lista
    
    info_dupla = soup.find_all('ul', class_ = "ui-search-card-attributes ui-search-item__group__element") #salvando dois resultados de atributos nessa variavel info_dupla (m2 e número de quartosw)
    
    area = []
    quartos = []

    for line in info_dupla:
        info_area = line.find_all("li")[0].text
        area.append(info_area)
        try:                                              #separando valor da area e do numero de quartos
            info_quartos = line.find_all("li")[1].text
        except:
            info_quartos = '0'
        quartos.append(info_quartos)
    
    lista_de_resultados = list(zip(lista_de_urls, lista_precos, lista_nomes, lista_enderecos, area, quartos)) #armazena as listas dentro de uma nova com todas as informacoes agrupadas
    resultados = resultados + lista_de_resultados #adiciona informacao da pagina atual no conjunto de informacoes de todas as paginas
    
    next_page = (soup.find("a", title="Seguinte")["href"]) #seleciona o url da proxima pagina
    url = next_page #atualiza a pagina atual para ir para a proxima


import pandas as pd
pd.DataFrame(resultados,columns=["Url","Preço","Titulo Imóvel","Endereço","Área","Número de Quartos"]).to_csv("Resultados_MercadoLivre_Barra.csv")





