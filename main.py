from lexer import *
def main():
    source="LET a=1"
    lexer=Lexer(source)
    while lexer.peek()!='\0':
        print(lexer.curChar)
        lexer.nextChar()
main()
