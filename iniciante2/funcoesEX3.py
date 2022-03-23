kmveiculo = 0
tempo = 0
velocidade = 0
distancia = 0
litros_usados = 0

def dados():
    print("Insira a quantidade de Km que o veículo percorre com 1 Litro de combustivel: ")
    global kmveiculo
    kmveiculo = float(input())
    print("insira a duração em Horas da viagem: ")
    global tempo
    tempo = float(input())
    print("Insira a velocidade média do veículo durante a viagem: ")
    global velocidade
    velocidade = float(input())

def caldistancia():
    global distancia
    distancia = velocidade * tempo

def litros():
    global litros_usados
    litros_usados = distancia / kmveiculo

def resultado():
    print("A quantidade de combustível será: ", litros_usados, "Litros")

if __name__ == '__main__':
    dados()
    caldistancia()
    litros()
    resultado()
