#ex 1

#lines="int x=5;"

#file  = open("./add.c", 'r')
#lines = file.readlines()

lines=""

keywords    = ["void", "main", "int", "float", "bool", "if", "for", "else", "while", "char", "return"]
operators   = ["=", "==", "+", "-", "*", "/", "++", "--", "+=", "-=", "!=", "||", "&&"]
punctuations= [";", "(", ")", "{", "}", "[", "]"]




















def is_int(x):
    try:
        int(x)
        return True
    except:
        return False







def parsefn(b):
    a=[]
    flag=0
    starting_symbol='S'
        # 5 - FIRST AND FOLLOW


    def first(string):
        #print("first({})".format(string))
        first_ = set()
        if string in non_terminals:
            alternatives = productions_dict[string]

            for alternative in alternatives:
                first_2 = first(alternative)
                first_ = first_ |first_2

        elif string in terminals:
            first_ = {string}

        elif string=='' or string=='#':
            first_ = {'#'}

        else:
            first_2 = first(string[0])
            if '#' in first_2:
                i = 1
                while '#' in first_2:
                    #print("inside while")

                    first_ = first_ | (first_2 - {'#'})
                    #print('string[i:]=', string[i:])
                    if string[i:] in terminals:
                        first_ = first_ | {string[i:]}
                        break
                    elif string[i:] == '':
                        first_ = first_ | {'#'}
                        break
                    first_2 = first(string[i:])
                    first_ = first_ | first_2 - {'#'}
                    i += 1
            else:
                first_ = first_ | first_2


        #print("returning for first({})".format(string),first_)
        return  first_

    

    def follow(nT):
        #print("inside follow({})".format(nT))
        follow_ = set()
        #print("FOLLOW", FOLLOW)
        prods = productions_dict.items()
        if nT==starting_symbol:
            follow_ = follow_ | {'$'}
        for nt,rhs in prods:
            #print("nt to rhs", nt,rhs)
            for alt in rhs:
                for char in alt:
                    if char==nT:
                        following_str = alt[alt.index(char) + 1:]
                        if following_str=='':
                            if nt==nT:
                                continue
                            else:
                                follow_ = follow_ | follow(nt)
                        else:
                            follow_2 = first(following_str)
                            if '#' in follow_2:
                                follow_ = follow_ | follow_2-{'#'}
                                follow_ = follow_ | follow(nt)
                            else:
                                follow_ = follow_ | follow_2
        #print("returning for follow({})".format(nT),follow_)
        return follow_

    productions=[]

    for line in b.split('+'):
        if flag==0:
            terminals=line.split()
        elif flag==1:
            non_terminals=line.split()
        else:
            productions.append(line)
        flag+=1

    starting_symbol=non_terminals[0]

    productions_dict = {}
    productions_len=0


    for nT in non_terminals:
        productions_dict[nT] = []


    for production in productions:
        nonterm_to_prod = production.split("->")
        print(nonterm_to_prod)
        alternatives = nonterm_to_prod[1].split("|")
        for alternative in alternatives:
            productions_len+=1
            productions_dict[nonterm_to_prod[0]].append(alternative)



    FIRST = {}
    FOLLOW = {}

    for non_terminal in non_terminals:
        FIRST[non_terminal] = set()

    for non_terminal in non_terminals:
        FOLLOW[non_terminal] = set()

    for non_terminal in non_terminals:
        FIRST[non_terminal] = FIRST[non_terminal] | first(non_terminal)

    FOLLOW[starting_symbol] = FOLLOW[starting_symbol] | {'$'}
    for non_terminal in non_terminals:
        FOLLOW[non_terminal] = FOLLOW[non_terminal] | follow(non_terminal)

    #print("FOLLOW", FOLLOW)

    a.append("{: ^20}{: ^20}{: ^20}".format('Non Terminals','First','Follow'))
    for non_terminal in non_terminals:
        a.append("{: ^20}{: ^20}{: ^20}".format(non_terminal,str(FIRST[non_terminal]),str(FOLLOW[non_terminal])))

    return(a)

    
##
##for line in lines:
##    for i in line.strip().split(" "):
##        if i in keywords:
##            print (i, " is a keyword")
##        elif i in operators:
##            print (i, " is an operator")
##        elif i in punctuations:
##            print (i, " is a punctuation")
##        elif is_int(i):
##            print (i, " is a number")
##        else:
##            print (i, " is an identifier")
