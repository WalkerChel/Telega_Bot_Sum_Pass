def proverka(par):
    f = par
    try:
        float(f)
    except ValueError:
        return False
    return True

def is_zero_and_neg(k):
    t=float(k)
    if (t <= 0) | (t - int(t) != 0):
        return False
    else:
        return True

def symbols(j):
    uy=['loik']
    aboba='oiuy'
    uy+=[aboba]
    #if len(h)==1:
    #    if len(h[0])==1:
    #        print('ggg')
    #    else:
    #        print('kkk')
    #else:
    #    print(j)
    print(uy)
    print(set(j))
    uy[1]+=[str(set(j))]
    print(uy)

#symbols(str(input('Here')))

