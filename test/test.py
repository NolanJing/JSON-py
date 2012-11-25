import sys
import os
sys.path.append(os.path.realpath('..'))
from JSON_parser import YAJP


print YAJP('{"a":[1,2,3], "b":"\\t"}').parse()
print '*'*20
print YAJP(open('json/test1.json').read()).parse()
print '*'*20
print YAJP(open('json/test2.json').read()).parse()
print '*'*20
print YAJP(open('json/test3.json').read()).parse()
print '*'*20
print YAJP(open('json/test4.json').read()).parse()
print '*'*20
print YAJP(open('json/test5.json').read()).parse()
