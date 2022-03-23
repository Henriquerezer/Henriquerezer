## Ler uma temperatura em graus Celsius e apresenta-la convertida em graus fahrenheit,
## Função para ler os valores
## função para fazer o cálculo
## Função para mostrar o resultado

F = 0
C = 0
def dados():
    print("Insira a temperatura em Celsius")
    global C
    C = float(input())
def conversor():
    print("Conversor de temperatura")
    global F
    F = (9 * C + 160) / 5
def mostrar():
    print("O valor convertido é igual a: ", F)

if __name__ == '__main__':
    dados()
    conversor()
    mostrar()