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

import scraperwiki
textoCompleto = scraperwiki.scrape("http://thacker.diraol.eng.br/thackerdf/emendasDistritais/2012/txt/dcl-2011-11-23-suplemento2.txt")


#Experimentando busca literal e extração simples
print "Extrai o texto existente entre dois pedaços de texto localizados num texto completo:"
 
def extraia(texto, subtexto1, subtexto2):
#Extrai o texto existente entre dois pedaços de texto (subtexto1 e subtexto2) localizados num texto completo
    return texto.split(subtexto1)[-1].split(subtexto2)[0]

textoExtraido = extraia(textoCompleto, 'LOA 2012', 'Emenda Modificativa')
#print textoCompleto
print textoExtraido

#Experimentando ler o arquivo linha à linha
arquivoTXT = open("arquivo.txt","w")
arquivoTXT.write(textoCompleto)
arquivoTXT.close()
arquivoTXT = open("arquivo.txt","r")

linhasDoTXT = arquivoTXT.readlines()
qtdeLinhasDoTXT = len(linhasDoTXT)
print "qtdeLinhasDoTXT:"
print qtdeLinhasDoTXT

#Excluindo todas as linhas vazias do arquivo para normalizar a posição relativa das mesmas entre elas e possibilitar a extração automática:

textoDaLinhaEliminada = ""
linhaSemEspacosBrancos = ""
linhaComEspacosBrancos = " "
i=0 #Zera o contador de linhas
while i < qtdeLinhasDoTXT: #Enquanto  o contador "i" for menor que a quantidade de linhas do arquivo de texto prossiga
    #print "Linha "+str(i)
    #print len(linhasDoTXT[i])
    linhaComEspacosBrancos = linhasDoTXT[i]
    linhaSemEspacosBrancos = linhaComEspacosBrancos.replace(' ','')
#    print linhaSemEspacosBrancos
    while len(linhaSemEspacosBrancos)==2:
        if len(linhaSemEspacosBrancos)==2: # Se a linha de numero "i" for vazia(tiver tamanho 2), após retirar todo espaço em branco, prossiga.
                                           # Tamanho 2 é considerado vazio porque mesmo uma linha vazia tem 2 caracteres: um de início e outro de fim de linha. 
#            print "A linha "+str(i)+" AGORA é vista como vazia.  ##################### Será Eliminada"
#            print "Eliminada a linha "+str(i)+linhasDoTXT.pop(i)
            textoDaLinhaEliminada=linhasDoTXT.pop(i)
            qtdeLinhasDoTXT = qtdeLinhasDoTXT-1 #Decrementa a quantidade de linhas já que uma delas foi eliminada
        linhaComEspacosBrancos = linhasDoTXT[i]
        linhaSemEspacosBrancos = linhaComEspacosBrancos.replace(' ','')
#        print "A nova linha "+str(i)+" AGORA é "+linhaComEspacosBrancos
#    if len(linhaSemEspacosBrancos)>2:
#        print "CONTEÚDO da linha "+str(i)+" :"+linhaSemEspacosBrancos
    i = i+1
print "Limpeza de espaços em branco na lista de linhas do arquivo Ok"

# Finalmente localizando e copiando todos os parâmetros das Emendas Parlamentares do DF 2012 para o DeOlhoNasEmendas
#Inicializando os parâmetros:
autorDaEmenda = ""
tipoDaEmenda = ""
situacaoDaEmenda = ""
numeroDaEmenda = ""
numeroProvisorioDaEmenda = ""
esfera = ""
unidadeUO = ""
funcao = ""
subfuncao = ""
programa = ""
acao = ""
subtitulo = ""
localizacao = ""
produto = ""
natureza = ""
fonte = ""
valor = ""
i=0 #Zera o contador de linhas
n=0 #Contador generico
ordemEmqueFoiGravada = 0
ordemEmqueFoiGravadaTexto = ""
iD = ""
gravada = False #Informa se a emenda percorrida já foi gravada
parametrosExtraidos = {}
data = {}
linhaInicialDeUmaEmenda = 0

qtdeLinhasDoTXT = len(linhasDoTXT)
print "qtdeLinhasDoTXT:"
print qtdeLinhasDoTXT

while i < qtdeLinhasDoTXT: #Enquanto  o contador "i" for menor que a quantidade de linhas do arquivo de texto prossiga
    if linhasDoTXT[i].find("Emenda Modificativa")!= -1: # Se na atual linha de numero "i" for encontrada a expressão "Emenda Modificativa" prossiga
        linhaInicialDeUmaEmenda = i
        gravada = False
        ordemEmqueFoiGravada = ordemEmqueFoiGravada+1
        ordemEmqueFoiGravadaTexto = str(ordemEmqueFoiGravada)
        autorDaEmenda = linhasDoTXT[i-1] # Salve o nome do autor da Emenda que está na linha anterior da linha atual i do arquivo
        situacaoDaEmenda = linhasDoTXT[i+1] # Salve a situação da Emenda que está na proxima linha da linha atual i do arquivo
    elif (linhasDoTXT[i].find("Esfera:")!=-1 and linhasDoTXT[i+1].find("FISCAL")!=-1):
    # Se na atual linha de numero "i" for encontrada a expressão "Esfera:" e na linha seguinte a expressão "FISCAL" prossiga
        numeroDaEmenda = linhasDoTXT[i-2] # Salve o Numero da Emenda que está na 2a linha anterior da linha atual i do arquivo
        numeroProvisorioDaEmenda = linhasDoTXT[i-1] # Salve a situação da Emenda que está na 1a linha anterior da linha atual i do arquivo
        esfera = linhasDoTXT[i+1] # Salve a esfera da Emenda que está na 1a linha posterior da linha atual i do arquivo
    elif linhasDoTXT[i].find("Programa: A")!=-1 and not(linhasDoTXT[i+2].find("90101")!=-1 or linhasDoTXT[i+3].find("90101")!=-1 or linhasDoTXT[i+4].find("90101")!=-1 or linhasDoTXT[i+5].find("90101")!=-1):
        n=0
        while (linhasDoTXT[i+n+1].find("Localiza")!=-1 or linhasDoTXT[i+n+1].find("Produto")!=-1 or linhasDoTXT[i+n+1].find("Natureza")!=-1):
            n=n+1

        unidadeUO = linhasDoTXT[i+n+1] # Salve a Unidade Orçamentaria da Emenda que está na 2a linha posterior da linha atual i do arquivo

        if len(unidadeUO)<10:
            while len(unidadeUO)<10: # Desconsidera qualquer linha que não tenha a quantidade mínima de 10 caracteres esperada para UO
                n=n+1
            unidadeUO = linhasDoTXT[i+n+1] # Salve a Unidade Orçamentaria da Emenda que está na 2a linha posterior da linha atual i do arquivo

        funcao = linhasDoTXT[i+n+2] # Salve a funcao da Emenda que está na 3a linha posterior da linha atual i do arquivo
        subfuncao = linhasDoTXT[i+n+3] # Salve a esfera da Emenda que está na 4a linha posterior da linha atual i do arquivo
        programa = linhasDoTXT[i+n+4] # Salve a esfera da Emenda que está na 5a linha posterior da linha atual i do arquivo
        acao = linhasDoTXT[i+n+5] # Salve a esfera da Emenda que está na 6a linha posterior da linha atual i do arquivo
        subtitulo = linhasDoTXT[i+n+6] # Salve a esfera da Emenda que está na 7a linha posterior da linha atual i do arquivo
        localizacao = linhasDoTXT[i+n+7] # Salve a esfera da Emenda que está na 8a linha posterior da linha atual i do arquivo

    elif (i>=linhaInicialDeUmaEmenda+50 and not gravada): 
    #Antes de gravar, resolver problema de encode - deve ter um jeito melhor de tratar isso
        # resolvendo manualmente, via replace
        numeroDaEmenda = numeroDaEmenda.replace("\xb0", "o.") #Resolver problema de encode para caractere Nº
        numeroDaEmenda = numeroDaEmenda.replace("\xf3", "ó") #Resolver problema de encode para caractere ó
        
        # resolvendo via python. O problema é que as strings serão gravadas com ?
        subtitulo = subtitulo.decode('ascii','replace').encode('ascii', 'replace')
        autorDaEmenda = autorDaEmenda.decode('ascii', 'replace').encode('ascii', 'replace')
        localizacao = localizacao.decode('ascii', 'replace').encode('ascii', 'replace')
        unidadeUO = unidadeUO.decode('ascii','replace').encode('ascii', 'replace')
        funcao = funcao.decode('ascii', 'replace').encode('ascii', 'replace')
        subfuncao = subfuncao.decode('ascii', 'replace').encode('ascii', 'replace')
        programa = programa.decode('ascii', 'replace').encode('ascii', 'replace')
        acao = acao.decode('ascii', 'replace').encode('ascii', 'replace')

        iD = numeroDaEmenda
        parametrosExtraidos = {
          "Numero da Emenda" : numeroDaEmenda,
          "Subtitulo" : subtitulo,
          "Autor da Emenda" : autorDaEmenda,
          "Valor" : valor,
          "Localizacao" : localizacao,
          "Numero provisorio da Emenda" : numeroProvisorioDaEmenda,
          "Situacao da Emenda" : situacaoDaEmenda,
          "Esfera" : esfera,
          "UO Unidade Orcamentaria" : unidadeUO,
          "Funcao" : funcao,
          "Subfuncao" : subfuncao,
          "Programa" : programa,
          "Acao" : acao
        }

        #print parametrosEstraidos
        scraperwiki.sqlite.save(unique_keys=["Numero da Emenda"], data=parametrosExtraidos)
        gravada = True

#    elif i>=linhaInicialDeUmaEmenda+50: #Se depois que a emenda foi encontrada ja foram percorridas pelo menos 50 linhas prossiga
#        print "Mais 100 linhas se passaram desde que a ultima emenda foi encontrada"
#            print "autorDaEmenda:"
#            print autorDaEmenda
#            if autorDaEmenda=="":
#                print "Autor da Emenda não encontrado"
    i = i+1



#Mostrando como seria o arquivo sem espaços em branco
#arquivoTXTsemVazios = open("arquivoSemVazios.txt","w")
#arquivoTXTsemVazios.write('\n'.join(linhasDoTXT))
#arquivoTXT.close()
##arquivoTXTsemVazios = open("arquivoSemVazios.txt","r")
#print arquivoTXTsemVazios.read()
#arquivoTXT.close()



#for cadaLinha in linhasDoTXT:
    

#while arquivoTXT.readline()!="":
#     print arquivoTXT.readline()

#linhaAtual =
#conteudo_texto = arquivoTXT.read()
#print conteudo_texto
arquivoTXT.close()



