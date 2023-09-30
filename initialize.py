from ppadb.client import Client as AdbClient
from time import time
import os
import sys
import win32gui

def getWindowList():
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            hwnd_list.append((title, hwnd))
        return True
    output = []
    win32gui.EnumWindows(callback, output)
    return output

def inputValue():
    windowList = getWindowList()
    for i, window in enumerate(windowList):
        print(f'[{i}]', window)
    print('=============================')
    hwndNum = input('매크로를 실행시킬 블루스택 App Player의 번호를 입력해주세요. (숫자만 입력) : ')
    hwndNum = windowList[int(hwndNum)][1]
    print('=============================')
    port = input('ADB 포트번호를 입력해주세요. (숫자만 입력) : ')

    return hwndNum , port

class Macro:

    # 글로벌로 

    client = AdbClient(host="127.0.0.1", port=5037)

    if len(sys.argv) > 1:
        port = sys.argv[1]
        bluestack = int(sys.argv[2])
    else:
        hwndNum, port = inputValue()
        bluestack = -1

    print("port :", port)
    print("bluestack :", bluestack)

    pickUp = input('초보자 뽑기 이후 픽업 가차를 진행하시겠습니까? (y/n) : ')
    if pickUp == 'y':
        pickUp = True
    else:
        pickUp = False

    stopNum = input('사도가 몇개 이상 나올시 중지하시겠습니까? (숫자만 입력) : ')
    stopNum = int(stopNum)

    os.system(f'adb connect 127.0.0.1:{port}')

    connectSuccess = False
    print('Device List')
    for i, device in enumerate(client.devices()):
        print(f"[{i}] {device.serial}")
        if device.serial.split(':')[1] == port:
            print('Device Connect Success')
            connectSuccess = True
            break

    if not connectSuccess:
        print(f'ADB가 연결되지 않았습니다. 관리자 권한으로 cmd를 열고 adb connect 127.0.0.1:{port} 를 입력해주세요.')
        exit()

    clicknum = {port:0}
    gachaNum = 0

    isTutorialGachaStart = False
    isTutorialGachaEnd = False
    getMail = False
    gachaEnd = False
    isSadoRoom = False
    checkEnd = False
    noScreenChangeStack = 0
    startTime = time()
    screenshot_time = time()
    im = None

    def reset():
        Macro.isTutorialGachaStart = False
        Macro.isTutorialGachaEnd = False
        Macro.getMail = False
        Macro.gachaEnd = False
        Macro.isSadoRoom = False
        Macro.checkEnd = False
        Macro.gachaNum = 0
        Macro.startTime = time()
        Macro.screenshot_time = time()