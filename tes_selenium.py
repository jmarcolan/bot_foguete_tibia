from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import soup as sg
import db_sql as db

import re
import time 
import numpy as np




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
    
def get_quant_player(driver):
    def limpa_texto(x):
        regex = r"\d*"
        return re.findall(regex,  x)[0]

    s_qnt_player = driver.find_element_by_xpath('//*[@id="betList"]/div/div[1]/h3/div[1]')
    qnt_player = s_qnt_player.get_attribute('innerHTML') 

    return int(limpa_texto(qnt_player))
    
def get_tabela_player(driver):
    s_tabela_playuer = driver.find_element_by_xpath('//*[@id="betList"]/div/div[2]/table')
    plyer_tabela = s_tabela_playuer.get_attribute('innerHTML') 
    
    return plyer_tabela


# FUNCOES PARA ENVIAR OS COMANDOS PARA A TELA
def send_aposta(driver, qnt="1"):
    botao = driver.find_element_by_xpath('//*[@id="betValues"]/div/div/input')
    botao.clear()
    time.sleep(0.3)
    botao.send_keys(qnt)
    time.sleep(0.2)



def click_botao_aposta(driver):
    botao_aposta = driver.find_element_by_xpath('//*[@id="betValues"]/div/div/span/button[5]')
    botao_aposta.click()

def creat_aposta(driver, qnt="1"):
    send_aposta(driver, qnt)
    time.sleep( 0.8 + np.random.uniform(0,3)*0.1)
    click_botao_aposta(driver)

def retira_aposta(driver):
    botao_aposta = driver.find_element_by_xpath('//*[@id="betValues"]/div/button')
    botao_aposta.click()


# def primeiro_jogo()



# assert "Crash - TibiaPlay" in driver.title



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
                db.gravando_tempo(ultimo_valor_antigo)
                print(10*"----")
                print("O ultimo valor pego e atualizado foi o do: ", ultimo_valor_antigo)
                # create aposta.
                
                yield ultimo_valor_antigo
            else:
                yield ultimo_valor_antigo
        else:
            yield ultimo_valor_antigo


def construindo_funcao_geradora_pega_tabela(driver):
    r_pegou_1_vez = False
    # r_resetou = False
    r_game_tem_player = False
    while True:

        
        status_game = get_status_game(driver)
        r_inicio_partida = r_determina_inicio_game(status_game)
        r_game_fim = r_determina_fim_game(status_game)
        
        if r_inicio_partida:
            r_pegou_1_vez = False
            # r_resetou = True
            r_game_tem_player = get_quant_player(driver) != 0
            yield 0

        if r_game_fim and r_game_tem_player:
            if not r_pegou_1_vez:
                r_pegou_1_vez = True
                player_texto = get_tabela_player(driver)

                dados_player = sg.get_dados(player_texto)
                # print(dados_player)
                db.gravando_player(dados_player)
                print(dados_player)
                print(10*"*--*")
                yield 0

        yield 0 


import aposta as ap

def construindo_apostador(driver):

    e1 = ap.estrategia_mock(50, ap.estrategia_v1, "estrategia_v1", qnt_aposta=1)
    
    def faz_aposta(driver, apostador, ultimo_crash):
        print("O ultimo valor pego e atualizado foi o do: ", ultimo_valor_antigo)
        r_fez_aposta = apostador.faz_aposta(ultimo_crash,0)
        if r_fez_aposta:
            print("clicou para fazer as apostas")
            # BOOT CLICANDO VIVO
            # creat_aposta(driver)

        return apostador

    def monitora_fim_partida(driver, apostador):
        # r_not_crash = True
        status_game = get_status_game(driver)
        r_inicio_partida = r_determina_inicio_game(status_game)
        r_not_crash = not r_determina_fim_game(status_game)
        print(r_not_crash)

        r_existe_aposta = apostador.get_status_aposta()
        if r_existe_aposta:
            while r_not_crash:
                r_not_crash = not r_determina_fim_game(status_game)
                time.sleep(0.02)
                status_game = get_status_game(driver)
                r_inicio_partida = r_determina_inicio_game(status_game)
                if not r_inicio_partida:
                    status_game = get_status_game(driver)
                    get_timer = get_timer_texto(status_game)
                    print(f"O tempo {get_timer} da partida em {r_not_crash}")
                    # print(type(get_timer))
                    # print(get_timer)
                    try:
                        valor_atual = float(get_timer)
                        r_clicar = apostador.cliclar_bota(valor_atual)
                        if r_clicar:
                            print("clicou e ganhou")
                            # BOOT CLICANDO VIVO
                            # retira_aposta(driver)
                            # apostador.atualiza_imagem_ganhos()

                            # r_not_crash = False
                        
                        if not r_not_crash and not r_clicar:
                            apostador.atualiza_montante(valor_atual)
                            # apostador.atualiza_imagem_ganhos()
                            print("perdeu")
                    except:
                        print("An exception occurred")

        
            
            
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
                # db.gravando_tempo(ultimo_valor_antigo)
                # print(10*"----")
                # print("O ultimo valor pego e atualizado foi o do: ", ultimo_valor_antigo)
                e1 = faz_aposta(driver, e1, ultimo_valor_antigo)
                monitora_fim_partida(driver, e1)

                
                yield ultimo_valor_antigo
            else:
                yield ultimo_valor_antigo
        else:
            yield ultimo_valor_antigo



def apostando(driver):
    faz_aposta = construindo_apostador(driver)
    while True:
        time.sleep(0.1)
        next(faz_aposta)




def pegando_dados(driver):
    # ultimo_valor_antigo = ""
    pega_valor_1_vez_lal = construindo_funcao_geradora_pega_ultimo(driver)
    pega_tabela = construindo_funcao_geradora_pega_tabela(driver)
    while True:
        time.sleep(0.1)
        next(pega_valor_1_vez_lal)
        next(pega_tabela)




if  __name__ == "__main__":
    PATH = "./chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.tibiaplay.com/crash")
    time.sleep(10)


        # ultimo_valor_antigo = pega_ultimo_valor_apenas_1_vez(driver, ultimo_valor_antigo)
        # print(ultimo_valor_antigo)

        # ultimo_valor_antigo = pega_ultimo_valor_apenas_1_vez(driver, ultimo_valor_antigo)
        # yield ultimo_valor_antigo
        

        




        



