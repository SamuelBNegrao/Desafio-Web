from bs4 import BeautifulSoup
import requests
import json

def list_creator_category(class_name):
    category = parsed_html.select('nav[aria-label="breadcrumbs"] a')
    list = [tag.get_text(strip=True) for tag in category]
    return list

def paragrafo(class_name):
   div = parsed_html.find('div', class_ = class_name)
   paragraphs = div.find_all('p')
   return [p.get_text(strip=True) for p in paragraphs]

def array_produtos(array):
    produtos_lista = []
    for item in array:
            prod_nome = item.find('div', class_= 'prod-nome')
            pnow = item.find('div', class_= 'prod-pnow')
            pold = item.find('div', class_= 'prod-pold')
            available = item.find('i')
            produtos = {
            'name': prod_nome.get_text(strip=True) if prod_nome else None,
            'current_price': pnow.get_text(strip=True) if pnow else None,
            'old-price': pold.get_text(strip=True) if pold else None,
            'available' : not bool(available)}
            produtos_lista.append(produtos)
    return produtos_lista

def array_properties(array):
    propriedades_lista = []
    for item in array:
        tds = item.find_all('td')
        if len(tds) >= 2:
            label_tag = tds[0].find('b')
            label = label_tag.get_text(strip=True) if label_tag else tds[0].get_text(strip=True)
            value = tds[1].get_text(strip=True)
        propriedades = {
            'label': label,
            'value': value}
        propriedades_lista.append(propriedades)
    return propriedades_lista

def array_review(array):
    reviews_lista = []
    for item in array:
        name = item.find('span', class_= 'analiseusername')
        date = item.find('span', class_= 'analisedate')
        text = item.find('p')
        score = item.find('span', class_= 'analisestars')
        if score:
            estrelas = score.get_text(strip=True)
            nota = estrelas.count('★')
        else:
            nota = 0
        analises = {
        'name': name.get_text(strip=True) if name else None,
        'date': date.get_text(strip=True) if date else None,
        'score': nota,
        'text': ' '.join([p.get_text(strip=True) for p in text]) if text else None}
        reviews_lista.append(analises)
    return reviews_lista

def num_score(num):
    score_str = num.split(':')[-1].strip()
    score = score_str.split('/')[0].strip()
    score = float(score)
    return score

url = 'https://infosimples.com/vagas/desafio/commercia/product.html'

# Objeto contendo a resposta final
resposta_final = {}

# Faz o request
response = requests.get(url)

# Parse dos responses
parsed_html = BeautifulSoup(response.content, 'html.parser')
resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()
resposta_final['brand'] = parsed_html.find(class_= 'brand').get_text()
resposta_final['categories'] = list_creator_category('breadcrumbs')
resposta_final['description'] = paragrafo('proddet')
produtos = parsed_html.find_all('div', class_ = 'card')
resposta_final['skus'] = array_produtos(produtos)
properties = parsed_html.find_all('table', class_ = 'pure-table pure-table-bordered')
linhas = []
for tabela in properties:
    linhas.extend(tabela.find_all('tr'))
resposta_final['properties'] = array_properties(linhas)
reviews = parsed_html.find_all('div', class_ = 'analisebox')
resposta_final['reviews'] = array_review(reviews)
average_score = parsed_html.find('h4', string ='Average score: 3.3/5' ).get_text()
resposta_final['review_Average_score'] = num_score(average_score)
resposta_final['url'] = url

# Gera string JSON com a resposta final
json_resposta_final = json.dumps(resposta_final,ensure_ascii=False)
json_resposta_final = json.dumps(resposta_final, indent=1, ensure_ascii=False)

# Salva o arquivo JSON com a resposta final
with open('produto.json', 'w', encoding='utf-8') as arquivo_json:
 arquivo_json.write(json_resposta_final)