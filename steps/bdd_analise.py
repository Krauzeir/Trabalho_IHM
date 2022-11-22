import face_recognition as reconhecedor
import colored
import secrets
import random
import json

# Arquivo de Configuração / Mock
ARQUIVO_DE_CONFIGURACAO = "configuracao.json"

# Ler configuracoes e preparar estruturas de dados
def preparar():
    preparado, configuracao = False, None
    try:
        with open(ARQUIVO_DE_CONFIGURACAO, "r") as arquivo:
            configuracao = json.load(arquivo)
            if configuracao:
                print("arquivo de configuracao carregado")
            arquivo.close()
            
            preparado = True
    except Exception as e:
        print(f"erro lendo configuração: {str(e)}")

    return preparado, configuracao


def simular_chegadas(foto):
    print(f"foto de motoristas: {foto}")

    motoristas = {
        "foto": foto,
        "trabalhadores": None
    }

    return motoristas

# Reconhece quem é motorista que trabalha para alguma empresa entre motoristas
def reconhecer_trabalhadores(configuracao, motoristas):
    foto_motoristas = reconhecedor.load_image_file(motoristas["foto"])
    caracteristicas_dos_motoristas = reconhecedor.face_encodings(
        foto_motoristas)

    trabalhadores = []
    for trabalhador in configuracao["trabalhadores"]:
        fotos = trabalhador["fotos"]
        total_de_reconhecimentos = 0

        for foto in fotos:
            foto = reconhecedor.load_image_file(foto)
            caracteristicas = reconhecedor.face_encodings(foto)[0]

            reconhecimentos = reconhecedor.compare_faces(
                caracteristicas_dos_motoristas, caracteristicas)
            if True in reconhecimentos:
                total_de_reconhecimentos += 1

        if total_de_reconhecimentos/len(fotos) >= 0.6:
            trabalhadores.append(trabalhador)

    return (len(trabalhadores) > 0), trabalhadores


# Imprimir dados do trabalhador
def imprimir_dados_do_trabalhador(trabalhador):
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
def reconhecer_motoristas(trabalhadores_reconhecidos):
    trabalhadores_em_reconhecimento = {}
    
    for trabalhador in trabalhadores_reconhecidos:
        trabalhador["multa"] = False
        trabalhador['preso'] = False

        id_atendimento = secrets.token_hex(nbytes=16).upper()
        trabalhadores_em_reconhecimento[id_atendimento] = trabalhador

        imprimir_dados_do_trabalhador(trabalhador)

    return len(trabalhadores_em_reconhecimento) > 0, trabalhadores_em_reconhecimento

def liberar_trabalhador(trabalhadores_em_reconhecimento, probabilidade_de_liberacao):
    total_de_trabalhadores_liberados = 0
    
    
    for id_atendimento, trabalhador in list(trabalhadores_em_reconhecimento.items()):
        if not trabalhador["preso"]:
            trabalhador_liberado = (random.randint(1, 100)) <= probabilidade_de_liberacao
            if trabalhador_liberado:
                trabalhadores_em_reconhecimento.pop(id_atendimento)
                
                total_de_trabalhadores_liberados += 1
    
    return total_de_trabalhadores_liberados

def analisar_irregulariedade(trabalhadores_em_reconhecimento, probabilidade_de_irregular):
    total_de_trabalhadores_irregulares = 0
    
    for id_atendimento, trabalhador in list(trabalhadores_em_reconhecimento.items()):
        if not trabalhador["multa"]:
            trabalhador_com_multa = (random.randint(1,100) <= probabilidade_de_irregular)
            if trabalhador_com_multa:
                valor_multa = random.randint(100,300)
                trabalhadores_em_reconhecimento[id_atendimento]["multa"] = valor_multa
                
                total_de_trabalhadores_irregulares += 1
                
    return total_de_trabalhadores_irregulares



















# def liberar_trabalhador(trabalhadores_em_reconhecimento, probabilidade_de_liberar):
#     total_trabalhadores_liberados = 0

#     for id_atendimento, trabalhador in list(trabalhadores_em_reconhecimento.items()):
#         if not trabalhador["preso"]:
#             trabalhador_liberado = (random.randint(
#                         1, 100) <= probabilidade_de_liberar)
#             if trabalhador_liberado:
#                 trabalhadores_em_reconhecimento.pop(id_atendimento)
                
#                 total_trabalhadores_liberados += 1
                
#     return total_trabalhadores_liberados


# def analisar_irregulariedade(trabalhadores_em_reconhecimento, probabilidade_multa):
#     total_trabalhadores_irregulares = 0
    
#     for id_atendimento, trabalhador in list(trabalhadores_em_reconhecimento.items()):
#         if not trabalhador["multa"]:
#             multa_entregue = (random.ranint(1,100) <= probabilidade_multa)
#             if multa_entregue:
#                 trabalhadores_em_reconhecimento[id_atendimento]["multa"] = random.ranint(100,300)

#                 total_trabalhadores_irregulares += 1
                
#     return total_trabalhadores_irregulares


# def acionar_policia(trabalhadores_reconhecidos, probabilidade_irregulariedade_alta):
#     total_perseguidos = 0
    
#     for trabalhador in trabalhadores_reconhecidos.values():
#         if not trabalhador["preso"]:
#             irregulariedade_alta = (random.randint(
#                     1, 100)) <= probabilidade_irregulariedade_alta
#             if irregulariedade_alta:
#                 trabalhador["preso"] = True
                
#                 total_perseguidos += 1

#     return total_perseguidos
