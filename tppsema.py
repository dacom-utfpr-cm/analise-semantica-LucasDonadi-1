import os
import sys
import logging
from sys import argv
from myerror import MyError
from anytree import RenderTree, findall_by_attr, LevelOrderIter
from anytree.exporter import DotExporter, UniqueDotExporter

logging.basicConfig(
     level = logging.DEBUG,
     filename = "sema.log",
     filemode = "w",
     format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()
error_handler = MyError('SemaErrors', showErrorMessage=True)
root = None

variablesError = []

def addVaribleError(name, scope):
    variablesError.append({
        'name': name,
        'scope': scope
    })

def variableHasError(name, scope):
    for variable in variablesError:
        if variable['name'] == name and variable['scope'] == scope:
            return True
    return False

def symbolTable():
    res = findall_by_attr(root, "declaracao")
    variables = []
    for p in res:
        item = [node for pre, fill, node in RenderTree(p)]
        if (item[1].name == "declaracao_variaveis"):
            variable = variableDeclaration(node1=item[1], scope="global")
            if variableIsDeclared(table=variables, name=variable['name'], scope='global'):
                typeVar = getType(table=variables, name=variable['name'], scope='global')
                print(error_handler.newError('WAR-SEM-VAR-DECL-PREV').format(variable['name'], typeVar))
            else:
                variables.append(variable)
        elif (item[1].name == "declaracao_funcao"):
            if item[2].name == "tipo":
                name = item[7].name
                token = item[6].name
                type = item[4].name
                line = item[4].line
            else:
                name = item[4].name
                token = item[3].name
                type = 'vazio'
                line = item[4].line

            variable = {
                "declarationType": 'func',
                "type": type,
                "line": line,
                "token": token,
                "name": name,
                "scope": "global",
                "used": "S" if name == "principal" else "N",
                "dimension": 0,
                "sizeDimension1": 1,
                "sizeDimension2": 0,
                "parameters": parametersDeclaration(item)
            }
            if variableIsDeclared(table=variables, name=name, scope='global'):
                typeVar = getType(table=variables, name=name, scope='global')
                print(error_handler.newError('WAR-SEM-FUNC-DECL-PREV').format(name, typeVar))
            else:
                variables.append(variable)
                functionDeclaration(node1=item[1], scope=name, table=variables)
    return variables






# Programa Principal.
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        raise TypeError(error_handler.newError('ERR-SEM-USE'))

    aux = argv[1].split('.')
    if aux[-1] != 'tpp':
      raise IOError(error_handler.newError('ERR-SEM-NOT-TPP'))
    elif not os.path.exists(argv[1]):
        raise IOError(error_handler.newError('ERR-SEM-FILE-NOT-EXISTS'))
    else:
        data = open(argv[1])
        source_file = data.read()
