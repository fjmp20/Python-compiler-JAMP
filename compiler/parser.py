class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.match('ID') and self.check('ASSIGN'):
            left = self.previous()
            self.consume('ASSIGN')
            right = self.expression()
            self.consume('END')
            return ('assign', left, right)
        elif self.match('IF'):
            condition = self.expression()
            self.consume('COLON')
            body = self.block()
            if self.match('ELSE'):
                self.consume('COLON')
                else_body = self.block()
                return ('if', condition, body, else_body)
            return ('if', condition, body, None)
        elif self.match('FOR'):
            self.consume('LPAREN')
            variable = self.consume('ID')
            self.consume('IN')
            self.consume('RANGE')
            self.consume('LPAREN')
            start = self.expression()
            self.consume('COMMA')
            end = self.expression()
            self.consume('RPAREN')
            self.consume('RPAREN')
            self.consume('COLON')
            body = self.block()
            return ('for', variable, start, end, body)
        raise RuntimeError(f'Sintaxis inválida en el token {self.peek()}')

    def block(self):
        statements = []
        while not self.check('END') and not self.is_at_end():
            statements.append(self.statement())
        return statements

    def expression(self):
        return self.term()

    def term(self):
        node = self.factor()
        while self.match('OP'):
            op = self.previous()
            right = self.factor()
            node = ('binop', op, node, right)
        return node

    def factor(self):
        if self.match('NUMBER'):
            return self.previous()
        elif self.match('ID'):
            return self.previous()
        elif self.match('QUOTE'):
            string_value = self.string()
            return ('string', string_value)
        elif self.match('LPAREN'):
            node = self.expression()
            self.consume('RPAREN')
            return node
        raise RuntimeError(f'Factor inesperado en el token {self.peek()}')

    def string(self):
        value = []
        while not self.match('QUOTE'):
            value.append(self.advance()[1])
        return ''.join(value)

    def match(self, kind):
        if self.check(kind):
            self.pos += 1
            return True
        return False

    def consume(self, kind):
        if self.check(kind):
            return self.advance()
        raise RuntimeError(f'Token esperado {kind} pero se encontró {self.peek()}')

    def check(self, kind):
        if self.is_at_end():
            return False
        return self.peek()[0] == kind

    def advance(self):
        if not self.is_at_end():
            self.pos += 1
        return self.previous()

    def is_at_end(self):
        return self.pos >= len(self.tokens)

    def peek(self):
        return self.tokens[self.pos]

    def previous(self):
        return self.tokens[self.pos - 1]
