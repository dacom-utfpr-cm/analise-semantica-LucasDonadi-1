import tpplex
import subprocess
import shlex
import os, fnmatch

def execute_test(input_file, args):
    if(input_file != ''):
        path_file = 'tests/' + input_file
    else:
        path_file = ""
    
    # Por algum motivo quando passava input_file = "" o pytest passava um nome de arquivo e dava o erro:
    # b'ERR-LEX-NOT-TPP\n'
    # Expected output:
    # ERR-LEX-USE
    # process = subprocess.Popen(['python', 'tpplex.py', args, path_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "python tpplex.py {0} {1}".format(args, path_file)
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    stdout, stderr

    path_file = 'tests/' + input_file
    output_file = open(path_file + ".out", "r")

    #read whole file to a string
    expected_output = output_file.read()

    output_file.close()

    print("Generated output:")
    print(stdout)
    print("Expected output:")
    print(expected_output)

    return stdout.decode("utf-8") == expected_output

#def testes():
#    for file in fnmatch.filter(os.listdir('tests'), '*.tpp'):
#        assert execute_test(file) == True

def test_001():
    assert execute_test("", "-k") == True

def test_002():
    assert execute_test("teste.c", "-k") == True

def test_003():
    assert execute_test("notexist.tpp", "-k") == True

def test_004():
    assert execute_test("teste-001.tpp", "-k") == True

def test_005():
    assert execute_test("teste-002.tpp", "-k") == True

def test_006():
    assert execute_test("teste-003.tpp", "-k") == True

def test_007():
    assert execute_test("teste-004.tpp", "-k") == True

def test_008():
    assert execute_test("teste-005.tpp", "-k") == True

def test_009():
    assert execute_test("bubble_sort_2.tpp", "-k") == True

def test_010():
    assert execute_test("bubble_sort.tpp", "-k") == True

def test_011():
    assert execute_test("Busca_Linear_1061992.tpp", "-k") == True

def test_012():
    assert execute_test("buscaLinear-2020-2.tpp", "-k") == True

def test_013():
    assert execute_test("comp.tpp", "-k") == True

def test_014():
    assert execute_test("fatorial-2020-2.tpp", "-k") == True

def test_015():
    assert execute_test("fatorial.tpp", "-k") == True

def test_016():
    assert execute_test("fat.tpp", "-k") == True

def test_017():
    assert execute_test("fibonacci-2020-2.tpp", "-k") == True

def test_018():
    assert execute_test("fibonacci.tpp", "-k") == True

def test_019():
    assert execute_test("hanoi-2020-2.tpp", "-k") == True

def test_020():
    assert execute_test("insertionSort-2020-2.tpp", "-k") == True

def test_021():
    assert execute_test("insertSort-2020-2.tpp", "-k") == True

def test_022():
    assert execute_test("maiorDoVetor.tpp", "-k") == True

def test_023():
    assert execute_test("multiplicavetor.tpp", "-k") == True

def test_024():
    assert execute_test("operacao_vetor-2020-2.tpp", "-k") == True

def test_025():
    assert execute_test("paraBinario-2020-2.tpp", "-k") == True

def test_026():
    assert execute_test("primo.tpp", "-k") == True

def test_027():
    assert execute_test("produtoEscalar.tpp", "-k") == True

def test_028():
    assert execute_test("prog_test.tpp", "-k") == True

def test_029():
    assert execute_test("sample.tpp", "-k") == True

def test_030():
    assert execute_test("selectionSort-2020-2.tpp", "-k") == True

def test_031():
    assert execute_test("selectionsort.tpp", "-k") == True

def test_032():
    assert execute_test("soma_maior_que_3.tpp", "-k") == True

def test_033():
    assert execute_test("somavet.tpp", "-k") == True

def test_034():
    assert execute_test("subtraiVetores.tpp", "-k") == True

def test_035():
    assert execute_test("verifica_valor_10.tpp", "-k") == True

def test_036():
    assert execute_test("verif_num_negativo.tpp", "-k") == True

def test_037():
    assert execute_test("bubble_sort-2020-2.tpp", "-k") == True
