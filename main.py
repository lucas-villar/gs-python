import os
import json
import time
import random
from datetime import datetime
os.system("cls")

#Variáveis globais
arquivo_sensores = "sensores.json"
arquivo_log = "logs.json"
arquivo_alertas = "alertas.txt"
menuOn = True


#Funções
def inicializar_arquivo_sensores() -> None: 
    if not os.path.exists(arquivo_sensores):
        with open(arquivo_sensores, 'w') as arq:
            json.dump([], arq)

def inicializar_arquivo_log() -> None:
    if not os.path.exists(arquivo_log):
        with open(arquivo_log, 'w') as arq:
            json.dump([], arq)
            
def inicializar_arquivo_alertas() -> None:
    if not os.path.exists(arquivo_alertas):
        with open(arquivo_alertas, 'w') as arq:
            arq.write("")
        
def salvar_sensores(sensores):
    with open(arquivo_sensores, 'w') as arq:
        json.dump(sensores, arq, indent=4)
        
def carregar_sensores():
    with open(arquivo_sensores, 'r') as arq:
        try:
            return json.load(arq)
        except:
            print("Erro ao carregar sensores. O arquivo pode estar corrompido.")
            return []
        
def cadastrar_sensor():
    sensores = carregar_sensores()
    while True:
        print("--- Cadastro de Sensor ---\n")
        sensor_id = input("ID do sensor: ").strip()
        if sensor_id == "":
            print("\nID não pode estar vazio.\n")
            time.sleep(1.5)
            os.system("cls")
            continue
        
        id_duplicado = False
        for i in sensores:
            if i['id'] == sensor_id:
                id_duplicado = True
        if id_duplicado:
            print("\nEste ID já foi cadastrado.\n")
            time.sleep(1.5)
            os.system("cls")
            continue
        break

    # Loop até receber localização válida
    while True:
        localizacao = input("Localização do sensor: ").strip()
        if localizacao == "":
            print("Localização não pode estar vazia.")
        else:
            break

    # Loop até receber tipo válido
    while True:
        tipo = input("Tipo de sensor: ").strip()
        if tipo == "":
            print("Tipo não pode estar vazio.")
        else:
            break

    # Criando o novo sensor
    novo_sensor = {
        'id': sensor_id,
        'localizacao': localizacao,
        'tipo': tipo
    }

    # Salvando no arquivo JSON
    sensores.append(novo_sensor)
    salvar_sensores(sensores)

    print("\nSensor cadastrado com sucesso!\n")
    input("Pressione Enter para continuar...")
    
def listar_sensores():
    sensores = carregar_sensores()
    if not sensores:
        print("Nenhum sensor cadastrado.\n")
        input("Pressione Enter para continuar...")
        return
    
    # Cabeçalho da tabela
    print(f"{'ID':<10} {'Localização':<25} {'Tipo':<15}")
    print("-" * 50)
    
    # Exibindo cada sensor em linha formatada
    for sensor in sensores:
        print(f"{sensor['id']:<10} {sensor['localizacao']:<25} {sensor['tipo']:<15}")
 
    
    input("\nPressione Enter para continuar...")   

def coletar_dados():
    sensores = carregar_sensores()
    if not sensores:
        print("Nenhum sensor cadastrado\n")
        return

    leituras = []
    for sensor in sensores:
        leitura = {
            'id': sensor['id'],
            'data': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'valor': round(random.uniform(0, 100), 2)
        }
        leituras.append(leitura)

    # Agora salvamos a lista inteira de leituras no arquivo JSON
    with open("logs.json", "w") as arquivo:
        json.dump(leituras, arquivo, indent=4)

    print("--- Coleta de dados concluída! ---\n")
    print(f"{len(sensores)} leituras coletadas e salvas em log.txt.\n")
    input("Pressione Enter para continuar...")

def detectar_risco():
    try:
        with open("logs.json", "r") as arquivo:
            leituras = json.load(arquivo)

        if leituras ==[]:
            print("Nenhuma leitura encontrada.\n")
            input("Pressione Enter para continuar...")
            return

        valores = [leitura['valor'] for leitura in leituras]

        media = sum(valores) / len(valores)
        print("--- Análise de risco de alagamento ---\n")
        if media > 70:
            print(f"Risco de Alagamento: {media:.2f}%\nNíveis críticos!\n")
            input("Pressione Enter para continuar...")
        else:
            print(f"Risco de Alagamento: {media:.2f}%\nNíveis seguros!\n")
            input("Pressione Enter para continuar...")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def emitir_alerta():
    try:
        with open("logs.json", "r") as arquivo:
            leituras = json.load(arquivo)

        if leituras ==[]:
            print("Nenhuma leitura encontrada.\n")
            input("Pressione Enter para continuar...")
            return

        valores = [leitura['valor'] for leitura in leituras]

        media = sum(valores) / len(valores)
        print("--- Análise de risco de alagamento ---\n")
        if media > 70:
            with open("alertas.txt", "a") as arquivo_alerta:
                arquivo_alerta.write(f"Alerta de alagamento emitido! Risco: {media:.0f}%\n")
                print(f"Nível crítico de alagamento ({media:.0f}%), alerta enviado!\n")
                input("Pressione Enter para continuar...")
        else:
            print(f"Risco de baixo de alagamento ({media:.0f}%), alerta não enviado!\n")
            input("Pressione Enter para continuar...")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

#Bloco principal
inicializar_arquivo_sensores()
inicializar_arquivo_log()
inicializar_arquivo_alertas()

while menuOn:
    os.system("cls")
    print("--- Sistema BioSentinelaX ---\n\n1 - Cadastrar Sensor\n2 - Listar Sensores\n3 - Coletar dados\n4 - Calcular risco de alagamento\n5 - Emitir alertas\n0 - Sair\n")
    
    opcao = input("Escolha uma opção: ").strip()
    os.system("cls")
    
    match opcao:
        case "0":
            menuOn = False
        case "1":
            cadastrar_sensor()
        case "2":
            listar_sensores()
        case "3":
            coletar_dados()
        case "4":
            detectar_risco()
        case "5":
            emitir_alerta()


