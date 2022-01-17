#!/usr/bin/env python3

from os import listdir

# ~ def ultimo_fichero(DIR, CFG):
    # ~ try:    return open(DIR+'/'+CFG).readlines()[0].rstrip('\n')
    # ~ except: return None

def ficheros_pim(DIR):
    lista = [f for f in listdir(DIR) if f[-7:] == 'PIM.csv']
    return sorted(lista)

class FICHERO:
    def __init__(self, direc: str, nombre: str):
        self.direc = direc
        self.nombre = nombre[:-8]
        self.cargado = False
        self.num_regs = 'sin cargar'
        self.registros = []
        # ~ self.carga()

    def anadir(self, reg):
        if not self.cargado: self.carga()
        self.registros.append(reg)
        with open(self.direc+'/'+self.nombre+'-PIM.csv','w') as fich:
            for reg in sorted(self.registros):
                fich.write(reg + '\n')

    def carga(self):
        # ~ print([l.rstrip('\n') for l in open(self.direc+'/'+self.nombre+'-PIM.csv').read().splitlines()])
        # ~ print(self.direc+'/'+self.nombre+'-PIM.csv')
        try:
            self.registros = sorted([l.rstrip('\n') for l in open(self.direc+'/'+self.nombre+'-PIM.csv').read().splitlines()])
        except:
            exit('Error al cargar')
        self.num_regs = len(self.registros)
        self.cargado = True

    def claves(self) -> list:
        if not self.cargado: self.carga()
        lis = []
        for linea in self.registros:
            lis = lis + [c for c in linea.split('~')[2:]]
        return sorted(list(set(lis)), key=str.lower)

    def get_claves(self) -> list:
        return self.claves()

    def busca_registros(self, item='', en_memo=True, ignora_tilde=False, log_y=True, claves='') -> list:
        pass

    def busca_reg_x_claves(self, claves='') -> list:
        claves_bus = claves.split(',')
        lis = []
        for i in range(len(self.registros)):
            claves_reg = self.registros[i].split('~')[2:]
            hit = True
            for c_bus in claves_bus:
                if c_bus not in claves_reg:
                    hit = False
                    break
            if hit: lis.append(i)
        return sorted([(self.registros[i], i) for i in lis])

