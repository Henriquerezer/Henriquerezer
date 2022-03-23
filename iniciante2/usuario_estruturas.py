
continua = 's'
while continua == 's':

    print("Insira os valores de Comprimento, Altura  e Largura: ")
    comprimento = float(input())
    altura = float(input())
    largura = float(input())

    volume = comprimento * altura * largura

    print("volume: ",volume)
    print('Caso deseje continuar presione S ')
    continua = input()