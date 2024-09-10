import tppparser
import subprocess
import os, fnmatch

def execute_test(input_file):
    path_file = 'tests/' + input_file
    process = subprocess.Popen(['python', 'tppparser.py', path_file],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr

    output_file = open(path_file + ".out", "r")

    #read whole file to a string
    expected_output = output_file.read()

    output_file.close()

    print(stdout)
    print(expected_output)

    return stdout.decode("utf-8") == expected_output

def test_001():
    assert execute_test("erro-001.tpp") == True

# Em preparação
