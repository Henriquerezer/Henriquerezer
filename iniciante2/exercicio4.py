print(' Ferramenta para calculo de consumo de combustivel')

print('Insira quantos Km seu veículo percorre com 1 Litro de combustível')
kmveiculo = float(input())
print('Insira a duração da viagem ')
tempo = float(input())
print('Insira a velocidade média ')
velocidade = float(input())
distancia =  tempo * velocidade
print('A dintância da viagem é igual a: ', distancia)

litros_usados = distancia / kmveiculo

print('A quantidade de litros utilizados é igual a: ', litros_usados)
