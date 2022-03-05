import pydirectinput as pdi
from time import sleep
import pyautogui



sprites = {
    'one': {
        'button': 'f1',
        'training': True,
        'collecting': False
    },

    'second': {
        'button': 'f2',
        'training': True,
        'collecting': True
    },

    'third': {
        'button': 'f3',
        'training': False,
        'collecting': True
    }
}



def mouse_click(x, y, amount=1, fast=False):
    pyautogui.moveTo(x, y)

    if not fast:
        sleep(0.5)

    if amount < 1:
        amount = 1
    
    for x in range(amount):
        pdi.mouseDown()
        pdi.mouseUp()

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
        sleep(0.5)



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



def sprite_is_back():
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
        mouse_click(x_detalhes-50, y_detalhes, fast=True) # aba sprite
        mouse_click(x, y, fast=True)



def run():
    for sprite in sprites:
        if sprites[sprite]['training'] or sprites[sprite]['collecting']:
            pdi.press(sprites[sprite]['button'])
            
            if not verify_state():
                sprite_is_back()
                improve_mood()

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