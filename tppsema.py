import sys
import os
from sys import argv, exit
import ply.yacc as yacc
from tpplex import tokens
from mytree import MyNode
from anytree.exporter import DotExporter, UniqueDotExporter
from anytree import Node, RenderTree, AsciiStyle, PostOrderIter, PreOrderIter, findall_by_attr, Walker, Resolver, findall
from myerror import MyError
from symbols_table import SymbolsTable
from symbols_func_table import SymbolsFuncTable
import tppparser
import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename="sema.log",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Get the token map from the lexer.  This is required.


error_handler = MyError('SemaErrors')


def return_leaf(no):
    
    for node in no.descendants:
        if node.is_leaf:
            return node


def check_fator(no):
    aux = no
    while len(aux.children) == 1:
        if aux.name == 'ID':
            return [aux.children[0], 'ID']
        
        aux = aux.children[0]
    
    # if aux.name == 'chamada_funcao':
    #     aux2 = no.parent
    #     while len(aux2.children) == 1:
    #         aux2 = aux2.parent

    #     # print(aux2.name)

    #     return [return_leaf(aux2.children[0]), 'chamada_funcao']

    return None


# def get_exp(node):
#     aux = node.parent
#     while aux.name != 'programa':
#         if aux.name == 'expressao':
#             if aux.children[0].name != 'atribuicao':
#                 return node
        
#         aux = aux.parent
    
#     return None


def get_all_vars(root):
    all_vars = list()

    for i in PreOrderIter(root):
        if i.name == 'var':
            var_name = return_leaf(i).name
            if var_name not in all_vars:
                all_vars.append(var_name)

    return all_vars


def get_all_used_vars(root):
    all_vars = list()

    for i in PreOrderIter(root):
        if i.name == 'fator':
            fator = check_fator(i)
            
            if fator:
                var_name = fator[0].name
                if var_name not in all_vars:
                    all_vars.append(var_name)
            # exp = get_exp(i)


            # if exp:
            #     var_name = return_leaf(i).name
            #     print(var_name)
            #     if var_name not in all_vars:
            #         all_vars.append(var_name)

    # for i in PreOrderIter(root):
    #     if i.name == 'var':
    #         exp = get_exp(i)

    #         if exp:
    #             var_name = return_leaf(i).name
    #             print(var_name)
    #             if var_name not in all_vars:
    #                 all_vars.append(var_name)

    return all_vars


def get_poda_leaf_node(node):

    if not node.parent.is_root:
        if len(node.parent.children) == 1:
            return get_poda_leaf_node(node.parent)

    return node


def set_poda_branch(node_leaf, node_parent):
    new_name = node_parent.name.replace(f"{node_parent.name}", f"{node_leaf.name}")
    node_parent.name = new_name
    node_parent.children[0].parent = None


def return_all_leafes(no):
    nodes = [node for node in no.descendants if node.is_leaf]

    for i in nodes:
        node_pai = get_poda_leaf_node(i)
        set_poda_branch(i, node_pai)


    return no


def get_index(node):
    for i in range(len(node.parent.children)):
        if node.parent.children[i] == node:
            return i


def poda_tudo(no):
    nodes = [node for node in no.descendants if node.is_leaf]

    for i in nodes:
        node_pai = i.parent
        new_node = get_poda_leaf_node(i.parent)
        node_position = get_index(new_node)

        if len(node_pai.parent.children) == 1:
            node_pai.parent = None

            children = list(new_node.parent.children)
            children[node_position] = node_pai
            new_node.parent.children = tuple(children)

            new_node.parent = None


    return no


def get_function(node):
    aux = node.parent
    while aux.name != 'programa':
        if aux.name == 'declaracao_funcao':
            return aux.children[1].children[0].name
        
        aux = aux.parent
    
    return 'global'



def fill_symbols_table(tree, st):
    dec_variables = list()
    for i in PreOrderIter(tree):
        if i.name == 'declaracao_variaveis':
            dec_variables.append(i)

    for var in dec_variables:
        tipo = var.children[0].name

        if len(var.children[2].children) > 0:
            v = var.children[2]
            var_name = v.children[0].name
            st.set_escopo(get_function(var), tipo, var_name)

        else:
            var_name = var.children[2].name
            st.set_escopo(get_function(var), tipo, var_name)



    param_variables = list()
    for i in PreOrderIter(tree):
        if i.name == 'parametro':
            param_variables.append(i)

    for var in param_variables:
        tipo = var.children[0].name

        if len(var.children[2].children) > 0:
            pass
            # v = var.children[2]
            # var_name = v.children[0].name
            # st.set_escopo(get_function(var), tipo, var_name)

        else:
            var_name = var.children[2].name
            function_name = var.parent.parent.children[0].name

            check_var_exist = st.var_name_exists(var_name)

            if check_var_exist == '':
                st.add("VAR", var_name, tipo, 0, 1, 0, function_name, 'S', 'N', 0)
            else:
                st.errors.append(['WAR-SEM-VAR-DECL-PREV', var_name, check_var_exist])

            # st.set_escopo(get_function(var), tipo, var_name)


# def fill_used_symbols_table(tree, st):
#     used_vars = list()

#     # for i in PreOrderIter(tree):
#     #     if i.name == 'leia' and len(i.children) != 0:
#     #         used_vars.append(i)

#     for i in PreOrderIter(tree):
#         if i.name == 'var':
#             used_vars.append(i)

    

#     for var in used_vars:
#         st.set_used_var(var)


def fill_ini_symbols_table(tree, st, sft):
    # print("\nATRIBVUICAO\n")
    atr_variables = list()
    for i in PreOrderIter(tree):
        if i.name == 'atribuicao':
            atr_variables.append(i)

    for var in atr_variables:
        st.set_ini_var(var, sft)


    
def verify_function_calls(tree, st, sft):
    chamada_funcoes = list()
    for i in PreOrderIter(tree):
        if i.name == 'chamada_funcao':
            chamada_funcoes.append(i)

    for chamada in chamada_funcoes:
        escopo = get_function(chamada)
        sft.check_funcion_call(chamada, st, escopo)
    

def delete_node(node):
    node.parent = None


def clear_tree(tree):
    for i in PreOrderIter(tree):
        if i.name in [',', '(', ')']:
            delete_node(i)
        
        if i.name in ['vazio', 'leia', 'escreva', 'retorna']:
            if len(i.children) == 0:
                delete_node(i)

def main():

    poda = None
    root, symbols_table, symbols_func_table = tppparser.main()

    if len(sys.argv) < 2:
        raise TypeError(error_handler.newError('ERR-SEM-USE'))

    aux = argv[1].split('.')

    if aux[-1] != 'tpp':
        raise IOError(error_handler.newError('ERR-SEM-NOT-TPP'))
    elif not os.path.exists(argv[1]):
        raise IOError(error_handler.newError('ERR-SEM-FILE-NOT-EXISTS'))
    else:

        vars_root = get_all_vars(root)
        used_vars = get_all_used_vars(root)
        # print(used_vars)

        podado = return_all_leafes(root).root
        podado = poda_tudo(podado).root


        fill_symbols_table(podado, symbols_table)
        # fill_used_symbols_table(podado, symbols_table)
        fill_ini_symbols_table(podado, symbols_table, symbols_func_table)
        verify_function_calls(podado, symbols_table, symbols_func_table)


        symbols_table.set_vars_used(used_vars)
        symbols_table.check_vars_declared(vars_root)

        symbols_func_table.check_func_table(symbols_table)
        symbols_table.check_table(symbols_func_table)

        clear_tree(podado)

        UniqueDotExporter(podado).to_picture(argv[1] + ".unique.ast.png")

        if sys.argv[-1] == '-k':
            symbols_func_table.get_errors(True)
            symbols_table.get_errors(True)

        else:
            print("\n===== TABELA DE FUNCOES =====")
            symbols_func_table.prints()

            print("\n===== TABELA DE SIMBOLOS =====")
            symbols_table.prints()

            print("\n===== WARNINGS & ERRORS =====")
            symbols_func_table.get_errors(False)
            symbols_table.get_errors(False)


# Programa Principal.
if __name__ == "__main__":
    main()
