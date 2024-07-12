import requests
from bs4 import BeautifulSoup as bs
import json

url_login = 'http://127.0.0.1:8000/my-login'
url_dados = 'http://127.0.0.1:8000/dashboard'

login_data = {
    'username': 'usuario_teste_bs4',
    'password': 'mb9@439m39zjgKF'
}

with requests.Session() as session:
    login_page = session.get(url_login)
    soup = bs(login_page.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    login_data['csrfmiddlewaretoken'] = csrf_token

    dados_login = json.dumps(login_data, indent=4, ensure_ascii=False)
    print(dados_login)

    # headers = {
    #     'Referer': url_login,
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    # }

    response = session.post(url_login, data=login_data)
    print(response.status_code)

    if response.status_code == 200:
        dashboard_response = session.get(url_dados)
        if dashboard_response.status_code == 200:
            print(dashboard_response.status_code)

            
            soup = bs(dashboard_response.content, 'html.parser')

            table = soup.find('table', {'id': 'client-table'})
            records = []
            for row in table.find('tbody').find_all('tr'):
                cols = row.find_all('td')
                record_id = int(cols[0].text.strip())
                records.append({
                    'ID': record_id,
                    'Cliente': cols[1].text.strip(),
                    'E-mail': cols[2].text.strip(),
                    'Whatsapp': cols[3].text.strip(),
                    'Endereço': cols[4].text.strip(),
                    'Cidade': cols[5].text.strip(),
                    'Estado': cols[6].text.strip(),
                    'País': cols[7].text.strip(),
                    'Data de adesão': cols[8].text.strip(),
                    'Visualizar': cols[9].find('a')['href']
                })
            for record in records:
                record_json = json.dumps(record, indent=4, ensure_ascii=False)
                print(record_json)

        else:
            print(f"Falha ao acessar a dashboard, código de status: {dashboard_response.status_code}")
    else:
        print(f"Falha no login, código de status: {response.status_code}")
