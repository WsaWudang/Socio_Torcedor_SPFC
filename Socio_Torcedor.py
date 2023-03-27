from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
from twilio.rest import Client

#variaveis
login = input("Qual seu login de acesso para o sócio torcedor? ").strip().replace(" ", "")
senha = input("Qual sua senha para acessar o socio torcedor ? ").strip().replace(" ", "")
celular = str(input("\nPara qual numero de você deseja enviar a mensagem ?\n\n"
                "Lembre de colocar o  numero completo: o começo deve ser +55 depois o seu DDD \n"
                "exemplo: +5511912345678\n"))[:14].strip().replace(" ", "")

# Dados da sua conta Twilio
account_sid = 'ACd4ae01609c0ffb0a822ac0bb21e555de'
auth_token = '707751d757341f9403497ef1caef0357'
client = Client(account_sid, auth_token)

#informações para webdriver
service = Service(r'C:\Users\wesle\OneDrive\Área de Trabalho\Wesley\Python\MeusProjetos\ST\Socio_Torcedor\msedgedriver.exe')
options = webdriver.EdgeOptions()
#options.add_argument('headless')
navegador = webdriver.Edge(service=service, options=options)

#entrar no site do st são paulo
navegador.get('https://sociotorcedor.com.br/')

#login e senha 
navegador.find_element(By.XPATH, "/html/body/app-root/div/fengstlayout-header/header/section/nav/a[1]").click()
navegador.find_element(By.XPATH, '//*[@id="mat-input-0"]').send_keys(login)
navegador.find_element(By.XPATH,'//*[@id="mat-input-1"]').send_keys(senha)
navegador.find_element(By.XPATH,'//*[@id="mat-dialog-0"]/fengstauth-modal-auth-st/div/div/mat-dialog-content/div[3]/form/fengstui-button/button').click()
time.sleep(5)

#verifcar se tem erro na hora de entrar no site
if navegador.find_element(By.ID,'swal2-content'):
    print("\n\nSENHA OU LOGIN INVALIDOS, TENTE NOVAMENTE")
    navegador.quit()
else:

    #entrar no site e ir nos extratos 
    while len(navegador.find_elements(By.CLASS_NAME,"home-plans__title")) <1:
            time.sleep(1)
    navegador.find_element(By.XPATH,'/html/body/app-root/div/fengstlayout-header/header/div/div[1]/i').click()
    navegador.find_element(By.XPATH,'/html/body/app-root/div/fengstlayout-header/div/nav/a[5]').click()
    navegador.find_element(By.XPATH,'/html/body/app-root/div/div/fengstexperience-catalog-container/fengstexperience-header/section/nav/a[3]').click()

    #pegar os pontos e data
    while len(navegador.find_elements(By.XPATH,'//*[@id="mat-input-3"]')) <1:
            time.sleep(1)
    pontos = navegador.find_element(By.XPATH,'/html/body/app-root/div/div/fengstexperience-points-container/fengstexperience-points-view/section/fengstexperience-points-table/section/div[2]/section')
    informacao = navegador.find_element(By.XPATH, '/html/body/app-root/div/div/fengstexperience-points-container/fengstexperience-points-view/section/fengstexperience-points-table/section/div[2]/fengstexperience-points-card[1]/fengstexperience-points-card-template-1/article/div[1]')

    #mensagem para enivar no celular
    mensagem = (f"\n{pontos.text}\n" 
          f"Meu Ultimo resgade foi de {informacao.text} \n ")

    # Número de telefone que você deseja enviar a mensagem
    numero_telefone = celular

    # Envie a mensagem SMS usando o método messages.create()
    message = client.messages.create(
                                  body=mensagem,
                                  from_='+14067208752', # Número de telefone Twilio
                                  to=numero_telefone
                              )

    # Imprime a mensagem SID (identificação única) para confirmar que a mensagem foi enviada com sucesso
    print(message.sid)
    print(mensagem)