import sys
import os
sys.path.append(os.path.realpath('..'))
from JSON_parser import YAJP


print YAJP('{"a":[1,2,3], "b":"\\t"}').parse()
print YAJP(open('json/test1.json').read()).parse()
