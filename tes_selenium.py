from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import re
import time 

def get_status_game(driver):
    # status de quando o jogo esta para começar
    # <span>Place your bet! Starting in 3 seconds...</span>
    # status de quando o jogo acaba
    # <span>1.63x - Crash!</span>

    # status de quando o jogo ta rolando
    # <span>1.35x</span>
    status_game = driver.find_element_by_xpath('//*[@id="crashStatus"]')
    timer = status_game.get_attribute('innerHTML') 
    return timer

def get_ultimo_valor_crash(driver):
    s_ultimo_chash_time = driver.find_element_by_xpath('//*[@id="lastResults"]/ul/li[8]')
    timer_crash = s_ultimo_chash_time.get_attribute('innerHTML') 
    return timer_crash
    
def get_tabela_player(driver):
    s_tabela_playuer = driver.find_element_by_xpath('//*[@id="betList"]/div/div[2]/table')
    plyer_tabela = s_tabela_playuer.get_attribute('innerHTML') 
    
    return plyer_tabela




PATH = "./chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.tibiaplay.com/crash")


time.sleep(10)

assert "Crash - TibiaPlay" in driver.title



# se o game ta para começar pegar o ultimo
def get_ultimo_crash(driver):
    status_texto = get_status_game(driver)
    r_inicio_game = r_determina_inicio_game(status_texto)
    
    if r_inicio_game:
        ultimo_valor = get_ultimo_valor_crash(driver)
        # print(ultimo_valor)
        return ultimo_valor

def r_determina_inicio_game(texto):
    saida = re.search(r'Place your bet',texto)
    r_possue_place = saida != None
    return r_possue_place

def r_determina_fim_game(texto):
    saida = re.search(r'Crash!',texto)
    r_possue_crash = saida != None
    return r_possue_crash


def get_timer_texto(texto):
    # regex = r'^[0-9]*[.,]{0,1}[0-9]*$'
    r_texto_existe = texto != None
    if r_texto_existe:
        def filter_vazio(x):
            return x != ""

        regex = r"\d*[.,]?\d*"
        reg_saida = re.findall(regex, texto)
        # print(reg_saida)
        if(reg_saida != None):
            lis_saida = list(filter(filter_vazio, reg_saida))
            return lis_saida[0]

    return None 

    # if (reg_saida != None):
    #     entrada_numero = reg_saida.start()
    #     saida_numero =reg_saida.end()
    #     numero = texto[entrada_numero: saida_numero]
    #     return numero


def construindo_funcao_geradora_pega_ultimo(driver):

    ultimo_valor_antigo = ""
    while True:        
        # print(ultimo_valor_antigo)
        ultimo_crash = get_ultimo_crash(driver)
        r_ultimo_crash_existe = ultimo_crash != None

        if(r_ultimo_crash_existe):
            ultimo_valor = get_timer_texto(ultimo_crash)
            r_ultimo_valor_atualizo = ultimo_valor_antigo != ultimo_valor

            if r_ultimo_valor_atualizo:
                ultimo_valor_antigo = ultimo_valor
                print("O ultimo valor pego e atualizado foi o do: ",ultimo_valor_antigo)
                
                yield ultimo_valor_antigo
            else:
                yield ultimo_valor_antigo
        else:
            yield ultimo_valor_antigo
    


def roda_por_1_minuto(driver):
    # ultimo_valor_antigo = ""
    pega_valor_1_vez_lal = construindo_funcao_geradora_pega_ultimo(driver)

    for i in range(20):
        time.sleep(1)
        next(pega_valor_1_vez_lal)

        # ultimo_valor_antigo = pega_ultimo_valor_apenas_1_vez(driver, ultimo_valor_antigo)
        # print(ultimo_valor_antigo)

        # ultimo_valor_antigo = pega_ultimo_valor_apenas_1_vez(driver, ultimo_valor_antigo)
        # yield ultimo_valor_antigo
        

        




        



