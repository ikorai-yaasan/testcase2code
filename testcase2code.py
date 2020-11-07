import csv
import sys
import argparse
import pathlib


def _BLOCK_START():
    print("{")

def _BLOCK_END():
    print("}")

def _TESTCASE(num):
    print("    TESTCASE({0});".format(num))

def _SET_TESTCONDITION(attr, val):
    print ("    SETUP_{0: <16}( {1: <16} );".format(attr.upper(), _ENUM_VAL_STR(attr, val)))

def _CHECK_CODE():
    print ("    CHECK_RESULT;")        

def _ENUM_START():
    print("typedef enum {")

def _ENUM_STR(attr):
    return "TEST_{0}".format(attr.upper())

def _ENUM_VAL_STR(attr, val):
    return "{0}_{1}".format(_ENUM_STR(attr), val.upper())

def _ENUM_VAL_DEF(attr, val):
    print("    {0: <32},".format(_ENUM_VAL_STR(attr, val)))

def _ENUM_END(attr):
    print("}} {0};".format(_ENUM_STR(attr)))

def _SETUP_FUNCTION(attr, vals):
    print("PRIVATE VOID SETUP_TEST_{0} ( {1} val )".format(attr.upper(), _ENUM_STR(attr)))
    _BLOCK_START()
    print("    switch (val) {")
    for val in vals :
        print("        case {0: <32} :".format(_ENUM_VAL_STR(attr, val)))
        print("            setup code")
        print("            break;")
    print("        default :")
    print("            break;")
    print("    }")
    _BLOCK_END()


parser = argparse.ArgumentParser()
parser.add_argument('testcase', default="testcase.csv")
args = parser.parse_args()

st = pathlib.PurePath(args.testcase).stem

try :
    f_csv = open(args.testcase)
except OSError as err:
    print(err)

print(st+'.c')

try :
    f_c = open(st+'.c', mode='w')
except OSError as err:
    print(err)


dataset = [data for data in csv.DictReader(f_csv, delimiter='\t')]
keys = [key for key in dataset[0].keys()]

sys.stdout = f_c

print("")
print("/* ***********************")
print(" * define enum ")
print(" * **********************/")
for key in keys :
    print("")
    vals = list(set([data[key] for data in dataset]))
    _ENUM_START()
    for val in vals :
        _ENUM_VAL_DEF(key, val)
    _ENUM_END(key)

print("")
print("/* ***********************")
print(" * setup function ")
print(" * **********************/")
for key in keys :
    print("")
    vals = list(set([data[key] for data in dataset]))
    _SETUP_FUNCTION(key, vals)

print("")
print("/* ***********************")
print(" * test case ")
print(" * **********************/")
casenum = 1
for data in dataset :
    print("")
    _BLOCK_START()
    _TESTCASE(casenum)
    for key in data.keys():
        _SET_TESTCONDITION(key, data[key])
    _CHECK_CODE()
    _BLOCK_END()
    casenum += 1

print("")

f_csv.close()
f_c.close()


