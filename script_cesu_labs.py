from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

# configurando o driver
dataAtual = datetime.today().strftime('%Y-%m-%d')
driver = webdriver.Chrome("C:\\Users\\chrst\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver.get("https://app.unicesumar.edu.br/presencial/forms/informatica/horario.php?dados=" + dataAtual + "%7CN")

# esperando todas as tabelas serem carregadas
wait = WebDriverWait(driver, 10)
tables = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))

# iterando por cada tabela e imprimindo seus dados
for table in tables:
    # criando um objeto BeautifulSoup para analisar o conteúdo HTML da tabela
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
    
    # coletando dados da tabela com o BeautifulSoup
    table_data = [[cell.text.strip() for cell in row.find_all(["th", "td"])] for row in soup.find_all("tr")]
    
    # imprimindo os dados da tabela
    for row in table_data:
        print("\t".join(row))
    print("--------------------")
