#!/usr/bin/env python3

from platform import uname
import PySimpleGUI as sg
import pim_backend as m

LETRAS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
          'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
          'y', 'z',)

if uname().node == 'pc1':
    DIR = '/home/atc/PIM'
    A1 = 'Arial 14'
    A2 = 'Courier 16'
    POSICION = (700,300)
    TAMANO = (380,540)
    LISCLAWID=30
    LISLETWID=6
    NOSCROLL = True
elif uname().node == 'patc':
    DIR = '/home/atc/PIM'
    A1 = 'Arial 14'
    A2 = 'Courier 16'
    POSICION = (730,130)
    TAMANO = (380,540)
    LISCLAWID=30
    LISLETWID=6
    NOSCROLL = True
else:
    DIR = '/storage/emulated/0/PIM'
    A1 = 'Arial 12'
    A2 = 'Courier 16'
    POSICION = (0,0)
    TAMANO=(980,1988)
    LISCLAWID=25
    LISLETWID=4
    NOSCROLL = False

CFG = f'{DIR}/PIM.cfg' # guarda el último

# ~ fichero = ''
registros = []
claves = []

def fichero_inicial() -> str:
    try: return open(CFG).readlines()[0].rstrip('\n')
    except: return elige_fichero()

def elige_fichero() -> str:
    ficheros = [f[:-8] for f in m.ficheros_pim(DIR)]
    if not ficheros:
        sg.popup('ERROR', 'No hay ficheros PIM')
        exit()
    layout = [
        [sg.Text('ELIGE FICHERO', justification='center', expand_x=True)],
        [sg.Listbox(values=ficheros, expand_x=True, expand_y=True, enable_events=True)]
    ]
    window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
    event, values = window.read(close=True)
    try: return values[0][0] + '-PIM.csv'
    except: exit()  # si cerro la ventana

# ~ def abre_fichero_inicial():
    # ~ global fichero, registros, claves
    # ~ if not fichero: fichero = m.ultimo_fichero(DIR, CFG)
    # ~ if not fichero: fichero = elige_fichero()
    # ~ if not fichero: exit() # si cancela o escape no devuelve fichero
    # ~ #d.set_background_title("PIM: " + fichero)
    # ~ registros = m.registros_ordenados(DIR, fichero)
    # ~ claves = m.claves_ordenadas(registros)

def menu_a(nombre = ''):
    layout = [
        [sg.Text(nombre, font=A1, justification='center', expand_x=True)],
        [sg.Button('Alta', auto_size_button='yes', font=A1, expand_x=True, expand_y=True)],
        [sg.Button('Buscar', auto_size_button='yes', font=A1, expand_x=True, expand_y=True)],
        [sg.Button('Abrir archivo', auto_size_button='yes', font=A1, expand_x=True, expand_y=True)],
        [sg.Button('Archivo nuevo', auto_size_button='yes', font=A1, expand_x=True, expand_y=True)],
        [sg.Button('Utilidades', auto_size_button='yes', font=A1, expand_x=True, expand_y=True)],
        [sg.Button('Salir', auto_size_button='yes', font=A1, expand_x=True, expand_y=True)],
    ]
    # ~ event, values = sg.Window('PIM', layout, location=POSICION, size=(480, 800)).read()
    window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
    event, values = window.read(close=True)
    return event

def elige_claves(F, claves_pre: str) -> str:
    claves = F.get_claves()
    try: claves.remove('')
    except: pass
    claves_lis = claves
    marcadas = claves_pre.split(',')
    while True:
        layout = [
            [sg.Text('Claves de ' + F.nombre, justification='center', expand_x=True)],
            [sg.B('Todas', expand_x=True), sg.B('Seleccionadas', expand_x=True)],
            [sg.Listbox(claves_lis, font=A1, key='-claves-', default_values=marcadas,
                        enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                        size=LISCLAWID, expand_y=True),
             sg.Listbox(LETRAS, key='letra', font=A2, enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                        size=LISLETWID, expand_y=True, no_scrollbar=True)
            ],
            [sg.B('Cancelar', expand_x=True), sg.B('Nueva', expand_x=True), sg.B('Aceptar', expand_x=True)],
            [sg.B('Salir', expand_x=True)]
        ]
        window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
        while True:
            event, values = window.read()
            marcadas = values['-claves-']
            if event == '-claves-': continue
            else: break
        window.close()
        if event == 'Seleccionadas': claves_lis = marcadas
        elif event == 'Todas': claves_lis = claves
        elif event in (sg.WIN_CLOSED, 'Salir'): exit()
        elif event in (None, 'Cancelar'): return claves_pre
        else: return ','.join(values['-claves-'])  # Aceptar

def elige_registro(lista = []) -> tuple:
    print(lista)
    lis = [l[0].split('~')[0] for l in lista]
    layout = [
        [sg.Text('ELIGE REGISTRO', justification='center', expand_x=True)],
        [sg.Listbox(values=lis, expand_x=True, expand_y=True, enable_events=True)],
        [sg.B(button_text='Cancelar',auto_size_button='no', expand_x=True),
         sg.B(button_text='Salir', auto_size_button='no',expand_x=True)]
    ]
    window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
    event, values = window.read(close=True)
    # ~ if event == 'Cancelar': return 0
    if event == 'Cancelar': return (None, None)
    if event in (None, 'Salir'): exit() # None si cierra ventana
    # ~ return lista[lis.index(values[0][0])][1] + 1 # el 0 es Cancelar
    return lista[lis.index(values[0][0])]

def muestra_registro(reg='', num=None):
    if not reg:
        item = memo = claves = ''
    else:
        # ~ [item,memo] = reg.split('~')[:2]
        # ~ claves = ','.join(reg.split('~')[2:])
        item, memo, *claves = reg.split('~')
        memo = memo.replace(' ^ ','\n')
        claves = ','.join(claves)
    layout = [
        [sg.B(button_text='Borrar',auto_size_button='no',expand_x=True),
         sg.B(button_text='Modificar', auto_size_button='no',expand_x=True),
         sg.B(button_text='Salir', auto_size_button='no',expand_x=True)],
        [sg.InputText(item, key='item', disabled=True,expand_x=True, disabled_readonly_background_color='#ffffcc')],
        [sg.Multiline(memo, key='memo', disabled=True,expand_x=True, expand_y=True, rstrip=True)],
        [sg.Text(claves, key='claves', justification='center', text_color='#000000', background_color='#ffff55', expand_x=True)],
        [sg.B(button_text='Volver',auto_size_button='no',expand_x=True),
         sg.B(button_text='Menu', auto_size_button='no',expand_x=True),
         sg.B(button_text='Buscar', auto_size_button='no',expand_x=True)],
    ]
    window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
    event, values = window.read(close=True)

def buscar(F):
    item = claves = '' # 'clave1,clave2'
    while True:
        layout = [
            [sg.Text('Buscando en ' + F.nombre, justification='center', expand_x=True)],
            # ~ [sg.InputText(focus=True), sg.Button(button_text='Alta',auto_size_button='yes')],
            [sg.Button(button_text='Borrar',auto_size_button='yes'), sg.InputText(item, key='-item-', font=A1, focus=True)],
            [sg.Checkbox('Buscar solo en título', key='-cont-', default=False)],
            [sg.Checkbox('Ignorar acentos, ñ y ç', key='-tilde-', default=False)],
            [sg.B(button_text='Elige claves',auto_size_button='no'), sg.B(button_text='Borrar claves',auto_size_button='no')],
            [sg.Text(claves, key='-claves-', font=A1, enable_events=True, justification='center', text_color='#000000', background_color='#ffff55', expand_x=True)],
            [sg.Text('Tipo de coincidencia', expand_x=True)],
            [sg.Radio('Texto <Y> Claves', "RADIO1", key='-y-', default=True)],
            [sg.Radio('Texto <O> Claves', "RADIO1")],
            [sg.B(button_text='Menu', auto_size_button='no',expand_x=True, expand_y=True),
             sg.B(button_text='Limpiar', auto_size_button='no', expand_x=True, expand_y=True),
             sg.B(button_text='Buscar', auto_size_button='no', expand_x=True, expand_y=True)],
            [sg.B(button_text='Salir', auto_size_button='no',expand_x=True)],
        ]
        window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
        while True:
            event, values = window.read()
            if event == 'Menu':
                window.close()
                return
            if event in (sg.WIN_CLOSED, None, 'Salir'): exit()
            if event == 'Borrar':
                window.Element('-item-').update('')
                continue
            if event in ('Elige claves', '-claves-'):
                item = values['-item-']
                window.close()
                claves = elige_claves(F, claves)
                break
            if event == 'Borrar claves':
                claves = ''
                window.Element('-claves-').update('')
                continue
            if event == 'Limpiar':
                window.Element('-item-').update('')
                claves = ''
                window.Element('-claves-').update('')
            if event == 'Buscar':
                window.close()
                if values['-item-'].strip(' ') != '':
                    hits = F.busca_registros(cad=values['-item-'],
                            solo_titulo=values['-cont-'], ignora_tilde=values['-tilde-'],
                            logic_y=values['-y-'], claves=claves)
                    print(hits)
                else:
                    # ~ num_reg = elige_registro(F.busca_reg_x_claves(claves))
                    reg, num_reg = elige_registro(F.busca_reg_x_claves(claves))
                    if num_reg: muestra_registro(reg, num_reg)
                    else: break

def editar(F, modo, _item='', _memo='', _claves=''):
    item = _item
    memo = _memo
    claves = _claves
    while True:
        layout = [
            [sg.B(button_text='Sustituir', auto_size_button='no', expand_x=True),
             sg.B(button_text='Cancelar',auto_size_button='no', expand_x=True),
             sg.B(button_text='Añadir', auto_size_button='no', expand_x=True)],
            [sg.InputText(item, key='item', expand_x=True, focus=True)],
            [sg.Multiline(memo, key='memo', expand_x=True, expand_y=True, rstrip=True)],
            [sg.Text(claves, key='claves', enable_events=True, justification='center', text_color='#000000', background_color='#ffff55', expand_x=True)],
            [sg.B(button_text='Limpiar\nTítulo',auto_size_button='no', expand_x=True),
             sg.B(button_text='Limpiar\nTexto', auto_size_button='no', expand_x=True),
             sg.B(button_text='Limpiar\nClaves', auto_size_button='no', expand_x=True)],
            [sg.B(button_text='Salir', auto_size_button='no', expand_x=True)],
        ]
        window = sg.Window('PIM', layout, location=POSICION, size=TAMANO)
        while True:
            event, values = window.read()
            if event == 'Cancelar':
                window.close()
                return
            if event in (sg.WIN_CLOSED, None, 'Salir'): exit()
            if event == 'Limpiar\nTítulo':
                window.Element('item').update('')
                continue
            if event == 'Limpiar\nTexto':
                window.Element('memo').update('')
                continue
            if event == 'Limpiar\nClaves':
                claves = ''
                window.Element('claves').update('')
            if event == 'claves':
                item = values['item']
                memo = values['memo']
                window.close()
                claves = elige_claves(F, claves)
                break
            if event == 'Añadir':
                window.close()
                F.anadir(values['item'] + '~' + \
                         values['memo'].replace('\n',' ^ ') + '~' + \
                         claves.replace(',','~'))
                return



def main():
    F = m.FICHERO(DIR, fichero_inicial())
    while True:
        opcion = menu_a(F.nombre + ' (' + str(F.num_regs) + ')')
        if opcion in ('Salir', None): exit()
        if opcion == 'Abrir archivo':
            fichero = elige_fichero()
            F = m.FICHERO(DIR, fichero)
            open('PIM.cfg','w').write(fichero)
            open(CFG,'w').write(fichero)
        if   opcion == 'Buscar': buscar(F)
        elif opcion == 'Alta'  : editar(F, 'alta')

if __name__ == '__main__':
    main()
