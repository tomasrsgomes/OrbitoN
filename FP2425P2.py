#Orbito-n - FP - Projeto 2

'''
Este projeto consiste em escrever um programa em Python que permita jogar a \
    uma adaptação do jogo Orbito. Para este efeito, foi definido um conjunto \
    de tipos abstratos de dados que foram utilizados para manipular a \
    informação necessária no decorrer do jogo, bem como um conjunto de \
    funções adicionais.

Tomás Gomes
'''


#2.1. Tipos Abstratos de Dados

#2.1.1. TAD posicao
##operações básicas
#construtor
def cria_posicao(col,lin):
    '''
    Recebe um caracter e um inteiro correspondentes à coluna (col) e à linha \
        (lin) e devolve a posição correspondente.
    cria_posicao: str X int --> posicao
    '''

    if not(type(col) == str and len(col) == 1 and 'a' <= col <= 'j' and \
           type(lin) == int and 1 <= lin <= 10):
        raise ValueError ('cria_posicao: argumentos invalidos')
    
    return col,lin


#seletores
def obtem_pos_col(p):
    '''
    Devolve a coluna (col) da posição p.
    obtem_pos_col: posicao --> str
    '''
    return p[0]


def obtem_pos_lin(p):
    '''
    Devolve a linha (lin) da posição p.
    obtem_pos_lin: posicao --> int
    '''
    return p[1]


#reconhecedor
def eh_posicao(arg):
    '''
    Devolve True caso o seu argumento seja um TAD posicao e False caso \
        contrário
    eh posicao: universal --> booleano
    '''
    return type(arg) == tuple and len(arg) == 2 and \
        type(obtem_pos_col(arg)) == str and len(obtem_pos_col(arg)) == 1 and \
        'a' <= obtem_pos_col(arg) <= 'j' and type(obtem_pos_lin(arg)) == int \
        and 1 <= obtem_pos_lin(arg) <= 10


#teste
def posicoes_iguais(p1, p2):
    '''
    Devolve True apenas se p1 e p2 são posições e são iguais, e False caso \
        contrário.
    posicoes_iguais: universal X universal --> booleano
    '''
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2


#transformadores
def posicao_para_str(p):
    '''
    Devolve a cadeia de caracteres que representa o seu argumento.
    posicao_para_str: posicao --> str
    '''
    return obtem_pos_col(p) + str(obtem_pos_lin(p))


def str_para_posicao(s):
    '''
    Devolve a posição representada pelo seu argumento.
    str_para_posicao: str --> posicao
    '''
    return s[0],int(s[1:])


##alto nível
def eh_posicao_valida(p, n):
    '''
    Devolve True se p é uma posição válida dentro do tabuleiro de Orbito-n \
        e False caso contrário.
    eh_posicao_valida: posicao X inteiro --> booleano
    '''

    return eh_posicao(p) and 'a' <= obtem_pos_col(p) <= chr(ord('a') + n*2-1) \
        and 1 <= obtem_pos_lin(p) <= n*2


def obtem_posicoes_adjacentes(p, n, d):
    '''
    Devolve as posições adjacentes ou adjacentes ortogonais de uma posição \
        de um tabuleiro
    
    Devolve um tuplo com as posições do tabuleiro de Orbito-n adjacentes à \
        posição p se d é True, ou as posições adjacentes ortogonais se d é \
        False. As posições do tuplo são ordenadas em sentido horário \
        começando pela posição acima de p.
    obtem_posicoes_adjacentes: posicao X inteiro X booleano --> tuplo
    '''
    
    coluna, linha = obtem_pos_col(p), obtem_pos_lin(p)
    pos_adj = ()
    marca_p2, marca_p4, marca_p6, marca_p8 = 0,0,0,0


    #todas as posições
    if linha - 1 >= 1:
        p1 = cria_posicao(coluna, linha - 1)
        pos_adj += (p1,)

        if ord(coluna)+1 <= 97 + 2*n - 1:
            p2 = cria_posicao(chr(ord(coluna)+1), linha-1)
            pos_adj += (p2,)
            marca_p2 += 1
    
    
    if ord(coluna)+1 <= 97 + 2* n - 1:
        p3 = cria_posicao(chr(ord(coluna)+1), linha) 
        pos_adj += (p3,)

        if linha + 1 <= 2*n:
            p4 = cria_posicao(chr(ord(coluna)+1), linha+1)
            pos_adj += (p4,)
            marca_p4 += 1

    if linha + 1 <= 2*n:
        p5 = cria_posicao(coluna, linha+1)
        pos_adj += (p5,) 
        
        if ord(coluna)-1 >= 97:
            p6 = cria_posicao(chr(ord(coluna)-1), linha+1)
            pos_adj += (p6,)
            marca_p6 += 1
    
    if ord(coluna)-1 >= 97:
        p7 = cria_posicao(chr(ord(coluna)-1), linha)
        pos_adj += (p7,)

        if linha - 1 >= 1:
            p8 = cria_posicao(chr(ord(coluna)-1), linha-1)
            pos_adj += (p8,)
            marca_p8 += 1

    if d:
        return pos_adj

    #retirar posicoes não ortogonais
    else:
        lst_pos_adj = list(pos_adj)
        if marca_p2 > 0:
            lst_pos_adj.remove(p2)
        if marca_p4 > 0:
            lst_pos_adj.remove(p4)
        if marca_p6 > 0:
            lst_pos_adj.remove(p6)
        if marca_p8 > 0:
            lst_pos_adj.remove(p8)


        return tuple(lst_pos_adj)
    
    
def ordena_posicoes(t, n):
    '''
    Devolve um tuplo de posições com as mesmas posições de t ordenadas de \
        acordo com a ordem de leitura do tabuleiro de Orbito-n.
    ordena_posicoes: tuplo X inteiro --> tuplo
    '''
    
    return sorted(t, key = lambda pos: (obtem_orbita(pos, n), \
        obtem_pos_lin(pos), obtem_pos_col(pos)))


#função auxiliar
def obtem_orbita(p,n):
    '''
    Devolve a distância de uma posição ao centro do tabuleiro.
    obtem_distancia_central: posicao X inteiro --> distancia
    '''

    return int((max(abs(ord(obtem_pos_col(p))-96 - (n+0.5)), \
                    abs(obtem_pos_lin(p) - (n+0.5)))) // 1 + 1)


#2.1.2. TAD pedra
##operações básicas
#construtores
def cria_pedra_branca():
    '''
    Devolve uma pedra pertencente ao jogador branco.
    cria_pedra_branca: {} --> pedra
    '''
    return -1 


def cria_pedra_preta():
    '''
    Devolve uma pedra pertencente ao jogador preto.
    cria_pedra_preta: {} --> pedra
    '''
    return 1


def cria_pedra_neutra():
    '''
    Devolve uma pedra neutra
    cria_pedra_neutra: {} --> pedra
    '''
    return 0


#reconhecedores
def eh_pedra(arg):
    '''
    Devolve True caso o seu argumento seja um TAD pedra e False caso contrário.
    eh_pedra: universal --> booleano
    '''
    return type(arg) == int and arg in (-1, 0, 1)


def eh_pedra_branca(p):
    '''
    Devolve True caso a pedra p seja do jogador branco e False caso contrário.
    eh_pedra_branca: pedra --> booleano
    '''
    return p == cria_pedra_branca()


def eh_pedra_preta(p):
    '''
    Devolve True caso a pedra p seja do jogador preto e False caso contrário.
    eh_pedra_preta: pedra --> booleano
    '''
    return p == cria_pedra_preta()


#teste
def pedras_iguais(p1, p2):
    '''
    Devolve True apenas se p1 e p2 são pedras e são iguais.
    pedras_iguais: universal X universal --> booleano
    '''
    return eh_pedra(p1) and eh_pedra(p2) and p1 == p2


#transformadore
def pedra_para_str(p):
    '''
    Transforma a pedra em 'X', 'O' ou ' '

    Devolve a cadeia de caracteres que representa o jogador dono da pedra, \
        isto é, 'O', 'X' ou ' ' para pedras do jogador branco, preto ou \
        neutra respetivamente.
    pedra_para_str: pedra --> str
    '''
    return 'X' if eh_pedra_preta(p) else 'O' if eh_pedra_branca(p) else ' '


##funções de alto nível
def eh_pedra_jogador(p):
    '''
    Devolve True caso a pedra p seja de um jogador e False caso contrário.
    eh_pedra_jogador_: pedra --> booleano
    '''
    return eh_pedra(p) and (eh_pedra_branca(p) or eh_pedra_preta(p))


def pedra_para_int(p):
    '''
    Devolve um inteiro valor 1, -1 ou 0, dependendo se a pedra é do jogador \
        preto, branco ou neutra, respetivamente.
    pedra_para_int: pedra --> int
    '''
    return 1 if eh_pedra_preta(p) else -1 if eh_pedra_branca(p) else 0


#TAD tabuleiro
##operações básicas
#construtores
def cria_tabuleiro_vazio(n):
    '''
    Devolve um tabuleiro de Orbito com n órbitas, sem posições ocupadas.
    cria_tabuleiro_vazio: int --> tabuleiro
    '''

    if not(type(n) == int and 2 <= n <= 5):
        raise ValueError ('cria_tabuleiro_vazio: argumento invalido')
    
    linha = [cria_pedra_neutra()]*2*n
    tab = [linha]
    for l in range(1,2*n):
        tab += [linha.copy()]

    return tab


def cria_tabuleiro(n, tp, tb):
    '''
    Cria um tabuleiro com pedras pretas e brancas
    
    Devolve um tabuleiro de Orbito com n órbitas, com as posições do tuplo tp \
        ocupadas por pedras pretas e as posições do tuplo tb ocupadas por \
        pedras brancas.
    cria_tabuleiro: int X tuplo X tuplo --> tabuleiro
    '''

    if not(type(n) == int and 2 <= n <= 5 and type(tp) == tuple and \
           type(tb) == tuple):                                              
        raise ValueError ('cria_tabuleiro: argumentos invalidos')

    tab = cria_tabuleiro_vazio(n)
    
    if not tp == ():
        for pos in tp:

            if not(eh_posicao(pos) and eh_posicao_valida(pos, n)) \
                or pos in tb or pos in tp[tp.index(pos) + 1:]:
                raise ValueError ('cria_tabuleiro: argumentos invalidos')
            
            tab[obtem_pos_lin(pos) - 1][ord(obtem_pos_col(pos)) - 97] = \
                cria_pedra_preta()
    
    if not tb == ():
        for pos in tb:

            if not(eh_posicao(pos) and eh_posicao_valida(pos, n)) \
                or pos in tp or pos in tb[tb.index(pos) + 1:]:
                raise ValueError ('cria_tabuleiro: argumentos invalidos')

            tab[obtem_pos_lin(pos) - 1][ord(obtem_pos_col(pos)) - 97] = \
                cria_pedra_branca()

    return tab



def cria_copia_tabuleiro(t):
    '''
    Recebe um tabuleiro e devolve uma cópia do tabuleiro.
    cria_copia_tabuleiro: tabuleiro --> tabuleiro
    '''
    return [l.copy() for l in t.copy()]


#seletores
def obtem_numero_orbitas(t):
    '''
    Devolve o número de órbitas do tabuleiro t.
    obtem_numero_orbitas: tabuleiro --> int
    '''
    return len(t)//2


def obtem_pedra(t, p):
    '''
    Devolve a pedra na posição p do tabuleiro t. Se a posição não estiver \
        ocupada, devolve uma pedra neutra.
    obtem_pedra: tabuleiro X posicao --> pedra
    '''
    return t[obtem_pos_lin(p) - 1][ord(obtem_pos_col(p)) - 97]


def obtem_linha_horizontal(t, p):
    '''
    Obtem as posições e as pedras da linha de uma posição
    
    Devolve o tuplo formado por tuplos de dois elementos correspondentes à \
        posicao e o valor de todas as posições da linha horizontal que passa \
        pela posição p, ordenadas de esquerda para a direita.
    obtem_linha_horizontal: tabuleiro X posicao --> tuplo
    '''

    l = obtem_pos_lin(p)
    lin = t[obtem_pos_lin(p) - 1]
    linha = ()
    col = 1
    for pos in lin:
        linha += ((cria_posicao(chr(col + 96), l), pos),)
        col += 1

    return linha


def obtem_linha_vertical(t, p):
    '''
    Obtem as posições e as pedras da coluna de uma posição
    
    Devolve o tuplo formado por tuplos de dois elementos correspondentes à \
        posicao e o valor de todas as posições da linha vertical que passa \
        pela posições p, ordenadas de cima para a baixo.
    obtem_linha_vertical: tabuleiro X posicao --> tuplo
    '''

    c = obtem_pos_col(p)
    coluna = ()
    lin = 1
    for linha in t:
        coluna += ((cria_posicao(c,lin), obtem_pedra(t,cria_posicao(c,lin))),)
        lin += 1
    
    return coluna


def obtem_linhas_diagonais(t, p):
    '''
    Obtem as posições e as pedras da diaganal e da antidiagonal de uma posição
    
    Devolve dois tuplos formados cada um deles por tuplos de dois elementos \
        correspondentes à posicao e o valor de todas as posições que formam a \
        diagonal (descendente da esquerda para a direita ) e antidiagonal \
        (ascendente da esquerda para a direita) que passam pela posição p, \
        respetivamente.
    obtem_linhas_diagonais: tabuleiro X posicao --> tuplo X tuplo
    '''

    col_lin_max = obtem_numero_orbitas(t) *  2
     
    #diagonal
    ##descobrir posição inicial
    i = 0
    while chr(ord(obtem_pos_col(p)) - i) >= 'a' and obtem_pos_lin(p) - i >= 1:
        pos_in_d = cria_posicao(chr(ord(obtem_pos_col(p)) - i), \
                                obtem_pos_lin(p) - i) 
        i += 1
    
    ##criar diagonal
    diagonal = ()
    col = obtem_pos_col(pos_in_d)
    lin = obtem_pos_lin(pos_in_d)
    while ord(col) - 96 <= col_lin_max and lin <= col_lin_max:
        diagonal += ((cria_posicao(col,lin), \
                      obtem_pedra(t,cria_posicao(col,lin))),)
        col = chr(ord(col) + 1)
        lin += 1


    #antidiagonal
    ##descobrir posição inicial
    i = 0
    while chr(ord(obtem_pos_col(p)) - i) >= 'a' and \
        obtem_pos_lin(p) + i <= col_lin_max:
        pos_in_ad = cria_posicao(chr(ord(obtem_pos_col(p)) - i), \
                                obtem_pos_lin(p) + i)
        i += 1

    ##criar antidiagonal
    antidiagonal = ()
    col = obtem_pos_col(pos_in_ad)
    lin = obtem_pos_lin(pos_in_ad)
    while ord(col) - 96 <= col_lin_max and lin >= 1:
        antidiagonal += ((cria_posicao(col,lin), \
                          obtem_pedra(t,cria_posicao(col,lin))),)
        col = chr(ord(col) + 1)
        lin -= 1

    return diagonal, antidiagonal


def obtem_posicoes_pedra(t, j):
    '''
    Devolve o tuplo formado por todas as posições do tabuleiro ocupadas por \
        pedras j (brancas, pretas ou neutras), ordenadas em ordem de leitura \
        do tabuleiro.
    obtem_posicoes_pedra: tabuleiro X pedra --> tuplo
    '''

    posicoes = ()
    lin = 1
    for linha in t:
        col = 'a'
        for pedra in linha:
            if pedra == j:
                posicoes += (cria_posicao(col, lin),)
            col = chr(ord(col) + 1)
        lin += 1

    return ordena_posicoes(posicoes, obtem_numero_orbitas(t))


#modificadores
def coloca_pedra(t, p, j):
    '''
    Modifica destrutivamente o tabuleiro t colocando a pedra j na posição p, \
        e devolve o próprio tabuleiro.
    coloca_pedra: tabuleiro X posicao X pedra --> tabuleiro
    '''

    col, lin = ord(obtem_pos_col(p)) - 97, obtem_pos_lin(p) - 1
    t[lin][col] = j
    return t


def remove_pedra(t, p):
    '''
    Modifica destrutivamente o tabuleiro p removendo a pedra da posição p, e \
        devolve o próprio tabuleiro.
    remove_pedra: tabuleiro X posicao --> tabuleiro
    '''

    col, lin = ord(obtem_pos_col(p)) - 97, obtem_pos_lin(p) - 1
    t[lin][col] = cria_pedra_neutra()
    return t


#reconhecedor
def eh_tabuleiro(arg):
    '''
    Devolve True caso o seu argumento seja um TAD tabuleiro e False caso \
        contrário.
    eh_tabuleiro: universal --> booleano
    '''

    if type(arg) != list:
        return False
    
    if not len(arg) in (4,6,8,10):
        return False
    
    for linha in arg:
        if not(type(linha) == list and len(linha) == len(arg)):
            return False

        for pedra in linha:
            if not eh_pedra(pedra):
                return False
    
    return True


#teste
def tabuleiros_iguais(t1, t2):
    '''
    Devolve True apenas se t1 e t2 forem tabuleiros e forem iguais.
    tabuleiros_iguais: universal X universal --> booleano
    '''

    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1 == t2


#transformador
def tabuleiro_para_str(t):
    '''
    Devolve a cadeia de caracteres que representa o tabuleiro como mostrado \
        nos exemplos.
    tabuleiro_para_str : tabuleiro --> str
    '''

    col_lin_max = obtem_numero_orbitas(t) *  2

    #primeira linha
    linha_1_tup = ()
    letra = 'a'
    while letra <= chr(ord('a') + col_lin_max - 1):
        linha_1_tup += (letra,)
        letra = chr(ord(letra) + 1)

    linha_1_str = '    '
    for l in linha_1_tup:
        linha_1_str += l
        if l != linha_1_tup[-1]:
            linha_1_str += '   '
        else: 
            linha_1_str += '\n'

    #linhas intermédias
    linha_intermedia = ' '
    while len(linha_intermedia) != len(linha_1_str) - 1:
        linha_intermedia += '   |'
    linha_intermedia += '\n'
    

    #tabuleiro
    conta_linha = 1
    tab_str = '01 ['
    for linha in t:
        conta_coluna = 1
        for pedra in linha:
            tab_str += pedra_para_str(pedra) + ']'
            if conta_coluna != col_lin_max:
                tab_str += '-['
            elif conta_linha != col_lin_max:
                tab_str += '\n' + linha_intermedia
            conta_coluna += 1
        
        if conta_linha != col_lin_max:
            if conta_linha + 1 < 10:
                tab_str += '0' + str(conta_linha + 1)
            else:
                tab_str += str(conta_linha + 1)
            tab_str += ' ['
        conta_linha += 1

    tab_str = linha_1_str + tab_str
    return tab_str
    

##funções de alto nível
def move_pedra(t, p1, p2):
    '''
    Modifica destrutivamente o tabuleiro t movendo a pedra da posição p1 para \
        a posição p2, e devolve o próprio tabuleiro.
    move_pedra: tabuleiro X posicao X posicao --> tabuleiro
    '''

    j = obtem_pedra(t, p1)
    remove_pedra(t,p1)
    coloca_pedra(t,p2, j)
    return t


def obtem_posicao_seguinte(t, p, s):
    '''
    Obtem a póxima posição da órbita

    Devolve a posição da mesma órbita que p que se encontra a seguir no \
        tabuleiro t em sentido horário se s for True ou anti-horário se \
        for False.
    obtem_posicao_seguinte: tabuleiro X posicao X booleano --> posicao
    '''
    n = obtem_numero_orbitas(t)
    orb = obtem_orbita(p,n)
    posicoes_adj_ort = obtem_posicoes_adjacentes(p, n, \
                                                 False)
    res_poss = []
    for pos in posicoes_adj_ort:
        if obtem_orbita(pos, n) == obtem_orbita(p, n):
            res_poss += [pos]
    
    if obtem_pos_lin(p) >= n - orb + 2 and ord(obtem_pos_col(p)) - 96 >= n - \
        orb + 2:
        res_poss.reverse()
    
    return res_poss[0] if s else res_poss[1]


def roda_tabuleiro(t):
    '''
    Modifica destrutivamente o tabuleiro t rodando todas as pedras uma \
        posição em sentido anti-horário, e devolve o próprio tabuleiro.
    roda_tabuleiro: tabuleiro --> tabuleiro
    '''
    
    #descobrir posições das pedras brancas e pretas
    pos_pedras_p = obtem_posicoes_pedra(t,cria_pedra_preta())
    pos_pedras_b = obtem_posicoes_pedra(t,cria_pedra_branca())    

    #descobrir as posições deguintes das pedras brancas e pretas
    tp = ()
    for pos_p in pos_pedras_p:
        pos_seguinte_p = obtem_posicao_seguinte(t,pos_p,False)
        tp += (pos_seguinte_p,)
    
    tb = ()
    for pos_b in pos_pedras_b:
        pos_seguinte_b = obtem_posicao_seguinte(t,pos_b,False)
        tb += (pos_seguinte_b,)
    
    #tabuleiro final
    t_novo = cria_tabuleiro(obtem_numero_orbitas(t),tp,tb)

    #esvaziar tabuleiro original
    for pos_p in pos_pedras_p:
        remove_pedra(t,pos_p)
    
    for pos_b in pos_pedras_b:
        remove_pedra(t,pos_b)

    #copiar tabuleiro final para o original
    pos_pedras_p_novo = obtem_posicoes_pedra(t_novo, cria_pedra_preta())
    pos_pedras_b_novo = obtem_posicoes_pedra(t_novo,cria_pedra_branca())

    for pos_p_novo in pos_pedras_p_novo:
        coloca_pedra(t,pos_p_novo,cria_pedra_preta())
    
    for pos_b_novo in pos_pedras_b_novo:
        coloca_pedra(t,pos_b_novo,cria_pedra_branca())
    
    return t
    

def verifica_linha_pedras(t, p, j, k):
    '''
    Verifica se um jogador tem uma sequência de k pedras naquela posição

    Devolve True se existe pelo menos uma linha (horizontal, vertical ou \
        diagonal) que contenha a posição p com k ou mais pedras consecutivas \
        do jogador com pedras j, e False caso contrário.
    verifica_linha_pedras: tabuleiro X posicao X pedra X int --> booleano
    '''

    for linha in (obtem_linha_horizontal(t,p), obtem_linha_vertical(t,p), \
            obtem_linhas_diagonais(t, p)[0], obtem_linhas_diagonais(t,p)[1]):
        idx_pos_val = linha.index((p,obtem_pedra(t,p)))
        
        for i in range(k):
            porcao_linha = linha[idx_pos_val-i:idx_pos_val+k-i] #seqências de k elementos contendo a posição
            valores_porcao_linha = ()
            
            for pos in porcao_linha:
                valores_porcao_linha += (pedra_para_int(pos[1]),)
           
            if sum(valores for valores in valores_porcao_linha) == \
                pedra_para_int(j) * k:
                return True
    
    return False


#2.2. Funções Adicionais
#2.2.1
def eh_vencedor(t, j):
    '''
    Verifica se o jogador com a pedra j ganhou

    Recebe um tabuleiro e uma pedra de jogador, e devolve True se existe uma \
        linha completa do tabuleiro de pedras do jogador ou False caso \
        contrário.
    eh_vencedor: tabuleiro X pedra --> booleano
    '''


    for pos in obtem_posicoes_pedra(t, j):
        if verifica_linha_pedras(t, pos, j, 2 * obtem_numero_orbitas(t)):
            return True 
    return False


#2.2.2
def eh_fim_jogo(t):
    '''
    Recebe um tabuleiro e devolve True se o jogo já terminou ou False caso \
        contrário.
    eh_fim_jogo: tabuleiro --> booleano 
    '''

    return eh_vencedor(t, cria_pedra_preta()) or \
        eh_vencedor(t, cria_pedra_branca()) or \
        obtem_posicoes_pedra(t,cria_pedra_neutra()) == ()


#2.2.3
def escolhe_movimento_manual(t):
    '''
    Recebe um tabuleiro t e permite escolher uma posição livre do tabuleiro \
        onde colocar uma pedra. A função não modifica o seu argumento e \
        devolve a posição escolhida.
    escolhe_movimento_manual: tabuleiro --> posicao
    '''

    while True:
        pos = input('Escolha uma posicao livre:')
        if not (len(pos) in (2,3) and pos[1:].isdigit()):
            continue
        posicao = str_para_posicao(pos)
        if eh_posicao(posicao) and \
            eh_posicao_valida(posicao, obtem_numero_orbitas(t)) and \
            posicao in obtem_posicoes_pedra(t, cria_pedra_neutra()):
            return posicao


#2.2.4
def escolhe_movimento_auto(t, j, lvl):
    '''
    Recebe um tabuleiro t (em que o jogo não terminou ainda), uma pedra j, e \
        a cadeia de carateres lvl correspondente à estratégia, e devolve a \
        posição escolhida automaticamente de acordo com a estratégia \
        selecionada para o jogador com pedras j.
    escolhe_movimento_auto: tabuleiro X pedra X str --> posicao
    '''

    #------------------ Definição das funções de estratégia ------------------#
    
    def estrategia_facil():
        '''
        Se existir no tabuleiro pelo menos uma posição livre que no fim do \
            turno (após rotação) fique adjacente a uma pedra própria, jogar \
            numa dessas posições;
        Se não, jogar numa posição livre.
        estrategia_facil: {} --> posicao
        '''        
        
        pos_livres_ord = ordena_posicoes(\
            obtem_posicoes_pedra(t,cria_pedra_neutra()), \
            obtem_numero_orbitas(t))
        
        novo_tab = roda_tabuleiro(cria_copia_tabuleiro(t))

        for pos in pos_livres_ord:
            valores_adjacentes = ()
            for posicao in obtem_posicoes_adjacentes(\
                obtem_posicao_seguinte(t, pos, False), \
                    obtem_numero_orbitas(novo_tab), True):
                valores_adjacentes += (obtem_pedra(novo_tab, posicao),)
            if j in valores_adjacentes:
                return pos
        
        return pos_livres_ord[0]
    

    def estrategia_normal():
        '''
        Determinar o maior valor de L <= k tal que o próprio jogador \
            conseguir colocar L peçaas consecutivas que contenha essa jogada \
            no fim do turno atual, ou seja, após uma rotação; ou que o \
            conseguir o adversário no fim do seu seguinte turno, ou seja, \
            após duas rotações. Para esse valor:
        Se existir pelo menos uma posição que permita no fim do turno obter \
            uma linha que contenha essa posição com L pedras consecutivas \
            próprias, jogar numa dessas posições;
        Se não, jogar numa posição que impossibilite o adversário no final do \
            seu próximo turno de obter L pedras consecutivas numa linha que \
            contenha essa posição.
        estrategia_normal: {} --> posicao
        '''
        
        pos_livres_ord = ordena_posicoes(\
            obtem_posicoes_pedra(t,cria_pedra_neutra()), \
            obtem_numero_orbitas(t))

        #jogador 
        x = 0
        novo_tab_j = roda_tabuleiro(cria_copia_tabuleiro(t))
        for lj in range(2 * obtem_numero_orbitas(t), 0, -1):
            for pos_j in pos_livres_ord:
                pos_seguinte_j = obtem_posicao_seguinte(t, pos_j, False)
                novo_tab_j_2 = cria_copia_tabuleiro(novo_tab_j)
                coloca_pedra(novo_tab_j_2, pos_seguinte_j, j)
                if verifica_linha_pedras(novo_tab_j_2, pos_seguinte_j, j, lj):
                    x = 1
                    break        
            if x == 1:
                break

        #adversário
        adv = cria_pedra_branca() if j == cria_pedra_preta() else \
            cria_pedra_preta()    
        y = 0
        novo_tab_a = roda_tabuleiro(roda_tabuleiro(cria_copia_tabuleiro(t)))
        for la in range(2 * obtem_numero_orbitas(t), 0, -1):
            for pos_a in pos_livres_ord:
                pos_seguinte_a = obtem_posicao_seguinte(t, \
                            obtem_posicao_seguinte(t, pos_a, False), False)
                novo_tab_a_2 = cria_copia_tabuleiro(novo_tab_a)
                coloca_pedra(novo_tab_a_2, pos_seguinte_a, adv)
                if verifica_linha_pedras(novo_tab_a_2, pos_seguinte_a, adv, la):
                    y = 1
                    break        
            if y == 1:
                break

        #posição a jogar
        if lj > la:
            return pos_j
        elif lj < la:
            return pos_a
        else:
            return pos_j

    #-------------------------------------------------------------------------#     

    if lvl == 'facil':
        return estrategia_facil()

    else:
        return estrategia_normal()


#2.2.5
def orbito(n, modo, jog):
    '''
    Permite jogar um jogo completo de Orbito-n. 
    
    A função recebe o número de órbitas do tabuleiro, uma cadeia de carateres \
        que representa o modo de jogo, e a representação externa de uma pedra \
        (preta ou branca), e devolve um inteiro identificando o jogador \
        vencedor (1 para preto ou -1 para branco), ou 0 em caso de empate.
    orbito: int X str X str --> int
    '''

    if not (type(n) == int and 2 <= n <= 5 and type(modo) == str and modo in \
            ('facil', 'normal', '2jogadores') and type(jog) == str and jog in \
                ('X','O')):
        raise ValueError ('orbito: argumentos invalidos')


    print(f'Bem-vindo ao ORBITO-{n}.')

    tab = cria_tabuleiro_vazio(n)

    
    #1jogador  
    if modo in ('facil', 'normal'):
        
        #jogo
        print(f'Jogo contra o computador ({modo}).')
        print(f"O jogador joga com '{jog}'.")
        print(tabuleiro_para_str(tab))

        jogador = cria_pedra_preta() if jog == 'X' else cria_pedra_branca()
        current = cria_pedra_preta()
        while not eh_fim_jogo(tab):
            if current == jogador:
                print('Turno do jogador.')
                pos = escolhe_movimento_manual(tab)
            else:
                print(f'Turno do computador ({modo}):')
                pos = escolhe_movimento_auto(tab, current, modo)

            coloca_pedra(tab, pos, current)
            roda_tabuleiro(tab)
            print(tabuleiro_para_str(tab))

            current = cria_pedra_branca() if current == cria_pedra_preta() \
                else cria_pedra_preta()

        #verificar resultado
        if eh_vencedor(tab, cria_pedra_branca()) and \
            eh_vencedor(tab, cria_pedra_preta()):
            print('EMPATE')
            return 0
        
        elif eh_vencedor(tab, cria_pedra_preta()):
            if cria_pedra_preta() == jogador:
                print('VITORIA')
            else:
                print('DERROTA')
            return pedra_para_int(cria_pedra_preta())
        
        elif eh_vencedor(tab, cria_pedra_branca()):
            if cria_pedra_branca() == jogador:
                print('VITORIA')
            else:
                print('DERROTA')
            return pedra_para_int(cria_pedra_branca())
        
        else:
            print('EMPATE')
            return 0

                   
    #2jogadores
    else:

        #jogo
        print('Jogo para dois jogadores.')     
        print(tabuleiro_para_str(tab))

        current = cria_pedra_preta()
        while not eh_fim_jogo(tab):
            print(f"Turno do jogador '{pedra_para_str(current)}'.")
            pos = pos = escolhe_movimento_manual(tab)

            coloca_pedra(tab, pos, current)
            roda_tabuleiro(tab)
            print(tabuleiro_para_str(tab))

            current = cria_pedra_branca() if current == cria_pedra_preta() \
                else cria_pedra_preta()
        
        #verificar resultado
        if eh_vencedor(tab, cria_pedra_branca()) and \
            eh_vencedor(tab, cria_pedra_preta()):
            print('EMPATE')
            return 0
        
        elif eh_vencedor(tab, cria_pedra_preta()):
            print("VITORIA DO JOGADOR 'X'")
            return pedra_para_int(cria_pedra_preta())
        
        elif eh_vencedor(tab, cria_pedra_branca()):
            print("VITORIA DO JOGADOR 'O'")
            return pedra_para_int(cria_pedra_branca())
        
        else:
            print('EMPATE')
            return 0