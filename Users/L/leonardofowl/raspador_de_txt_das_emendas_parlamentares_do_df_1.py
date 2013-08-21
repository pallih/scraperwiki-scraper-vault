# Demoulidor Python Extrator de parâmetros das Emendas Parlamentares do DF 2012 para o "DeOlhoNasEmendas" no www.adoteumdistrital.com.br
#
#Os parâmetros que devem ser extraidos e salvos em planilha são:
#Autor da Emenda
#Tipo da Emenda
#Situação da Emenda
#Numero da Emenda
#Numero provisório da Emenda
#Esfera
#UO(Unidade Orçamentária),
#Função,Subfunção,Programa,Ação,Subtítulo,
#Localização
#Produto
#Natureza
#Fonte
#Valor
################################################################
import re
import scraperwiki
textoCompleto = scraperwiki.scrape("http://adoteumdistrital.com.br/arquivos/dcl-2011-11-23-suplemento2.txt")
#print textoCompleto
################################################################


################################################################
#Criando lista do arquivo linha à linha
#Abrindo e escrevendo no arquivo:
arquivoTXT = open("arquivo.txt","w")
arquivoTXT.write(textoCompleto)
arquivoTXT.close()

#Convertendo o arquivo texto em uma lista de strings:
arquivoTXT = open("arquivo.txt","r")
linhasDoTXT = arquivoTXT.readlines()
print "Numero de linhas do arquivo original:"+str(len(linhasDoTXT))
################################################################

########################################################
#Excluindo todas as linhas vazias do arquivo para normalizar a posição relativa das mesmas entre elas e possibilitar a extração automática:
re_linhaconteudo = re.compile('\w') #Encontra todas as linhas com algum conteudo
listaLimpa=[]
for linha in linhasDoTXT:
    if re_linhaconteudo.match(linha):
        listaLimpa.append(linha)
print "Numero de linhas após elimindas as vazias:" + str(len(listaLimpa))
linhasDoTXT = listaLimpa
qtdeLinhasDoTXT = len(linhasDoTXT)
########################################################



########################################################
#Mostrando como seria o arquivo sem espaços em branco:
#Gerando o arquivo sem espaços em branco:
#arquivoTXTsemVazios = open("arquivoSemVazios.txt","w")
#for linha in linhasDoTXT:
#    arquivoTXTsemVazios.write(linha)
#
#arquivoTXT.close()
#
#Imprimindo o arquivo sem espaços em branco
#arquivoTXTsemVazios = open("arquivoSemVazios.txt","r")
#print "Imprimindo arquivo TXT sem Vazios"
#print arquivoTXTsemVazios.read()
#arquivoTXTsemVazios.close()
########################################################

########################################################
def nasProximas5linhasNaoHaEmenda(linhaDoTexto,i):
    naoHaEmenda=False
    n=1
    while n<=5:
        if linhaDoTexto[i+n].find("90101")!=-1: #Se na linha corrente encontrou o texto "90101" então nas imediações desta linha não há dados de emenda
            #print "linhaDoTexto : "+linhaDoTexto[i+n]
            naoHaEmenda = True
        n=n+1
    return naoHaEmenda
########################################################


########################################################
def encontraLinhaComTexto(textoProcurado, linhasDoTexto, indiceLinhaReferencia, linhasAcima, linhasAbaixo):
    indiceLinhaEncontrada=0
    i=indiceLinhaReferencia-linhasAcima
    f=indiceLinhaReferencia+linhasAbaixo
    while i<=f:
        if linhasDoTexto[i].find(textoProcurado)!=-1: #Se a linha corrente encontrou o texto retorne o numero da linha
            #print "linhaDoTexto : "+linhasDoTexto[i+n]
            indiceLinhaEncontrada=i
            i=f+1
        else:
            i=i+1
    return indiceLinhaEncontrada

########################################################


########################################################
# Finalmente localizando e copiando todos os parâmetros das Emendas Parlamentares do DF 2012 para o DeOlhoNasEmendas
#Inicializando os parâmetros:
numeroDaEmenda = ""
numeroProvisorioDaEmenda = ""
subtitulo = ""
autorDaEmenda = ""
valor = ""
unidadeUO = ""
localizacao = ""
situacaoDaEmenda = ""
esfera = ""
funcao = ""
subfuncao = ""
programa = ""
acao = ""
produto = ""
natureza = ""
fonte = ""


listaLinhasCSV = []
listaParametrosLinhaCSV = []

i=0 #Zera o contador de linhas
n=0 #Contador generico
ordemEmqueFoiGravada = 0
ordemEmqueFoiGravadaTexto = ""
gravada = False #Informa se a emenda percorrida já foi gravada: False=Não gravada
encontrouParametrosDaEmenda = False
parametrosExtraidos = {}
data = {}
linhaInicialDeUmaEmenda = 0





#print "Numero_da_Emenda,Numero_provisorio_da_Emenda,Subtitulo,Autor_da_Emenda,valor,UO_Unidade_Orcamentaria,Localizacao,Situacao_da_Emenda,Esfera,Funcao,Subfuncao,Programa,Acao"
parametrosExtraidos = {
          "Numero_da_Emenda" : "Numero_da_Emenda",
          "Autor_da_Emenda" : "Autor_da_Emenda",
          "Subtitulo" : "Subtitulo",
          "Valor" : "Valor",
          "UO_Unidade_Orcamentaria" : "UO_Unidade_Orcamentaria",
          "Localizacao" : "Localizacao",
          #"Numero_provisorio_da_Emenda" : numeroProvisorioDaEmenda,
          #"Situacao_da_Emenda" : situacaoDaEmenda,
          "Esfera" : "Esfera",
          "Funcao" : "Funcao",
          "Subfuncao" : "Subfuncao",
          "Programa" : "Programa",
          "Acao" : "Acao"
}
#print parametrosEstraidos
#scraperwiki.sqlite.save(unique_keys=["Subtitulo"], data=parametrosExtraidos)


while i < qtdeLinhasDoTXT: #Enquanto  o contador "i" for menor que a quantidade de linhas do arquivo de texto prossiga
    #Encontrando o início da Emenda e Nome do Autor:
    if linhasDoTXT[i].find("Emenda Modificativa")!= -1: # Se na atual linha de numero "i" for encontrada a expressão "Emenda Modificativa" prossiga
        linhaInicialDeUmaEmenda = i
        gravada = False
        encontrouParametrosDaEmenda = False
        ordemEmqueFoiGravada = ordemEmqueFoiGravada+1
        ordemEmqueFoiGravadaTexto = str(ordemEmqueFoiGravada)
        autorDaEmenda = linhasDoTXT[i-1] # Salve o nome do autor da Emenda que está na linha anterior da linha atual i do arquivo
        situacaoDaEmenda = "Protocolada" #linhasDoTXT[i+1] # Salve a situação da Emenda que está na proxima linha da linha atual i do arquivo
    #Encontrando o Numero da Emenda:
    elif linhasDoTXT[i].find("Esfera:")!=-1: # Se na atual linha de numero "i" for encontrada a expressão "Esfera:"
        if nasProximas5linhasNaoHaEmenda(linhasDoTXT,i): #Se nas próximas 5 linha após a expressão "Esfera:" não haver dados de emendas avance 10 linhas
            i = i+10
        else:
            numeroDaEmenda = linhasDoTXT[i-2] # Salve o Numero da Emenda que está na 2a linha anterior da linha onde foi encontrada "Esfera:"
            numeroDaEmenda = ''.join(numeroDaEmenda.split()) #Retira espaços vazios da string
            if not numeroDaEmenda.isdigit(): #Caso tipo o da emenda No 112
                indiceLinhaComTexto=encontraLinhaComTexto("Emenda:", linhasDoTXT, i, 10, 0) #Encontra a linha com a expressão "Emenda:"
                if indiceLinhaComTexto!=0:
                    numeroDaEmenda = linhasDoTXT[indiceLinhaComTexto+1] # No da Emenda está na 1a linha posterior da linha onde foi encontrada "Emenda:"
                    numeroDaEmenda = ''.join(numeroDaEmenda.split()) #Retira espaços vazios da string
                    autorDaEmenda = linhasDoTXT[indiceLinhaComTexto] # O Novo nome do autor da Emenda está na linha com a expressão "Emenda:"
                    if len(autorDaEmenda)>=12:
                        autorDaEmenda = autorDaEmenda[:len(autorDaEmenda)-12]
                if not numeroDaEmenda.isdigit(): #Caso tipo o da emenda No 104
                    numeroDaEmenda = ''.join(c for c in linhasDoTXT[indiceLinhaComTexto] if c.isdigit()) #  O Número da Emenda está na linha onde foi
                                                                                                         #encontrada a expressão "Emenda:"
                    autorDaEmenda = linhasDoTXT[linhaInicialDeUmaEmenda-1] # O nome do autor da Emenda está na linha anterior da linha Inicial De Uma Emenda                    
                    if not numeroDaEmenda.isdigit(): #Caso tipo o das emendas No 109,200
                        numeroDaEmenda = linhasDoTXT[i-1] # Salve o Numero da Emenda que está na 1a linha anterior da linha onde foi encontrada "Esfera:"
                        numeroDaEmenda = ''.join(numeroDaEmenda.split()) #Retira espaços vazios da string
                        autorDaEmenda = linhasDoTXT[linhaInicialDeUmaEmenda-1] # O nome do autor da Emenda está na linha anterior da linha Inicial De Uma Emenda
   
    if linhasDoTXT[i].find("UO:")!=-1: # Se na atual linha de numero "i" for encontrada a expressão "UO:"
        if nasProximas5linhasNaoHaEmenda(linhasDoTXT,i): #E se nas próximas 5 linha após a expressão "Esfera:" não haver dados de emendas avance 10 linhas
            i = i+10
        else:
            n=0
            while not linhasDoTXT[i+n+1][:5].isdigit(): #Enquanto o comeco da linha nao for um numero de 5 digitos teste a proxima linha
                n=n+1                                   #Cado tipo o da emenda No 101

            unidadeUO = linhasDoTXT[i+n+1] # Salve a Unidade Orçamentaria da Emenda

            if len(unidadeUO)<10:
                while len(unidadeUO)<10: # Desconsidera qualquer linha que não tenha a quantidade mínima de 10 caracteres esperada para UO
                    n=n+1
                    unidadeUO = linhasDoTXT[i+n+1] # Salve a Unidade Orçamentaria da Emenda que está na 2a linha posterior da linha atual i do arquivo

            funcao = linhasDoTXT[i+n+2] # Salve a funcao da Emenda que está na 3a linha posterior da linha atual i do arquivo
            subfuncao = linhasDoTXT[i+n+3] # Salve a esfera da Emenda que está na 4a linha posterior da linha atual i do arquivo
            programa = linhasDoTXT[i+n+4] # Salve a esfera da Emenda que está na 5a linha posterior da linha atual i do arquivo
            acao = linhasDoTXT[i+n+5] # Salve a esfera da Emenda que está na 6a linha posterior da linha atual i do arquivo
            subtitulo = linhasDoTXT[i+n+6]# Salve a esfera da Emenda que está na 7a linha posterior da linha atual i do arquivo
            localizacao = linhasDoTXT[i+n+7] # Salve a esfera da Emenda que está na 8a linha posterior da linha atual i do arquivo

            indiceLinhaComTexto=encontraLinhaComTexto("R$", linhasDoTXT, i+n+7, 0, 10) #Encontra a linha com a expressão "R$:" até 10 linhas após localizacao
            if indiceLinhaComTexto!=0:
                valor = linhasDoTXT[indiceLinhaComTexto]
                valor = valor[valor.find("R$")+2:]
                valor = ''.join(c for c in valor if c.isdigit())
            else:
                print "A emenda "+numeroDaEmenda+" tem valor R$"+valor+"vazio ou não foi encontrada"

            encontrouParametrosDaEmenda = True

    if (encontrouParametrosDaEmenda and not gravada):
    #Se depois que a emenda foi encontrada e os dados não foram gravados ainda prossiga
        #print numeroDaEmenda+","+autorDaEmenda+","+subtitulo+","+valor+","+unidadeUO+","+localizacao+","+esfera+","+funcao+","+subfuncao+","+programa+","+acao
        parametrosExtraidos = {
          "Numero_da_Emenda" : numeroDaEmenda,
          "Autor_da_Emenda" : autorDaEmenda,
          "Subtitulo" : subtitulo,
          "Valor" : valor,
          "UO_Unidade_Orcamentaria" : unidadeUO,
          "Localizacao" : localizacao,
          #"Numero_provisorio_da_Emenda" : numeroProvisorioDaEmenda,
          #"Situacao_da_Emenda" : situacaoDaEmenda,
          "Esfera" : esfera,
          "Funcao" : funcao,
          "Subfuncao" : subfuncao,
          "Programa" : programa,
          "Acao" : acao
        }
        #print parametrosEstraidos
        scraperwiki.sqlite.save(unique_keys=["Numero_da_Emenda"], data=parametrosExtraidos)
        gravada = True
    i = i+1

########################################################




