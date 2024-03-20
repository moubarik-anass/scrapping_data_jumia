import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

url = 'https://www.jumia.ma/catalog/?q=tablettes'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    wb = Workbook()
    ws = wb.active
    
    ws.append(['ID', 'Nom du produit', 'Ancienne Prix', 'Pourcentage', 'Nouveau Prix', 'Image du produit'])
    
    products = soup.find_all(class_='core')
    
    product_id = 1

    for product in products:
        name = product.find(class_='name').text.strip()
        
        price = product.find(class_='prc').text.strip()
        
        anc_element = product.find(class_='old')
        if anc_element:
            anc = anc_element.text.strip()
        else:
            anc = price

        pour_element = product.find(class_='bdg _dsct _sm')
        if pour_element:
            pour = pour_element.text.strip()
        else:
            pour = ''
        
        
        image = product.find('img')['data-src']
        
        ws.append([product_id, name, anc, pour, price, image])
        
        product_id += 1

    wb.save('produits.xlsx')
    
    print("Les données ont été sauvegardées dans le fichier produits.xlsx.")
else:
    print("La requête a échoué.")
