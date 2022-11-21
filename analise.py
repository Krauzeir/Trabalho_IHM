import face_recognition as reconhecedor
import colored
import secrets
import random
import simpy
import json

FOTOS_MOTORISTAS = [
    "faces/personagens1.jpg",
    "faces/personagens2.jpg",
    "faces/personagens3.jpg",
    "faces/personagens4.jpg"
]

# Arquivo de Configuração / Mock
ARQUIVO_DE_CONFIGURACAO = "configuracao.json"

# Probabilidades
PROBABILIDADE_DE_IRREGULARIEDADE = 30
PROBABILIDADE_DE_IRREGULARIEDADE_BAIXA = 70
PROBABILIDADE_DE_IRREGULARIEDADE_ALTA = 30



# Tempos relacionados a ação a ser executada
TEMPO_DE_DETECCAO_DE_TRABALHADOR = 40
TEMPO_DE_LIBERACAO_DE_TRABALHADOR = 80
TEMPO_MEDIO_DE_ANALISE = 40
TEMPO_POLICIA = 40


# Ler configuracoes e preparar estruturas de dados
def preparar():
    global configuracao

    configuracao = None
    try:
        with open(ARQUIVO_DE_CONFIGURACAO, "r") as arquivo:
            configuracao = json.load(arquivo)
            if configuracao:
                print("arquivo de configuracao carregado")
            arquivo.close()
    except Exception as e:
        print(f"erro lendo configuração: {str(e)}")

    global trabalhadores_reconhecidos
    trabalhadores_reconhecidos = {}


def simular_chegadas():
    foto = random.choice(FOTOS_MOTORISTAS)
    print(f"foto de motoristas: {foto}")

    motoristas = {
        "foto": foto,
        "trabalhadores": None
    }

    return motoristas


# Validação de trabalhor que foi reconhecido
def trabalhador_reconhecido_previamente(trabalhador):
    global trabalhadores_reconhecidos

    reconhecido_previamente = False
    for reconhecido in trabalhadores_reconhecidos.values():
        if trabalhador["id"] == reconhecido["id"]:
            reconhecido_previamente = True

            break

    return reconhecido_previamente


# Reconhece quem é motorista que trabalha para alguma empresa entre motoristas
def reconhecer_trabalhadores(motoristas):
    global configuracao

    print("realizando reconhecimento de trabalhadores...")
    foto_motoristas = reconhecedor.load_image_file(motoristas["foto"])
    caracteristicas_dos_motoristas = reconhecedor.face_encodings(
        foto_motoristas)

    trabalhadores = []
    for trabalhador in configuracao["trabalhadores"]:
        if not trabalhador_reconhecido_previamente(trabalhador):
            fotos = trabalhador["fotos"]
            total_de_reconhecimentos = 0

            for foto in fotos:
                foto = reconhecedor.load_image_file(foto)
                caracteristicas = reconhecedor.face_encodings(foto)[0]

                reconhecimentos = reconhecedor.compare_faces(
                    caracteristicas_dos_motoristas, caracteristicas)
                if True in reconhecimentos and trabalhador['status']=="Regular":
                    total_de_reconhecimentos += 1

            if total_de_reconhecimentos/len(fotos) >= 0.6:
                trabalhadores.append(trabalhador)
        else:
            print("Trabalhador(es) reconhecido previamente.")

    return (len(trabalhadores) > 0), trabalhadores


# Imprimir dados do trabalhador
def imprimir_dados_do_trabalhador(trabalhador):
    print(colored.fg('black'), colored.bg(
        'yellow'), f"trabalhador reconhecido em {ambiente_de_simulacao.now}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"nome: {trabalhador['nome']}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"idade: {trabalhador['idade']}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"endereço: {trabalhador['endereco']}", colored.attr('reset'))
    print(colored.fg('black'), colored.bg(
        'yellow'), f"trabalha para: {trabalhador['empresa']}", colored.attr('reset'))
    print('-----------------')


# Reconhece a face dos motoristas
def reconhecer_motoristas(ambiente_de_simulacao):
    global trabalhadores_reconhecidos

    while True:
        print(
            f"tentando reconhecer um trabalhador entre motoristas em {ambiente_de_simulacao.now}")

        motoristas = simular_chegadas()
        ocorreram_reconhecimentos, trabalhadores = reconhecer_trabalhadores(
            motoristas)
        if ocorreram_reconhecimentos:
            for trabalhador in trabalhadores:
                trabalhador["tempo_para_liberacao"] = ambiente_de_simulacao.now + \
                    TEMPO_DE_LIBERACAO_DE_TRABALHADOR
                trabalhador["em_analise_irregulariedade"] = False
                trabalhador["irregular"] = False
                trabalhador['preso'] = False

                id_atendimento = secrets.token_hex(nbytes=16).upper()
                trabalhadores_reconhecidos[id_atendimento] = trabalhador

                # imprimir informações do trabalhador
                imprimir_dados_do_trabalhador(trabalhador)
            
        yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_TRABALHADOR)


def liberar_trabalhador(ambiente_de_simulacao):
    global trabalhadores_reconhecidos

    while True:
        print(
            f"tentando liberar um trabalhador em {ambiente_de_simulacao.now}")

        if len(trabalhadores_reconhecidos):
            for id_atendimento, trabalhador in list(trabalhadores_reconhecidos.items()):
                if not trabalhador["em_analise_irregulariedade"] and trabalhador['preso']!=True and ambiente_de_simulacao.now >= trabalhador["tempo_para_liberacao"]:
                    trabalhador_liberado = (random.randint(
                        1, 100) >= PROBABILIDADE_DE_IRREGULARIEDADE)
                    if trabalhador_liberado:
                        trabalhadores_reconhecidos.pop(id_atendimento)
                        print(colored.fg('white'), colored.bg('green'),
                              f"liberando {trabalhador['nome']} em {ambiente_de_simulacao.now}", colored.attr('reset'))
                    else:
                        trabalhador["irregular"] = True

        yield ambiente_de_simulacao.timeout(TEMPO_DE_LIBERACAO_DE_TRABALHADOR)


def analisar_irregulariedade(ambiente_de_simulacao):
    global trabalhadores_reconhecidos

    while True:
        print(
            f"tentando identificar a irregulariedade {ambiente_de_simulacao.now}")

        if len(trabalhadores_reconhecidos):
            for id_atendimento, trabalhador in list(trabalhadores_reconhecidos.items()):
                if trabalhador["irregular"] and trabalhador["preso"]==False:
                    situacao_reconhecida1 = (random.randint(
                        1, 100) <= PROBABILIDADE_DE_IRREGULARIEDADE_BAIXA)
                    situacao_reconhecida2 = (random.randint(
                        1, 100) <= PROBABILIDADE_DE_IRREGULARIEDADE_ALTA)         
                    if situacao_reconhecida1:
                        multa = random.randint(100, 300)
                        print(colored.fg('white'), colored.bg('blue'),
                              f"trabalhador {trabalhador['nome']} em situação de irregulariedade BAIXA em {ambiente_de_simulacao.now}", colored.attr('reset'))
                        print(colored.fg('white'), colored.bg('blue'),
                              f"Aplicado multa no valor de R${multa}", colored.attr('reset'))
                        print('-----------')
                        situacao_reconhecida2 = False
                        
                        
                    if situacao_reconhecida2:
                        trabalhadores_reconhecidos[id_atendimento]["preso"] = True
                        print(colored.fg('white'), colored.bg('red'),f"Acionando policia para o atendimento {id_atendimento}",colored.attr('reset'))
                        print('-----------')
                        acionar_policia(trabalhador)
                        
        yield ambiente_de_simulacao.timeout(TEMPO_MEDIO_DE_ANALISE)

def contar_trabalhadores_perigosos():
    global trabalhadores_reconhecidos

    quant_irregulares_alta = 0
    for trabalhador in trabalhadores_reconhecidos.values():
        if trabalhador["preso"]:
            quant_irregulares_alta  += 1

    return quant_irregulares_alta 

def acionar_policia(trabalhador):
    global trabalhadores_reconhecidos
    
    while True:
        print(colored.fg('white'), colored.bg('red'),f"Sistema validando se existe algum trabalhor que seja necessário ser preso",colored.attr('reset'))
        
        for trabalhador in trabalhadores_reconhecidos.values():
            if trabalhador["preso"]:
                print(colored.fg('white'), colored.bg('red'),f"Policia acionada para apreensão do trabalhador {trabalhador['nome']}",colored.attr('reset'))
                print('-----------')
                trabalhador['status'] = "Irregular"   
                
        yield ambiente_de_simulacao.timeout(TEMPO_POLICIA)

if __name__ == "__main__":
    preparar()

    ambiente_de_simulacao=simpy.Environment()
    ambiente_de_simulacao.process(reconhecer_motoristas(ambiente_de_simulacao))
    ambiente_de_simulacao.process(liberar_trabalhador(ambiente_de_simulacao))
    ambiente_de_simulacao.process(analisar_irregulariedade(ambiente_de_simulacao))
    ambiente_de_simulacao.process(acionar_policia(ambiente_de_simulacao))
    ambiente_de_simulacao.run(until=2000)
