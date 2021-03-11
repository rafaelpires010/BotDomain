from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from datetime import date
import smtplib


class RegistroBot:

    listadomain = []                                            #// Declaração de Variaveis para guardar listas
    ListaTables = []
    ListaDatas = []

    Dataatual = "07/01/2022"                                    #variavel do tipo date esta com  valor definido apenas para teste de email
    #Dataatual = date.today()
    #data_em_texto = Dataatual.strftime('%d/%m/%Y')


    def __init__(self, domain):                                 #metodo Construtor, pega a lista de dominios e passa para o metodo check

        self.listadomain = domain
        self.driver = webdriver.Firefox(executable_path=r"/home/rafael/Documentos/geckodriver")

    def check(self):                                            #metodo onde esta todas a funçoes

        driver = self.driver
        driver.get("https://registro.br/tecnologia/ferramentas/whois/")

        for j in range(len(self.listadomain)):
            campowhois = driver.find_element_by_xpath("//input[@name='whois-field']")
            campowhois.clear()
            campowhois.send_keys(self.listadomain[j])
            campowhois.send_keys(Keys.ENTER)
            time.sleep(3)

            table = driver.find_element_by_xpath("//*[@id='app']/main/section/div[2]/div[2]/div/div/div[1]/div/table")
            table_html = table.get_attribute('outerHTML')
            df = pd.read_html(str(table_html))
            df = df[0]
            self.ListaTables.append(df)

            dataexpiracao = df.iloc[10, 1]
            self.ListaDatas.append(dataexpiracao)



        for i in range(len(self.ListaDatas)):

            if (self.ListaDatas[i] == self.Dataatual):
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('rafapires2210@gmail.com', 'xla-2215rafa')
                msg = "Dominio expirado"
                server.sendmail('rafapires2210@gmail.com', 'rafael.pires@seraph.com.br', msg)
                server.quit()
            else:
                print("tudo em ordem")

        self.driver.close()


RafaelBot = RegistroBot(['autofortebrasil.com.br', 'carmelogrupo.com.br', 'vizarbrasil.com.br'])
RafaelBot.check()
