programa
{
	
	funcao inicio()
	{
		inteiro idade
		escreva("Digite a idade do indivíduo: \n")
		leia(idade)
		se (idade > 0 e idade <= 12)
		{
			escreva("O indivíduo é uma criança")
		}
		se (idade >=13 e idade <=17)
		{
			escreva("adolescente")
		}
		se (idade >= 18)
		{
			escreva("Adulto")
		}
		se (idade < 0)
		{
			escreva("Idade Inválida")
		}
	}
}
/* $$$ Portugol Studio $$$ 
 * 
 * Esta seção do arquivo guarda informações do Portugol Studio.
 * Você pode apagá-la se estiver utilizando outro editor.
 * 
 * @POSICAO-CURSOR = 319; 
 * @PONTOS-DE-PARADA = ;
 * @SIMBOLOS-INSPECIONADOS = ;
 * @FILTRO-ARVORE-TIPOS-DE-DADO = inteiro, real, logico, cadeia, caracter, vazio;
 * @FILTRO-ARVORE-TIPOS-DE-SIMBOLO = variavel, vetor, matriz, funcao;
 */