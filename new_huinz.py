x=100
f = open('out1.txt', 'a')

def get_value(x):
    y = (((1) / ((1) / (x) - 0.045)) / (x) - 1)*100+0.1
    if y<9.1:
        y=9.1
    if x>=1.5 and x<1.75:
        y=10
    elif x>=1.75 and x<2.0:
        y=y+1.5
    elif x>=2.0 and x<3.0:
        y=y+2.0
    elif x>=3.0 and x<4.0:
        y=y+2.5
    elif x>=4.0 and x<5.0:
        y=y+3.0
    elif x>=5.0:
        y=y+4.0
    return float(toFixed(y, 2))

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

while x<600:
    y=get_value(x/100)
    f.write(str(x/100) + " -> " + str(y)  +"\n")
    print(str(x/100) + " -> " + str(y))
    x = x + 15
f.close()