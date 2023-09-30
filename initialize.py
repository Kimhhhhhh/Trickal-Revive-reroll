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

    # 글로벌로 사용할 변수들 모음

    client = AdbClient(host="127.0.0.1", port=5037)

    if len(sys.argv) > 1:
        port = sys.argv[1]
        bluestack = int(sys.argv[2])
    else:
        hwndNum, port = inputValue()
        bluestack = -1

    print("port :", port)
    print("bluestack :", bluestack)

    # 초보자 50뽑 이후 픽업 or 상시로 할지 설정
    pickUp = input('초보자 뽑기 이후 픽업 가차를 진행하시겠습니까? (y/n) : ')
    if pickUp == 'y':
        pickUp = True
    else:
        pickUp = False

    # 사도가 몇개 이상 나올 때 매크로 멈출지 설정
    stopNum = input('사도가 몇개 이상 나올시 중지하시겠습니까? (숫자만 입력) : ')
    stopNum = int(stopNum)

    # ADB 연결, 간혹 권한 문제로 연결이 안될 때가 있음 그럴때 무반응 버그 발생
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

    # 클릭 횟수 저장
    clicknum = {port:0}

    # 가챠 횟수 저장
    gachaNum = 0

    # 현재 매크로 진행 상황
    isTutorialGachaStart = False
    isTutorialGachaEnd = False
    getMail = False
    gachaEnd = False
    isSadoRoom = False
    checkEnd = False

    # 화면 안바뀌는 경우 처리
    noScreenChangeStack = 0

    # 매크로 사이클 시작 시간
    startTime = time()

    # 스크린샷 캐싱용
    screenshot_time = time()
    im = None

    # 매크로 진행상황 리셋, 캐시 클리어 후 콜
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