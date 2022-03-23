programa
{
	
	funcao inicio()
	{
		real kmveiculo
		real distancia
		real tempo
		real velocidade
		real litros_usados
		escreva("ferramenta para calculo de consumo de combustivel \n")
		escreva("Insira quantos Km o seu veículo percorre com 1 Litro de combústivel: ")
		leia(kmveiculo)
		escreva("\n Insira a duração em horas da sua viagem: ")
		leia(tempo)
		escreva("\n Insira a velocidade média da sua viagem: ")
		leia(velocidade)
		escreva("\n Com base nesses dados de tempo e velocidade média, teremos a distância percorrida:")
		distancia = tempo * velocidade
		escreva("\n A distância da viagem será de: ", distancia, " Km")
		escreva("\n Agora teremos a quantidade de combústivel utilizado: ")
		litros_usados = distancia / kmveiculo
		escreva("\n A quantidade de litros utilizados é igual a: ", litros_usados, " Litros")
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 828; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */