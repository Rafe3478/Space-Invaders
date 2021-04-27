import curses
import re

"[*][ ][ ]\n[ ][ ][*]"

def validate_file(z):                              # функция проверяет соответствие вводимых пользователем значений регулярному выражению
    z_1 = z.split('\n')                            # для начала убираем перенос строк, при этом формируя новый список
    z_2 = []                                       # создаем пустой список
    for n in range(len(z_1)):
        z_2.append(len(z_1[n]))
    if not equal_elems(z_2):                       # проверяем длину строк в новом списке, чтобы они были введены пользователем одинаковые
        return False
    for i in z_1:
        if not re.match(r'(\[ \]|\[\*\])+', i):    # проверяет, чтобы значения строк соответствовали введенному наблону
            return False
    return True


def validate_file(z):
    z_1 = z.split('\n')                             # в этом варианте отказались от пустого списка
    if not equal_elems([len(n) for n in z_1]):      # применили сахар
        return False
    for i in z_1:
        if not re.match(r'(\[ \]|\[\*\])+', i):
            return False
    return True


def validate_file(z):
    z_1 = z.split('\n')
    if not equal_elems([len(n) for n in z_1]):
        return False
    return all([not re.match(r'(\[ \]|\[\*\])+', i) for i in z_1])    # применили метод списков all и синтаксический сахар
    
def validate_file(z):
    z_1 = z.split('\n')
    return all(equal_elems([len(n) for n in z_1]))                    # сократили соответствующее описание, но эта строка исполняется всегда и потому не дает работать следующей строке, что требует их объединения
    return all([not re.match(r'(\[ \]|\[\*\])+', i) for i in z_1])
    
def validate_file(z):
    z_1 = z.split('\n')
    return equal_elems([len(n) for n in z_1]) and all([re.match(r'(\[ \]|\[\*\])+$', i) for i in z_1]) # поэтому мы их объединяем
    
    
#equal_elems([2,2,2,2]) -> True
#equal_elems([1,4,1]) -> False

def equal_elems(z):              # проверяет одинаковость всех значений в списоке
    for n in range(len(z)-1):
        if z[n] != z[n+1]:
            return False
    return True






def main(scr):
    global m
    while True:
        scr.addstr(0,0,matrix_to_string(m))
        scr.getch()
        m = next_generation(m)


def print_matrix(m):                   # функция рисует заданную матрицу
    for i in range(len(m)):            # проходит по массиву матрицы
        for n in range (len(m[i])):    # проходит внутри каждого подмассива матрицы
            if m[i][n] == 0:           # сравнивает каждое значение в подмассиве с 0
                print('[ ]', end = '') # выводит заданный рисунок и не переносит строку
            elif m[i][n] == 1:         # сравнивает каждое значение в подмассиве с 1
                print('[*]', end = '') # выводит заданный рисунок и не переносит строку
        print()                        # позволяет пссле окончания малого цикла перенести строку


def matrix_to_string(m):               # функция рисует заданную матрицу
    d = ''                             # в переменной создаем пустую строку
    for i in range(len(m)):            # проходит по массиву матрицы
        for n in range (len(m[i])):    # проходит внутри каждого подмассива матрицы
            if m[i][n] == 0:           # сравнивает каждое значение в подмассиве с 0
                d = d + '[ ]'          # выводит заданный рисунок и не переносит строку
            elif m[i][n] == 1:         # сравнивает каждое значение в подмассиве с 1
                d = d + '[*]'          # выводит заданный рисунок и не переносит строку
        d += '\n'                      # добавляет в строку символ переноса строки
    return d



def matrix_to_string(m):               
    d = '\n'.join ([''.join(['[ ]' if n == 0 else '[*]' for n in i]) for i in m])
    return d

def matrix_to_string(m):               
    return '\n'.join ([''.join([['[ ]','[*]'][n] for n in i]) for i in m])


#[1,0,1,0,0] -> ['[*]','[ ]','[*]',...] -> '[*][ ][*]...'


def get_cell(m,y_1,x_1):                                             # функция присваивает значение 0 при выходе за границы матрицы и действительные значения, если внутри матрицы
    if y_1 > len(m)-1 or y_1 < 0 or x_1 > len(m[y_1])-1 or x_1 < 0:  # при этих условиях происходит выход за пределы матрицы
        return 0                                                     # тогда функция выдает значение 0
    else:
        return m[y_1][x_1]                                           # в противном случае выдает то значение, которое находится в координатах матрицы


def count_neighbours(m,y,x):    # функция считает сумму единиц в клетках, граничащих с заданной клеткой
    return get_cell(m,y+1,x) +\
    get_cell(m,y-1,x) +\
    get_cell(m,y,x+1) +\
    get_cell(m,y,x-1) + \
    get_cell(m,y-1,x-1) +\
    get_cell(m,y-1,x+1) +\
    get_cell(m,y+1,x-1) +\
    get_cell(m,y+1,x+1)
 # функция в итоге взвращает матрицу с конкретными значениями и из заданной точки в её середине. Левая верхняя цифра в матрице имеет координаты 0,0.

# Правила игры:
#в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
#если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
#в противном случае, если соседей меньше двух или больше трёх, клетка умирает («от одиночества» или «от перенаселённости»)

def apply_rule(m,y,x):                      # функция позволяет реализовать правила игры, которые выше (плодиться, выживать или умирать клеткам)
    r = count_neighbours(m,y,x)             # задаем значение в переменную, которое является результатом сложения из предыдущей функции
    if m[y][x] == 0 and r == 3:             # если клетка мертвая (ее значение равно 0) и если соседние клетки в сумме дают 3
        return 1                            # то клетка оживает (ее значение из 0 превращается в 1)
    if m[y][x] == 1 and (r == 2 or r == 3): # r in [2,3] (хакерский вариант) если клетка живая, но вокруг 2 или 3 живые клетки
        return 1                            # то клетка продолжает жить
    else:                                   # в противном случае
        return 0                            # клетка умирает



def next_generation(m):                      функция порождает новую матрицу на основе предыдущей функции
    d = []
    for i in range(len(m)):
        c = []
        for n in range(len(m[i])):
            c.append(apply_rule(m,i,n))
        d.append(c)
    return d



def next_generation(m):               # предыдущая функция в синтаксическом сахаре наполовину
    d = []
    for i in range(len(m)):
        c = [apply_rule(m,i,n) for n in range(len(m))]
        d.append(c)
    return d




def next_generation(m):                 # предыдущая функция в синтаксическом сахаре
    d = [[apply_rule(m,i,n) for n in range(len(m[i]))] for i in range(len(m))]
    return d





#string_to_matrix('[ ][*][ ]\n[ ][ ][*]\n[ ][ ][ ]') -> [[0,1,0],[0,0,1],[0,0,0]]
#-> ['[ ][*][ ]','[ ][ ][*]',...] -> [['[ ]','[*]','[ ]'],...] -> [[0,1,0],...]

def split_3(st):                  # функция разделяет строку на мелкие строки по 3 символа и формирует из них список
    e = []                        # задаем пустой список
    for x in range(0,len(st),3):  # проходим по строке от начала до конца с интервалом в 3 шага
        e.append(st[x:x+3])       # во время итерации выбираем три символа в строке, определяя их по индексам
    return e



def split_3(st):                                      # предыдущая функция в синтаксическом сахаре
    return [st[x:x+3] for x in range(0,len(st),3)]



def string_to_matrix(stroka):
    stroka = [split_3(i) for i in stroka.split('\n')]
    for i in range(len(stroka)):
        for n in range (len(stroka[i])):
            if stroka[i][n] == '[ ]':
                stroka[i][n] = 0
            elif stroka[i][n] == '[*]':
                stroka[i][n] = 1
    return stroka



s = open('life.txt', 'r').read()
validate_file(s)
if not validate_file(s):
    print('Синтаксическая ошибка при вводе в файле')
else:
    m = string_to_matrix(s)
    curses.wrapper(main)





