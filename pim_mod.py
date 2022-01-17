#!/usr/bin/env python3

from os import listdir

def ultimo_fichero(DIR, CFG):
    try:
        return open(DIR+'/'+CFG).readlines()[0].rstrip('\n')
    except:
        return None

def ficheros_pim(DIR):
    lista = [f for f in listdir(DIR) if f[-7:] == 'PIM.csv']
    return sorted(lista)

def registros_ordenados(DIR, FICHERO):
    regs = [l.rstrip('\n') for l in open(DIR+'/'+FICHERO).read().splitlines()]
    return sorted(regs, key=str.lower)

def claves_ordenadas(lista):
    lis = []
    for linea in lista:
        lis = lis + [c for c in linea.split('~')[2:]]
    return sorted(list(set(lis)), key=str.lower)

def inserta_claves(claves, nuevas=[]):
    for c in nuevas:
        if not c in claves: claves.append(c)
    return sorted(claves)

def busca_registros(cad, memo, claves, regs):
    hits = []
    while ('  ' in cad): cad.replace('  ', ' ')
    if (cad == ' '):
        hits = regs
    else:
        for r in regs:
            if (cad in r.lower()): hits.append(r)
    #if (not claves): return hits
    if (not claves): return sorted([h.split('~')[0] for h in hits])
    hitsk = []
    for h in hits:
        hit = True
        for k in claves:
            if (not '~'+k.lower() in h.lower()): hit = False
        if (hit): hitsk.append(h)
    #return hitsk
    return sorted([h.split('~')[0] for h in hitsk])

def busca_registro_por_titulo(tit, regs):
    for r in regs:
        if tit == r.split('~')[0]:
            return r

def borrar_por_titulos(direc, fich, regs, tits):
    regs.sort()
    titulos = [t.split('~')[0] for t in regs]
    tits.sort(reverse=True) # importante
    for t in tits:
        i = titulos.index(t)
        regs.pop(i)
    F = open(direc + '/' + fich,'w')
    for r in regs: F.write(r + '\n')
    F.close()

def main():
    pass

if __name__ == '__main__':
    main()
