'''Lista: Crie uma estrutura de repetição para fazer a leitura de 5 números inteiros e os armazene dentro de uma lista. Após a leitura, crie outra estrutura de repetição para somar todos os valores digitados
Dicionário: Crie um dicionário para armazenar o nome e a nota de 3 alunos, fazendo a leitura dos valores por meio de uma estrutura de repetição. Depois, crie uma nova estrutura de repetição para somar todas as notas e retornar a média
Matriz: Dada a matriz abaixo, construa uma estrutura de repetição para percorrer e somar todos os elementos da matriz'''
if __name__ == '__main__':
    lista = []
    for i in range (1,6):
        valor = int(input('Digite o valor: '))
        lista.append(valor)
    print(lista)
    soma = 0
    for i in range(len(lista)):

        soma += lista[i]
    print('soma: ', soma)
if __name__ == '__main__':
    alunos = {}
    for _ in range (1,4):
        nome = input('Digite o nome: ')
        nota = input('Digite a nota: ')
        alunos[nome] = nota
    print(alunos)
