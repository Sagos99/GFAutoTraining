from configparser   import ConfigParser
from time           import sleep

import pydirectinput as pdi
import pyautogui



# Carrega o arquivo de configuração
parser = ConfigParser()
parser.read('config.ini', encoding='UTF-8')


sprites = {
    'one': {
        'button': parser['sprite1']['button'],
        'training': True if parser['sprite1']['training'] == 'yes' else False,
        'collecting': True if parser['sprite1']['collecting'] == 'yes' else False
    },

    'second': {
        'button': parser['sprite2']['button'],
        'training': True if parser['sprite2']['training'] == 'yes' else False,
        'collecting': True if parser['sprite2']['collecting'] == 'yes' else False
    },

    'third': {
        'button': parser['sprite3']['button'],
        'training': True if parser['sprite3']['training'] == 'yes' else False,
        'collecting': True if parser['sprite3']['collecting'] == 'yes' else False
    }
}



def mouse_click(x, y, amount=1, fast=False, right=False):
    pyautogui.moveTo(x, y)

    if not fast:
        sleep(0.5)

    if amount < 1:
        amount = 1
    
    for x in range(amount):
        if not right:
            pdi.mouseDown(button='left')
            pdi.mouseUp(button='left')
        else:
            pdi.mouseDown(button='right')
            pdi.mouseUp(button='right')

    if not fast:
        sleep(0.2)



def click_button_ok(button):
    try:
        x, y = pyautogui.locateCenterOnScreen('img/button_Ok2.png', confidence=0.8)
    except:
        x, y = None, None

    if x and y:
        mouse_click(x-35, y)

        pdi.press(button)
        sleep(0.3)
        pdi.press(button)



def improve_mood():
    try:
        x, y = pyautogui.locateCenterOnScreen('img/button_batepapo.png', confidence=0.8)
    except:
        x, y = None, None

    if x and y:
        mouse_click(x, y, amount=10)



def go_training():
    sleep(0.5)

    try:
        x, y = pyautogui.locateCenterOnScreen('img/button_Treinar.png', confidence=0.8)
    except:
        x, y = None, None

    if x and y:
        mouse_click(x, y)
        sleep(0.1)



def go_collecting():
    sleep(0.5)

    try:
        x, y = pyautogui.locateCenterOnScreen('img/button_Coletar.png', confidence=0.8)
    except:
        x, y = None, None

    if x and y:
        mouse_click(x, y)
        sleep(0.1)



def verify_state():
    sleep(0.5)
    states = [
        'state_Cacando',
        'state_Colhendo',
        'state_Minerando',
        'state_Treinando'
    ]

    for state in states:
        try:
            x, y = pyautogui.locateCenterOnScreen(f'img/{state}.png', confidence=0.8)
        except:
            x, y = None, None

        if x and y:
            return True

    return False



def verify_energy():
    try:
        x, y = pyautogui.locateCenterOnScreen('img/resistencia.png', confidence=0.9)
    except:
        x, y = None, None

    if x and y:
        return True
    else:
        return False



def verify_mood():
    humor_atual = None
    humor_setado = f'humor_{parser["geral"]["humor"].lower()}'

    humores = {
        'humor_feliz'       : 4,
        'humor_alegre'      : 3,
        'humor_normal'      : 2,
        'humor_triste'      : 1,
        'humor_depressivo'  : 0
    }

    for humor in humores:
        try:
            x, y = pyautogui.locateCenterOnScreen(f'img/{humor}.png', confidence=0.8)
            humor_atual = humor
            break
        except:
            x, y = None, None

    if x and y:
        if humores[humor_atual] <= humores[humor_setado]:
            return True
    
    return False



def use_item(sprite_button, item):
    pdi.press(parser['geral']['bag_button'])

    try:
        x_item, y_item = pyautogui.locateCenterOnScreen(f'img/{item}.png', confidence=0.8)
    except:
        x_item, y_item = None, None

    if x_item and y_item:
        mouse_click(x_item, y_item, right=True)
        pdi.press(sprite_button)

    pdi.press(parser['geral']['bag_button'])



def sprite_is_back():
    need_cookie = False
    sleep(3)

    try:
        x, y = pyautogui.locateCenterOnScreen('img/button_Ok.png', confidence=0.8)
        x_detalhes, y_detalhes = pyautogui.locateCenterOnScreen('img/button_Detalhes.png', confidence=0.8)
    except:
        x, y = None, None
        x_detalhes, y_detalhes = None, None

    if x and y:
        mouse_click(x, y, fast=True)
        mouse_click(x_detalhes, y_detalhes, fast=True)
        need_cookie = verify_energy()
        mouse_click(x_detalhes-50, y_detalhes, fast=True) # aba sprite
        mouse_click(x, y, fast=True)

    return need_cookie



def run():
    for sprite in sprites:
        if sprites[sprite]['training'] or sprites[sprite]['collecting']:
            pdi.press(sprites[sprite]['button'])
            
            if not verify_state():
                need_cookie = sprite_is_back()
                improve_mood()

                if sprite != 'one':
                    need_soda = verify_mood()

                    if need_soda:
                        use_item(sprites[sprite]['button'], 'item_refri')

                    if need_cookie:
                        if need_soda:
                            sleep(5)

                        use_item(sprites[sprite]['button'], 'item_biscoito')

                if sprites[sprite]['training']:
                    go_training()
                    click_button_ok(sprites[sprite]['button'])
                if sprites[sprite]['collecting']:
                    go_collecting()
                    click_button_ok(sprites[sprite]['button'])

            pdi.press(sprites[sprite]['button'])
            sleep(0.5)



sleep(5)
while True:
    run()