import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

with requests.Session() as s:
    url = 'http://ar.facieg.com.br/administrator/login/authenticate'
    r = s.get(url, headers=headers, stream=True)
    soup = BeautifulSoup(r.content, 'html5lib')

    token = soup.find('meta', {'name':'csrf-token'}).get("content")

    email = input("Digite o email: " )
    senha = input("Digite a senha: ")

    dados_login = {
        'utf8': '✓',
        'authenticity_token': token,
        'email': email,
        'password': senha,
        'commit': 'Entrar',
    }

    r = s.post(url, data=dados_login, headers=headers, stream=True, verify=False)

    # operação ternaria que verifica se foi feito o login
    print("Login Realizado" if r.status_code == 200 else "Erro ao fazer login")

    id = 1 #inicia procura o primeiro usuário
    while id < 30000:
        urlCliente = s.get('http://ar.facieg.com.br/administrator/clientes/'+str(id), headers={'X-CSRF-Token': token, 'X-Requested-With': 'XMLHttpRequest'})

        id += 1 # incremento para ir para o proximo usuário

        soupCliente = BeautifulSoup(urlCliente.content, 'html5lib')

        print("ID: "+str(id))

        dados = soupCliente.find_all("dd")
        itens = []
        for item in dados:
            itens.append(item.string) # adiciona o item aos itens
            #print(item.string)

        #print(itens)

        # abre o arquivo csv e cria uma nova linha
        with open('clientes.csv', 'a', newline='', encoding='utf-8') as file:

            writer = csv.writer(file)

            writer.writerow(itens) # escreve a linha com o vetor items

            #file.close