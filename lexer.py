import enum
from tokentype import *
from tokenn import *
import sys
class Lexer(object):
    def __init__(self,source) -> None:
        self.curPos=-1
        self.curChar=""
        self.source=source+ "\n"
        self.nextChar()
    # Process the next character.
    def nextChar(self):
        self.curPos+=1
        if self.curPos>=len(self.source):
            self.curChar="\0"
        else: self.curChar=self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos+1>=len(self.source):
            return "\0"
        else: return self.source[self.curPos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)
		
       # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

		
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()
    


    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        # operators out of 2 chars are: == >= <= != 
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                secondChar=self.peek()
                token = Token(secondChar + self.curChar, TokenType.EQEQ)
                self.nextChar()
            else:
                token=Token(self.curChar,TokenType.EQ)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
                # Check whether this is token is < or <=
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curChar=='\"':
            self.nextChar()
            startPosition=self.curPos
            while self.curChar!="\"":
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal Chars")
                self.nextChar()
            tokText = self.source[startPosition : self.curPos] # Get the substring.
            token=Token(tokText,TokenType.STRING)
        elif self.curChar.isdigit():
            startPosition=self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # Decimal!
                    self.nextChar()

                # Must have at least one digit after decimal.
                    if not self.peek().isdigit(): 
                    # Error!
                        self.abort("Illegal character in number.")
                    while self.peek().isdigit():
                        self.nextChar()

            deget=self.source[startPosition:self.curPos+1]
            token=Token(deget,TokenType.NUMBER)
        elif self.curChar.isalpha():
            startPosition=self.curPos
            while self.peek().isalnum():
                self.nextChar()
            var=self.source[startPosition:self.curPos+1]
            keyword=Token.checkForKeyWord(var)
            if keyword==None:
                token=Token(var,TokenType.IDENT)
            else:token=Token(var,keyword)
            

            
            


        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)
			
        self.nextChar()
        return token