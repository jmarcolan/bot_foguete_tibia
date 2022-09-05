import matplotlib.pyplot as plt
import numpy as np

class estrategia_mock():
    def __init__(self, montante_inicial, estrategia, nome, qnt_aposta=3):
        self.montante_inicial= montante_inicial
        self.montante_atualizado = montante_inicial
        self.estrategia = estrategia
        self.qnt_aposta = qnt_aposta
        self.guarda_produtividade = []
        self.nome = nome
        self.r_faz_aposta = False
        
    def atualiza_montante(self, novo_valor_tempo):
        #         self.last_aposta = novo_valor_tempo
        if novo_valor_tempo > self.t_aposta:
            self.montante_atualizado = self.montante_atualizado + (self.qnt_aposta * self.t_aposta)
        else:
            self.montante_atualizado  = self.montante_atualizado  - self.qnt_aposta
       
        self.guarda_produtividade.append(self.montante_atualizado - self.montante_inicial)


    
    def atualiza_imagem_ganhos(self):
        plt.plot(self.guarda_produtividade, label=self.nome)
        plt.show()

    def get_status_aposta(self):
        return self.r_faz_aposta

    def faz_aposta(self, valor_tempo_passado, i=0):
        valor_tempo_passado = float(valor_tempo_passado)

        self.t_aposta = self.estrategia(valor_tempo_passado)
        self.r_faz_aposta = self.t_aposta >= 1 
        if self.r_faz_aposta:
            self.montante_atualizado = self.montante_atualizado - self.qnt_aposta
            print(f"A {self.nome}, apostou o valor de **{self.t_aposta}x**, tem um montante de {self.montante_atualizado}TC na i:{i}; t ultima {valor_tempo_passado}x")
        else:
            print("não fez aposta nessa rodada")
        return self.r_faz_aposta

    def cliclar_bota(self, valor_atual):
        r_clicou = valor_atual > self.t_aposta
        if r_clicou:
            self.atualiza_montante(valor_atual)
        return r_clicou



def estrategia_v1(x):
    def map_categoria(x):
        x = float(x)
        r_casa = x >= 1 and x  < 1.4
        r_dinheiro = x >= 1.4 and x <2.3
        r_ganancia = x >= 2.3

        if r_casa:
            return "casa"
        elif r_dinheiro:
            return "ganhando"
        elif r_ganancia:
            return "ganancia"
    
    categoria = map_categoria(x)
    r_casa = categoria == "casa"
    r_dinheiro = categoria == "ganhando"
    r_ganancia = categoria == "ganancia"

    r_deu_ruim = x <= 1.01
    if r_deu_ruim:
        return 0 
    else:
        if r_casa:
            return 1.3 + np.random.uniform(0,3)*0.1
        if  r_ganancia:
            return 1.6 + np.random.uniform(0,4)*0.1
        elif r_dinheiro:
            return 0
        else:
            return 0