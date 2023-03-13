import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Extração da página.
data_atual = datetime.today().strftime('%Y-%m-%d')
response = requests.get(
    f'https://app.unicesumar.edu.br/presencial/forms/informatica/horario.php?dados={data_atual}%7CN'
)

if not response.status_code == 200:
    raise Exception('Serviço indisponível ou requisição invalidada.')

soup = BeautifulSoup(response.content, 'html.parser')
labs = soup.find_all(name='td', class_='lab')

# Tratamento dos dados.
aulas_hoje = []
for lab in labs:
    reservas = lab.find_all(name='td')

    for horario, reserva in enumerate(reservas[1:], 1):
        lab_name = reservas[0].text
        reserva_name = reserva.text

        # Pula para a próxima execução caso não seja um laboratório.
        if (
            not ('Lab'.upper() in lab_name.upper())
            or 'Carrinho'.upper() in lab_name.upper()
        ):
            continue

        # Filtra por apenas aulas de Engenharia de Software.
        if 'ESOFT5S-N-A'.upper() in reserva_name.upper():
            
            # Recupera a tabela pai que contém os elementos
            table = lab.find_parent(name='table', class_='bloco')
            # Procura na tabela pelo primeiro elemento tr (Cabeçalho)
            bloco = table.find(name='tr').text

            aula = {
                'Horário': horario,
                'Bloco': bloco,
                'Laboratório': lab_name,
                'Reserva': reserva_name,
                'Data_ETL': data_atual,
            }
            aulas_hoje.append(aula)

if not aulas_hoje:
    aulas_hoje.append(
        {
            'Horário': None,
            'Bloco': None,
            'Laboratório': None,
            'Reserva': 'Nenhuma aula encontrada nos laboratórios',
            'Data_ETL': data_atual,
        }
    )

# Carregamento dos dados tratados.
with open('aulas.json', 'w', encoding='utf-8') as arquivo_json:
    json.dump(
        aulas_hoje, arquivo_json, ensure_ascii=False, indent=4, sort_keys=False
    )
