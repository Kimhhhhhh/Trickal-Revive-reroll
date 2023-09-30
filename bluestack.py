import win32gui, win32ui, win32con
import pyautogui
from initialize import Macro
from time import sleep, time
from PIL import Image

# 이미지 인식 제외, 윈도우 핸들 or ADB 사용한 블루스택 조작 관련 함수들 모음

# 이미지 유사도 검색, 좌표 반환
def search(destPath, originImg, confidence=0.8):
    result = pyautogui.locate(destPath, originImg, confidence=confidence)
    if result == None:
        return None
    result = (result.left + result.width/2, result.top + result.height/2)
    x, y = map(int, result)
    return x, y

# 블루스택 hwnd 찾고 창 크기 변환
def resizeBluestack(bluestack, width=1280, height=735):
    if bluestack == 0:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player')
    elif bluestack == -1:
        hwnd = Macro.hwndNum
    else:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player {bluestack}')

    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    win32gui.MoveWindow(hwnd, x0, y0, width, height, True)

# 블루스택 hwnd 찾고 비활성 스크린샷
# 이미지를 캐싱해서 최적화. 0.05초에 한번씩 캐싱 width, height 하드코딩 되어있음
def background_screenshot(bluestack):
    if bluestack == 0:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player')
    elif bluestack == -1:
        hwnd = Macro.hwndNum
    else:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player {bluestack}')
    
    width = 1280
    height = 735
    
    if time() - Macro.screenshot_time > 0.05:
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)
        Macro.im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        Macro.screenshot_time = time()

    return Macro.im

# ADB로 꾹 누르기 명령
def press(x, y, port, time=10):
    cmd = "input swipe " + str(x) + " " + str(y) + " " + str(x) + " " + str(y) + " " + str(time)
    devices = Macro.client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

# adb 키 타이핑
def typing(text, port):
    cmd = "input text " + text
    devices = Macro.client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

# adb 키 이벤트
# https://developer.android.com/reference/android/view/KeyEvent 참조
def keyevent(key, port):
    cmd = "input keyevent " + str(key)
    devices = Macro.client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

# adb 클릭, 클릭횟수 카운트
def click(x, y, port):
    cmd = "input touchscreen tap " + str(x) + " " + str(y)
    devices = Macro.client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            Macro.clicknum[port] += 1
            break

# adb 스와이프
def swipe(x1, y1, x2, y2, port, time=10):
    cmd = "input swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(time)
    devices = Macro.client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

# 특정 이미지가 나올때까지 대기. 기본 Timeout은 2초 나오면 True 반환
def imageWait(imgPath, bluestack, timeout=2, confidence=0.8):
    startTime = time()
    imgPath = 'img/' + imgPath + '.png'

    while True:
        try:
            im = background_screenshot(bluestack)
            result = search(imgPath, im, confidence)
            if result != None:
                sleep(0.3)
                return True
            
            if time() - startTime > timeout:
                return False
        except win32ui.error:
            print('imageWait error')
            

# 모든 앱 끄기
def clearApp(port):
    keyevent('KEYCODE_APP_SWITCH', port)
    sleep(2)
    keyevent('KEYCODE_DEL', port)

# 홈 화면 이동 -> 어플 시작
def startApp(port, bluestack):
    keyevent(3, port)
    sleep(0.5)
    result = search('img/homestart.png', background_screenshot(bluestack), 0.8)

    if result == None:
        return

    x, y = result
    click(x, y, port)
    print('homestart Click')

# 모든 앱 끄고 -> 홈 화면 이동 -> 어플 시작
def restartApp(port, bluestack):
    clearApp(port)
    sleep(0.5)
    startApp(port, bluestack)