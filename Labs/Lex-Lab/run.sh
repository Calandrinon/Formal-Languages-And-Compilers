lex language_specification.lxi
gcc lex.yy.c -o my_lex -lfl
./my_lex $1
