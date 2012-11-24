class YAJP:

    def __init__(self, json):
        self.escapee = {'"': '"', '\\': '\\',
                        '/': '/', 'b': 'b',
                        'f': '\f', 'n': '\n',
                        'r': '\r', 't': '\t'}

        self.json = json
        self.json_length = len(json)
        self.current_pos = 0
        self.current_char = ' '
        self.debug = 'not set'

    def number(self):
        self.debug = 'number'
        # text -> python number
        def text2num(text):
            return float(text[0])*10**float(text[1])
        
        # get all consecutives number digits
        def fetch_num_digits():
            if not '0' <= self.current_char <= '9':
                print '!!!!!!!!!!!!!!!!!', self.current_char
                self.error('NumDigit Failed at:' + str(self.current_pos)+
                           ': ' + self.current_char)
                
            tmp = self.current_char
            print "+++++++++",tmp, "+++++++++++"
            while '0' <= self.next() <= '9':
                tmp += self.current_char
            return tmp

        # [number, exp]
        text = ['', 0]

        # the base number 
        if self.current_char == '-':
            print 'base -> minus'
            text[0] = '-'
            self.debug = 'minus'
            self.next('-')
            self.debug = 'number'
        text[0] += fetch_num_digits()

        if self.current_char == '.':
            print 'base -> .'
            text[0] += '.'
            self.debug = 'float'
            self.next('.')
            self.debug = 'number'
            text[0] += fetch_num_digits()

        # the Exp number if there is 
        if self.current_char.lower() == 'e':
            print 'exp -> all'
            self.next()
            if self.current_char == '+' or self.current_char == '-':
                text[1] = self.current_char
            text[1] += fetch_num_digits()

        self.debug = 'unset in number'
        return text2num(text)

    def string(self):
        self.debug = 'string'
        string = ''
        if not self.current_char == '"': 
            self.error("Bad String at: " + str(self.current_pos))

        while self.next():
            if self.current_char == '"': 
                self.next('"')
                return string

            elif self.current_char == '\\':
                self.next()
                
                if self.current_char == 'u':
                    hex_str = '0x'
                    for i in range(0, 4):
                        hex_str += self.next()
                    string += chr(hex_str)
                elif self.current_char in self.escapee:
                    string += self.escapee[self.current_char]
                else:
                    error("StringEscape Error at :"+ str(self.current_pos)+
                          ": "+ self.current_char)

            else: string += self.current_char

    def object(self):
        self.debug = 'object'
        obj = {}
        if not self.current_char == '{':
            self.error("Bad Object at: "+ str(self.current_pos))

        self.next('{')
        if self.current_char == '}':
            self.next('}')
            return obj

        while self.white():
            key = self.string()
            self.white().next(':')
            obj[key] = self.value()
            if self.white().current_char == '}':
                self.next('}')
                return obj
            self.next(',')

    def array(self):
        self.debug = 'array'
        array = []
        if not self.current_char == '[':
            self.error("Bad Array at: "+ str(self.current_pos))

        if self.next('[').current_char == ']':
            self.next(']')
            return array

        while self.white():
            array.append(self.value())
            self.debug = 'array'
            if self.white().current_char == ']':
                self.next(']')
                return array
            self.next(',')

    def word(self):
        self.debug = 'word'
        if self.current_char == 't':
            self.next('r').next('u').next('e')
            return True
        elif self.current_char == 'f':
            self.next('a').next('l').next('s').next('e')
            return False
        elif self.current_char == 'n':
            self.next('u').next('l').next('l')
            return None
        else:
            self.error('CheckFailAt '+ str(self.current_pos)+ 
                       ': '+ self.current_char)
    
    def next(self,check=None):
        if check and self.current_char != check:
            self.error('CheckFailAt '+ str(self.current_pos)+
                       ': '+ self.current_char +
                       ' check : '+ check + ' method:' +self.debug)

        if self.current_pos == self.json_length:
            self.current_char = None
            return self
        self.current_char = self.json[self.current_pos]
        self.current_pos += 1
        return self

    def white(self):
        while self.current_char == ' ' and self.next() == ' ': continue
        return self

    def value(self):
        self.white()
        ch = self.current_char
        print 'the first char',ch, 'the first pos ', self.current_pos
        if ch == '{': return self.object()
        elif ch == '[': return self.array()
        elif ch == '"': return self.string()
        elif ch == '-': return self.number()
        else: return  self.number() if '0' <= ch <= '9' else self.word()
        # switch =  {'{': self.object,
        #            '[': self.array,
        #            '"': self.string,
        #            '-': self.number}
        # return switch.get(ch, self.number if '0'<=ch<='9' else self.word)()


    def parse(self):
        result = self.value()
        if self.white().current_char is not None :
            self.error('Syntax Error')
        return result
        
    def error(self,m):
        raise RuntimeError(m)


print YAJP('{"a":[1,2,3], "b":"\\t"}').parse()
