from bs4 import BeautifulSoup
with open('players_apostando_fim.html', 'r') as file:
    html_doc = file.read()


soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())

def get_dados(texto):
    soup = BeautifulSoup(texto, 'html.parser')
    list_saida = []
    
    for player in soup.find_all('tr'):
        dic_saida = {}
        for numero, dados in enumerate(player.find_all("td")):
            r_nome = numero == 0
            r_qnt = numero == 1
            r_mlt = numero == 2

            if r_nome:
                # dic_saida["nome"] = dados.get_text()
                pass
            if r_qnt:
                dic_saida["qt"] = dados.get_text()
            if r_mlt:
                dic_saida["mlt"] = dados.get_text()
        
        list_saida.append(dic_saida)
    
    return list_saida
        # print(dic_saida) 

        # print(dic_saida)
        # print("---------------------------")


# get_dados(soup)