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

    def graba(self):
        self.registros.sort()
        try:
            with open(self.direc+'/'+self.nombre+'-PIM.csv','w') as fich:
                for reg in self.registros:
                    fich.write(reg + '\n')
            return True
        except:
            return False

    def anadir(self, reg):
        if not self.cargado: self.carga()
        self.registros.append(reg)
        return self.graba()

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

    def destilde(self, _cad):
        # ~ print(_cad)
        cad = _cad.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
        cad =  cad.replace('ñ','n').replace('ç','c').replace('ü','u').replace('º','o').replace('ª','a')
        cad =  cad.replace('¿','?').replace('¡','!')
        # ~ print(cad)
        return cad

    def segun_tilde(self, reg, ignora_tilde):
        if ignora_tilde: return self.destilde(reg)
        return reg

    def claves_en_registro(self, _claves: str, claves_reg: list):
        claves = _claves.split('~')
        for cla in claves:
            if cla not in claves_reg: return False
        return True

    def busca_registros(self, cad='', solo_titulo=False, ignora_tilde=False, logic_y=True, claves='') -> list:
        # ~ print(cad)
        # ~ print(solo_titulo)
        # ~ print(ignora_tilde)
        # ~ print(log_y)
        # ~ print(claves)
        if not self.cargado: self.carga()
        cadena = cad.lower()
        if ignora_tilde: cadena = self.destilde(cadena)
        while ('  ' in cadena): cadena.replace('  ', ' ')
        claves_bus = claves.split(',')
        lis = []
        for i in range(len(self.registros)):
            reg = self.segun_tilde(self.registros[i].lower(), ignora_tilde)
            if solo_titulo:
                if cadena not in reg.split('~')[0]: continue
            else:
                print(cadena)
                print(reg)
                if cadena not in reg: continue
            if claves and logic_y:
                if not self.claves_en_registro(claves, self.registros[i].split('~')[2:]):
                    continue
            lis.append(i)
        return sorted([(self.registros[i], i) for i in lis])

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

    def sustituir(self, num, reg=''):
        self.registros[num] = reg
        return self.graba()

