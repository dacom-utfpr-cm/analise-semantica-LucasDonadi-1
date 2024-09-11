from myerror import MyError


error_handler = MyError('SemaErrors')


class SymbolsTable:

    def __init__(self):
        self.symbols = list()
        self.headers = ['token', 'lexema', 'tipo', 'dim', 'tam_dim1', 'tam_dim2', 'escopo', 'init', 'utilizada', 'linha']
        self.errors = []


    def add(self, *args):
        self.symbols.append(dict(zip(self.headers, args)))


    def var_declared(self, lexema):
        for i in self.symbols:
            if i['lexema'] == lexema:
                return True

        return False
    
    
    def var_used(self, lexema):
        for i in self.symbols:
            if (i['lexema'] == lexema) and (i['utilizada'] == 'S'):
                return True

        return False


    def check_vars_declared(self, vars):
        for var in vars:
            if not self.var_declared(var):
                self.errors.append(['ERR-SEM-VAR-NOT-DECL', var])

    
    def set_vars_used(self, vars):
        # print(vars)
        if vars:
            for var in vars:
                for i in self.symbols:
                    if i['lexema'] == var:
                        i['utilizada'] = 'S'


    # def check_vars_used(self, vars):
    #     print(vars)
    #     for var in vars:
    #         if not self.var_used(var):
    #             self.errors.append(['WAR-SEM-VAR-DECL-INIT-NOT-USED', var])


    # def set_ini_var(self, lexema, escopo):
    #     for i in self.symbols:
    #         if i['escopo'] == escopo:
    #             print("ASKDLUHAUKSDHKUASHDKUAHSDKUHASD")
    #         # if (i['lexema'] == lexema) and (i['escopo'] == escopo):
    #         #     print("ASDLHAUKSDHKUASD")
    #         #     i['init'] = 'S'
    


    def set_ini_var(self, var, sft):
        
        attr = var.children[2]
        function = None
        var_attr = None


        if attr.name != 'chamada_funcao':
            var_attr = attr

        if attr.name == 'chamada_funcao':
            func_name = attr.children[0].name
            
            func = sft.get_func(func_name)

            if func:
                function = func
            else:
                sft.errors.append(['ERR-SEM-CALL-FUNC-NOT-DECL', func_name])

        
        var_name = ''

        if len(var.children[0].children) == 0:  # Caso seja var com um valor
            var_name = var.children[0].name
        else:   # Caso seja um vetor
            var_name = var.children[0].children[0].name


        for i in self.symbols:
            if i['lexema'] == var_name:

                if i['dim'] != 0:
                    if i['dim'] == 1:
                        if str(i['tam_dim1']).isdigit() is True:
                            i['init'] = 'S'
                            

                    if i['dim'] == 2:
                        if (str(i['tam_dim1']).isdigit() and str(i['tam_dim2']).isdigit()) is True:
                            i['init'] = 'S'
                        
                else:
                    i['init'] = 'S'

                    if attr.name == 'chamada_funcao':
                        if function['tipo'] != i['tipo']:
                            self.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-VAR', function['nome'], function['tipo'], i['lexema'], i['tipo']])

                    else:
                        if var_attr != None:
                            if str(var_attr.name).isnumeric():
                                if str(var_attr.name).isdigit() is False and i['tipo'] == 'inteiro':
                                    self.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM', var_attr.name, 'flutuante', i['lexema'], i['tipo']])
                                elif str(var_attr.name).isdigit() is True and i['tipo'] == 'flutuante':
                                    self.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM', var_attr.name, 'inteiro', i['lexema'], i['tipo']])

                            else:
                                for j in self.symbols:
                                    if j['lexema'] == var_attr.name:
                                        if j['tipo'] != i['tipo']:
                                            self.errors.append(['WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-VAR', var_attr.name, j['tipo'], i['lexema'], i['tipo']])


    # def set_used_var(self, var):
    #     print(var.name)
    #     # used_var = var.children[2].name
    #     # for i in self.symbols:
    #     #     if i['lexema'] == used_var:
    #     #         i['utilizada'] = 'S'


    def var_exists(self, lexema, tipo, escopo):

        for i in self.symbols:
            # if (i['lexema'] == lexema) and (i['escopo'] == tipo) and (i['escopo'] == escopo):
            if (i['lexema'] == lexema) and (i['escopo'] == escopo):
                return True

        return False
    
    def var_name_exists(self, lexema):

        for i in self.symbols:
            if i['lexema'] == lexema:
                return i['tipo']

        return ''


    #ARRUMAR AQUI
    def set_escopo(self, escopo, tipo, lexema):
        # print("Resposta: " + str(self.var_exists(lexema, tipo, escopo)))
        # print(escopo)
        # print("Existe: " + str(self.var_exists(lexema, tipo, escopo)))

        if self.var_exists(lexema, tipo, escopo):
            # print("KUAKK")
            # self.errors.append(['WAR-SEM-VAR-DECL-PREV', lexema, tipo])
            pass
        else:
            for i in self.symbols:
                if i['lexema'] == lexema and i['tipo'] == tipo:
                    i['escopo'] = escopo


    def check_table(self, sft):

        ###### VARIAVEL NAO DECLARADA

        # for i in sft.symbols:
        #     if i['retorna'] != '':
        #         if i['retorna'].isnumeric():
        #             pass
        #         else:
        #             if self.var_name_exists(i['retorna']):
        #                 # print("VAR EXISTE SYMBOLS_TABLE")
        #                 pass
        #             else:
        #                 # print(error_handler.newError('ERR-SEM-VAR-NOT-DECL', a=i['retorna']))
        #                 # self.errors.append(['ERR-SEM-VAR-NOT-DECL', i['retorna']])
        #                 pass



        for i in self.symbols:
            if i['escopo'] == '':
                # print(error_handler.newError('WAR-SEM-VAR-DECL-PREV', a=i['lexema']))
                self.errors.append(['WAR-SEM-VAR-DECL-PREV', i['lexema']])

            if i['dim'] == 1:
                if str(i['tam_dim1']).isdigit() is False:
                    # print(error_handler.newError('ERR-SEM-ARRAY-INDEX-NOT-INT', a=i['lexema']))
                    self.errors.append(['ERR-SEM-ARRAY-INDEX-NOT-INT', i['lexema']])

            elif i['dim'] == 2:
                if (str(i['tam_dim1']).isdigit() and str(i['tam_dim2']).isdigit()) is False:
                    # print(error_handler.newError('ERR-SEM-ARRAY-INDEX-NOT-INT', a=i['lexema']))
                    self.errors.append(['ERR-SEM-ARRAY-INDEX-NOT-INT', i['lexema']])

            else:
                if (i['init'] == 'N') and (i['utilizada'] == 'N'):
                    # print(error_handler.newError('WAR-SEM-VAR-DECL-NOT-USED', a=i['lexema']))
                    self.errors.append(['WAR-SEM-VAR-DECL-NOT-USED', i['lexema']])

                if (i['init'] == 'N') and (i['utilizada'] == 'S'):
                    # print(error_handler.newError('WAR-SEM-VAR-DECL-NOT-USED', a=i['lexema']))
                    self.errors.append(['WAR-SEM-VAR-DECL-NOT-INIT', i['lexema']])
            
                if (i['init'] == 'S') and (i['utilizada'] == 'N'):
                    # print(error_handler.newError('WAR-SEM-VAR-DECL-NOT-USED', a=i['lexema']))
                    self.errors.append(['WAR-SEM-VAR-DECL-INIT-NOT-USED', i['lexema']])

                    

    def get_errors(self, key):
        # print(self.errors)
        # self.set_list()
        if self.errors:
            if key:
                for i in self.errors:
                    print(i[0])
                
            else:
                for i in self.errors:
                    match len(i):
                        case 2:
                            print(error_handler.newError(f"{i[0]}", a=[i[1]]))
                            
                        case 3:
                            print(error_handler.newError(f"{i[0]}", a=[i[1], i[2]]))

                        case 5:
                            print(error_handler.newError(f"{i[0]}", a=[i[1], i[2], i[3], i[4]]))
    


    def prints(self):
        print("|{:^7}|{:^8}|{:^12}|{:^7}|{:^10}|{:^10}|{:^12}|{:^8}|{:^11}|{:^7}|".format('TOKEN', 'LEXEMA', 'TIPO', 'DIM', 'TAM_DIM_1', 'TAM_DIM_2', 'ESCOPO', 'INIT', 'UTILIZADA', 'LINHA'))
        for i in self.symbols:
            print("|{:^7}|{:^8}|{:^12}|{:^7}|{:^10}|{:^10}|{:^12}|{:^8}|{:^11}|{:^7}|".format(i['token'], i['lexema'], i['tipo'], i['dim'], i['tam_dim1'], i['tam_dim2'], i['escopo'], i['init'], i['utilizada'], i['linha']))


    def set_list(self):
        formatted_errors_tuple = [tuple(t) for t in self.errors]
        formatted_errors_tuple = set(formatted_errors_tuple)
        self.errors = [list(t) for t in formatted_errors_tuple]

                        
                    
        

# if __name__ == "__main__":

#     asd = SymbolsTable()

#     asd.add('id', 'a', 'int', 0, 1, 0, 'global', 'N', 1)
#     asd.prints()
