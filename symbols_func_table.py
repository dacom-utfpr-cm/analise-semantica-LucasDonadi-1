from myerror import MyError
from anytree import Node, RenderTree, AsciiStyle, PostOrderIter, PreOrderIter, findall_by_attr, Walker, Resolver, findall


error_handler = MyError('SemaErrors')


class SymbolsFuncTable:

    def __init__(self):
        self.symbols = list()
        self.headers = ['tipo', 'nome', 'num_param', 'params', 'retorna', 'init']
        self.errors = []


    def add(self, *args):
        self.symbols.append(dict(zip(self.headers, args)))


    def func_exists(self, nome):

        for i in self.symbols:
            if (i['nome'] == nome):
                return True

        return False
    

    def get_func(self, nome):

        for i in self.symbols:
            if (i['nome'] == nome):
                return i

        return None


    # def set_escopo(self, tipo, nome, num_param):
    #     print("Resposta: " + str(self.func_exists(tipo, nome, num_param)))
    #     if not self.func_exists(tipo, nome, num_param):
    #         for i in self.symbols:
    #             if i['tipo'] == tipo and i['nome'] == tipo:
    #                 i['escopo'] = escopo

    def get_lista_args(self, lista_args):
        new_lista_args = list()
        formatted_lista_args = list()

        
        if lista_args.name == 'lista_argumentos':
            for i in PreOrderIter(lista_args):
                if i.name == 'lista_argumentos':
                    new_lista_args.append(i)
            
            new_lista_args = list(reversed(new_lista_args))
                    
            for i in new_lista_args:
                for j in i.children:
                    if j.name != 'lista_argumentos':
                        if j.name != ',':
                            formatted_lista_args.append(j.name)

        else:
            if lista_args.name == 'vazio':
                pass
            else:
                formatted_lista_args.append(lista_args.name)
        
        return formatted_lista_args


    def check_funcion_call(self, chamada, st, escopo):
        nome_func = chamada.children[0].name
        lista_args = self.get_lista_args(chamada.children[2])
        # print(lista_args)
        if nome_func == 'principal':
            if escopo == 'principal':
                self.errors.append(['WAR-SEM-CALL-REC-FUNC-MAIN'])
            else:
                self.errors.append(['ERR-SEM-CALL-FUNC-MAIN-NOT-ALLOWED'])
        else:

            if self.func_exists(nome_func):

                for i in self.symbols:
                    if i['nome'] == nome_func:
                        i['init'] = 'S'

                        if len(lista_args) < int(i['num_param']):
                            self.errors.append(['ERR-SEM-CALL-FUNC-WITH-FEW-ARGS', nome_func])
                        elif len(lista_args) > int(i['num_param']): 
                            self.errors.append(['ERR-SEM-CALL-FUNC-WITH-MANY-ARGS', nome_func])
                        else:
                            params = i['params']

                            for index in range(len(params)):
                                check_is_number = lista_args[index].replace(".", "")

                                if check_is_number.isnumeric():
                                    if (lista_args[index].isdigit() is False) and (params[index][0] == 'inteiro'):
                                        st.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM', lista_args[index], 'flutuante', params[index][1], params[index][0]])
                                    elif (lista_args[index].isdigit() is True) and (params[index][0] == 'flutuante'):
                                        st.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM', lista_args[index], 'inteiro', params[index][1], params[index][0]])
                                
                                else:
                                    for j in st.symbols:
                                        if j['lexema'] == lista_args[index]:
                                            if j['tipo'] != params[index][0]:
                                                st.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-VAR', lista_args[index], j['tipo'], params[index][1], params[index][0]])


                            # print(i['params'])
                            # for arg in lista_args:
                            #     for var in st.symbols:
                                    # if str(arg).isnumeric():
                                    #     if str(arg).isdigit() is False and i['tipo'] == 'inteiro':
                                    #         self.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM', var_attr.name, 'flutuante', i['lexema'], i['tipo']])
                                    #     elif str(arg).isdigit() is True and i['tipo'] == 'flutuante':
                                    #         self.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM', var_attr.name, 'inteiro', i['lexema'], i['tipo']])
                                


            else:
                self.errors.append(['ERR-SEM-CALL-FUNC-NOT-DECL', nome_func])


    def check_func_table(self, st):

        not_main = [func for func in self.symbols if func['nome'] == "principal"]

        if len(not_main) == 0:
            self.errors.append(['ERR-SEM-MAIN-NOT-DECL'])

        for i in self.symbols:
            if i['retorna'] == '':
                self.errors.append(['ERR-SEM-FUNC-RET-TYPE-ERROR', i['nome'], i['tipo'], 'vazio'])

            else:
                for j in st.symbols:
                    if i['retorna'] == j['lexema']:
                        if i['tipo'] != j['tipo']:
                            self.errors.append(['ERR-SEM-FUNC-RET-TYPE-ERROR', i['nome'], i['tipo'], j['tipo']])
            
            if i['init'] == 'N':
                self.errors.append(['WAR-SEM-FUNC-DECL-NOT-USED', i['nome']])

    def get_errors(self, key):

        if self.errors:
            if key:
                for i in self.errors:
                    print(i[0])

            else:
                for i in self.errors:
                    match len(i):
                        case 1:
                            print(error_handler.newError(f"{i[0]}"))

                        case 2:
                            print(error_handler.newError(f"{i[0]}", a=[i[1]]))

                        case 4:
                            print(error_handler.newError(f"{i[0]}", a=[i[1], i[2], i[3]]))


    def string_params(self, params):
        params_str = ''
        if len(params) != 0:
            cont = 0

            params_str = '['
            for i in params:
                params_str = params_str + f"{i[0]}" + ":" + f"{i[1]}"

                if cont+1 < len(params):
                    params_str = params_str + ", "

                cont += 1

            params_str = params_str + ']'
        
        return params_str


    def prints(self):
        print("|{:^12}|{:^16}|{:^11}|{:^46}|{:^9}|{:^8}|".format('TIPO', 'NOME', 'NUM_PARAM', 'PARAMS', 'RETORNA', 'INIT'))
        for i in self.symbols:
            print("|{:^12}|{:^16}|{:^11}|{:^46}|{:^9}|{:^8}|".format(i['tipo'], i['nome'], i['num_param'], self.string_params(i['params']), i['retorna'], i['init']))

# if __name__ == "__main__":

#     asd = SymbolsTable()

#     asd.add('id', 'a', 'int', 0, 1, 0, 'global', 'N', 1)
#     asd.prints()
