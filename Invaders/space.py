import curses
import random

def main(scr):
    EKRAN = scr.getmaxyx()
    y = int(EKRAN[0]-2)
    x = int(EKRAN[1] // 2)
    bullet = []
    guard = []
    curses.halfdelay(1)
    inv = []
    bulletInv = []
    player = '__^__'
    
    for n in range(EKRAN[0]-6, EKRAN[0]-2):
            for i in range(8):
                while i < EKRAN[1]:
                    guard.append([n,i])
                    i+=20
    
    for i in range(0, EKRAN[1]):
        inv.append([0,i])

    while True:
        scr.addstr(y,x,player)
        for i in inv:
            scr.addstr(i[0],i[1], 'V')
        for i in bullet:
            scr.addstr(i[0],i[1], '|')
        for i in bulletInv:
            scr.addstr(i[0],i[1], '|')
        for i in guard:
            scr.addstr(i[0],i[1], '#')
        
        z = scr.getch()
        if z == ord('a') and x > 0:
            x-=1
        scr.erase()
        if z == ord('d') and x + len(player) < EKRAN[1]-1:
            x+=1
        scr.erase()

        if z == ord(' '):
            bullet.append([y, x])
            scr.erase()
        
        bulletInv.append(inv[random.randint(0,len(inv)-1)])
        bulletInv = [[i[0]+1,i[1]] for i in bulletInv if i[0] < EKRAN[0]-2]
        bulletInv,guard = [i for i in bulletInv if i not in guard],[i for i in guard if i not in bulletInv]
        
        
        bullet = [[i[0]-1,i[1]] for i in bullet if i[0] > 0]  # если координата Y пули больше нуля, то ее заносим в массив пуль со значением меньше на единицу (стрельба)
        bullet,guard,inv = [i for i in bullet if i not in guard],[i for i in guard if i not in bullet], [i for i in inv if i not in bullet]       # исчезновение пуль при соприкосновении с защитой
        
        for i in bulletInv:
            for n in range(0,len(player)+1):
                if i[0] == y and i[1] == x + n:
                    return

curses.wrapper(main)


