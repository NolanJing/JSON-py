class YAJP:

    def __init__(self, json):
        self.escapee = {'"': '"', '\\': '\\',
                        '/': '/', 'b': 'b',
                        'f': '\f', 'n': '\n',
                        'r': '\r', 't': '\t'}

        self.END = 'END'
        self.json = json
        self.json_length = len(json)
        self.current_pos = 0
        self.current_char = ' '


    # parse number 
    def number(self):
        # text -> python number
        def text2num(text):
            return float(text[0])*10**float(text[1])
        
        # get all consecutives number digits
        def fetch_num_digits():
            if not '0' <= self.current_char <= '9':
                self.error('NumDigit Failed at:' + str(self.current_pos)+
                           ': ' + self.current_char)
                
            tmp = self.current_char
            while '0' <= self.next() <= '9':
                tmp += self.current_char
            return tmp

        # [number, exp]
        text = ['', 0]

        # the base number 
        if self.current_char == '-':
            text[0] = '-'
            self.next('-')
        text[0] += fetch_num_digits()

        if self.current_char == '.':
            text[0] += '.'
            self.next('.')
            text[0] += fetch_num_digits()

        # the Exp number if there is 
        if self.current_char.lower() == 'e':
            self.next()
            if self.current_char == '+' or self.current_char == '-':
                text[1] = self.current_char
            text[1] += fetch_num_digits()

        return text2num(text)

    # parse string
    def string(self):
        string = ''
        if not self.current_char == '"':
            self.error("Bad String at: " + str(self.current_pos))

        while self.next():
            if self.current_char == '"': 
                self.next('"')
                return string

            # special character
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

    # parse object
    def object(self):
        obj = {}
        if self.next('{').current_char == '}':
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

    # parse array
    def array(self):
        array = []
        if self.next('[').current_char == ']':
            self.next(']')
            return array

        while self.white():
            array.append(self.value())
            if self.white().current_char == ']':
                self.next(']')
                return array
            self.next(',')


    # parse JSON word
    def word(self):
        # true -> True
        if self.current_char == 't':
            self.next('r').next('u').next('e')
            return True
        # false -> False
        elif self.current_char == 'f':
            self.next('a').next('l').next('s').next('e')
            return False
        # null -> None
        elif self.current_char == 'n':
            self.next('u').next('l').next('l')
            return None
        else:
            self.error('CheckFailAt '+ str(self.current_pos)+ 
                       ': '+ self.current_char)


    # Assign next char to current_char.
    # If check is set, 
    # that means the current_char should equal to the check.
    # First do the checking then Update the current_char
    def next(self,check=None):
        if check and self.current_char != check:
            self.error('CheckFailAt '+ str(self.current_pos)+
                       ': '+ self.current_char +'check : '+ check)

        if self.current_pos == self.json_length:
            self.current_char = self.END
            return self
        self.current_char = self.json[self.current_pos]
        self.current_pos += 1

        # RETURN self, so it can cascade
        return self


    # Find the first not-whitespace character.
    def white(self):
        while self.current_char <= ' ' and self.next() <= ' ': continue
        # RETURN self, so it can cascade
        return self


    # Get the value of a JSON string
    def value(self):
        self.white()
        ch = self.current_char
        if ch == '{': return self.object()
        elif ch == '[': return self.array()
        elif ch == '"': return self.string()
        elif ch == '-': return self.number()
        else: return  self.number() if '0' <= ch <= '9' else self.word()

        ##################################################
        # WHY the following code won't work?             #
        # If you see this, Please help me figure it out. #
        # Any help will be highly appreciated            #
        ##################################################
        # switch =  {'{': self.object,
        #            '[': self.array,
        #            '"': self.string,
        #            '-': self.number}
        # return switch.get(ch, self.number if '0'<=ch<='9' else self.word)()


    # The only public method that parse the JSON object
    # to python Dictionary or Array
    def parse(self):
        result = self.value()
        if not self.white().current_char == self.END:
            self.error('Syntax Error')
        return result


    # Error Handler
    def error(self,m):
        raise RuntimeError(m)


