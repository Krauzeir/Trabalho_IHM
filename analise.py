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
PROBABILIDADE_DE_PERIGOSO = 20
PROBABILIDADE_DE_LADRAO = 20
PROBABILIDADE_DE_IRREGULAR = 30
PROBABILIDADE_DE_TRANSPORTE_DE_EMPRESA = 30

TEMPO_MEDIO_DE_ANALISE = 40

# Tempos relacionados a ação a ser executada
TEMPO_DE_DETECCAO_DE_TRABLHADOR = 40
TEMPO_DE_ACIONAR_POLICIA = 30
TEMPO_DE_LIBERACAO_DE_TRABALHADOR = 80
TEMPO_DE_ENQUADRO = 80
TEMPO_DE_PRENDER_MOTORISTA = 50

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

def trabalhador_reconhecido_previamente(trabalhador):
    global trabalhadores_reconhecidos

    reconhecido_previamente = False
    for reconhecido in trabalhadores_reconhecidos.values():
        if trabalhador["id"] == reconhecido["id"]:
            reconhecido_previamente = True

            break

    return reconhecido_previamente



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

                reconhecimentos = reconhecedor.compare_faces(caracteristicas_dos_motoristas, caracteristicas)
                if True in reconhecimentos:
                    total_de_reconhecimentos += 1

            if total_de_reconhecimentos/len(fotos) >= 0.6:
                trabalhadores.append(trabalhador)
        else:
            print("trabalhador reconhecido previamente")

    return (len(trabalhadores) > 0), trabalhadores

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
        'yellow'), f"carteira: {trabalhador['carteira']}", colored.attr('reset'))

def reconhecer_motoristas(ambiente_de_simulacao):
    global trabalhadores_reconhecidos

    while True:
        print(f"tentando reconhecer um trabalhador entre motoristas em {ambiente_de_simulacao.now}")

        motoristas = simular_chegadas()
        ocorreram_reconhecimentos, trabalhadores = reconhecer_trabalhadores(motoristas)
        if ocorreram_reconhecimentos:
            for trabalhador in trabalhadores:
                trabalhador["tempo_para_liberacao"] = ambiente_de_simulacao.now + \
                    TEMPO_DE_LIBERACAO_DE_TRABALHADOR
                #trabalhador["em_emergencia"] = False
                #trabalhador["em_uti"] = False

                id_atendimento = secrets.token_hex(nbytes=16).upper()
                trabalhadores_reconhecidos[id_atendimento] = trabalhador

                imprimir_dados_do_trabalhador(trabalhador)

        yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_TRABLHADOR)


if __name__ == "__main__":
    preparar()

    ambiente_de_simulacao = simpy.Environment()
    ambiente_de_simulacao.process(reconhecer_motoristas(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(liberar_paciente(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(identificar_emergencia(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(reservar_uti(ambiente_de_simulacao))
    #ambiente_de_simulacao.process(liberar_leito_da_uti(ambiente_de_simulacao))
    ambiente_de_simulacao.run(until=1000)