import subprocess
from ppadb.client import Client as AdbClient
from time import sleep, time
from PIL import Image
import pyautogui
import win32gui
import win32con
import win32ui
import os
import pytesseract
import sys

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
client = AdbClient(host="127.0.0.1", port=5037)

if len(sys.argv) > 1:
    port = sys.argv[1]
    bluestack = sys.argv[2]
else:
    port = '5555'
    bluestack = 0

os.system(f'adb connect 127.0.0.1:{port}')
clicknum = {port:0}
gachaNum = 0

def search(destPath, originImg, confidence=0.8):
    result = pyautogui.locate(destPath, originImg, confidence=confidence)
    if result == None:
        return None
    result = (result.left + result.width/2, result.top + result.height/2)
    x, y = map(int, result)
    return x, y

def resizeBluestack(bluestack, width=1280, height=735):
    if bluestack == 0:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player')
    else:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player {bluestack}')

    x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
    win32gui.MoveWindow(hwnd, x0, y0, width, height, True)

def background_screenshot(bluestack):
    if bluestack == 0:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player')
    else:
        hwnd = win32gui.FindWindow(None, f'BlueStacks App Player {bluestack}')
    
    width = 1280
    height = 735
    
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    bmpinfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)
    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return im

def press(x, y, port, time=10):
    cmd = "input swipe " + str(x) + " " + str(y) + " " + str(x) + " " + str(y) + " " + str(time)
    devices = client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

def typing(text, port):
    cmd = "input text " + text
    devices = client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

def keyevent(key, port):
    cmd = "input keyevent " + str(key)
    devices = client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break

def click(x, y, port):
    cmd = "input touchscreen tap " + str(x) + " " + str(y)
    devices = client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            clicknum[port] += 1
            break

def swipe(x1, y1, x2, y2, port, time=10):
    cmd = "input swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(time)
    devices = client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd)
            break
    
def imageWait(imgPath, bluestack, timeout=2, confidence=0.8):
    startTime = time()
    imgPath = 'img/' + imgPath + '.png'

    while True:
        try:
            im = background_screenshot(bluestack)
            result = search(imgPath, im, confidence)
            if result != None:
                return True
            
            if time() - startTime > timeout:
                return False
        except win32ui.error:
            print('imageWait error')
            
    
def getScreen(port):
    cmd1 = 'screencap -p /sdcard/screen.png'
    cmd2 = f'adb -s 127.0.0.1:{port} pull /sdcard/screen.png'

    devices = client.devices()
    for device in devices:
        if device.serial.split(':')[1] == port:
            device.shell(cmd1)
            subprocess.call(cmd2, shell=True)
            im = Image.open('screen.png')
            return im
        
def clearApp(port):
    keyevent('KEYCODE_APP_SWITCH', port)
    sleep(2)
    keyevent('KEYCODE_DEL', port)

def startApp(port, bluestack):
    keyevent(3, port)
    sleep(0.5)
    result = search('img/homestart.png', background_screenshot(bluestack), 0.8)

    if result == None:
        return

    x, y = result
    click(x, y, port)
    print('homestart Click')

def restartApp(port, bluestack):
    clearApp(port)
    sleep(0.5)
    startApp(port, bluestack)

def ocr():
    coords = [(100, 350, 170, 380),
            (300, 350, 370, 380),
            (490, 350, 560, 380),
            (690, 350, 760, 380),
            (890, 350, 960, 380),
            (1090, 350, 1160, 380),
            (100, 560, 170, 590),
            (300, 560, 370, 590),
            (490, 560, 560, 590),
            (690, 560, 760, 590),
            (890, 560, 960, 590),
            (1090, 560, 1160, 590)]

    lst = []
    for i in coords:
        img = cropimage(background_screenshot(0), i[0], i[1], i[2], i[3])
        try:
            lst.append(int(pytesseract.image_to_string(img, config="--psm 7 digits").replace('.', '').replace(',', '').replace('\n', '')))
        except:
            pass


    return lst

def cropimage(img, x1, y1, x2, y2):
    img = img.crop((x1, y1+22, x2, y2+22))
    return img
def terms(port, bluestack):
    coords = search('img/terms.png' ,background_screenshot(bluestack))
    if not coords:
        return False

    click(727,626, port)
    print(f"약관 {int(time()-startTime)}s {port}")

def guest_login_1(port, bluestack):
    coords = search('img/guest_login_1.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(631, 449, port)

def guest_login_2(port, bluestack):
    coords = search('img/guest_login_2.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1499, 1096, port)

def jab(port, bluestack):
    coords = search('img/jab.png' ,background_screenshot(bluestack), 0.5)
    if not coords:
        return False
    
    click(559, 416, port)
    click(745, 311, port)
    click(804, 499, port)
    print(f'볼잡기 {int(time()-startTime)}s {port}')

def naming(port, bluestack, name='temp'):
    coords = search('img/naming.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(662, 348, port)                                       
    typing(name, port)
    sleep(0.8)
    click(665, 522, port)
    click(665, 522, port)
    print(f'이름 {int(time()-startTime)}s {port}')

def ok(port, bluestack):
    coords = search('img/ok.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(coords[0], coords[1], port)

def arrow(port, bluestack):
    target = ['arrow2', 'arrow4', 'arrow5', 'arrow6', 'arrow8', 'arrow9']

    for i in target:
        coords = search(f'img/{i}.png' ,background_screenshot(bluestack), confidence=0.7)
        if coords:            
            click(631, 618, port)
            click(771, 651, port)
            click(644, 246, port)
            click(951, 115, port)
            click(540, 651, port)
            click(1234, 355, port) # 전투다음

            return

def youngchoon(port, bluestack):
    target = ['youngchoon', 'youngchoon2', 'youngchoon3']

    for i in target:
        coords = search(f'img/{i}.png' ,background_screenshot(bluestack), confidence=0.8)
        if coords:
            click(1154,601, port) # 모험
            click(1173,423, port) # 1-1
            click(618,573, port) # 마고
            click(847, 538, port) # 빨간애
            click(719, 688, port) # 마지막나가기
            click(945, 493, port) # 빈자리

            return
        

def universal(port, bluestack):
    arrow(port, bluestack)
    ok(port,bluestack)
    youngchoon(port,bluestack)

def go(port, bluestack):
    coords = search('img/go.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1020, 667, port)

def nextstage(port, bluestack):
    coords = search('img/nextstage.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1140, 458, port)
    click(1140, 657, port)

def eventstage(port, bluestack):
    coords = search('img/eventstage.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1140, 657, port)

def thirdstage(port, bluestack):
    coords = search('img/thirdstage.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(644, 451, port)

def selectdeck(port, bluestack):
    coords = search('img/selectdeck.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1148, 563, port)

def timefast(port, bluestack):
    coords = search('img/timefast.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1167, 38, port)
    print(f'배속 {int(time()-startTime)}s {port}')
    
def lock(port, bluestack):
    coords = search('img/lock.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(369, 675, port)
    print(f'lock {int(time()-startTime)}s {port}')

def gacha(port, bluestack):
    coords = search('img/gacha.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(66, 658, port)

def gacha_1(port, bluestack):
    coords = search('img/gacha_1.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1172, 658, port)

def gacha2(port, bluestack):
    pass
    # coords = search('img/check_gacha_end.png' ,background_screenshot(bluestack))
    # if not coords:
    #     return False
    
    # click(1001, 118, port)
    # if imageWait('gacha10', bluestack, 0.9): # 가차 가능
    #     click(1155, 638, port)
        
    # elif getMail:
    #     gachaEnd = True
    # else:
    #     Gacha.getMail(port, bluestack)



def gacha_start(port, bluestack):
    coords = search('img/gacha_start.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(524, 487, port)

def gacha_skip(port, bluestack):
    coords = search('img/gacha_skip.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1234, 37, port)
    return True

def dialog(port, bluestack):
    target = ['dialog1', 'dialog2']

    for i in target:
        coords = search(f'img/{i}.png' ,background_screenshot(bluestack), confidence=0.8)
        if coords:
            click(651, 181, port)
            click(651, 239, port)
            click(651, 277, port)
            click(1172,658,port)
            click(1172,658,port)
            click(1172,658,port)
            click(1172,658,port)
            click(1172,658,port)
            click(1172,658,port)

def table(port, bluestack):
    coords = search('img/table.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(28, 129, port)
    print(f'속성 {int(time()-startTime)}s {port}')

def table2(port, bluestack):
    coords = search('img/table2.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(131, 129, port)

def attendance(port, bluestack):
    coords = search('img/attendance.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1235, 49, port)

def exit(port, bluestack):
    coords = search('img/exit.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1172, 658, port)
    
class Gacha:
    def checkGachaEnd(bluestack):
        if search('img/check_gacha_end.png' ,background_screenshot(bluestack), confidence=0.8):
            return True
        else:
            return False
        
    def checkGachaRetry(bluestack):
        hasRetryButton = search('img/check_gacha_retry.png' ,background_screenshot(bluestack), confidence=0.8)
        hasOkButton = search('img/check_gacha_ok.png' ,background_screenshot(bluestack), confidence=0.8)
        gachaEnd = search('img/check_gacha_end.png' ,background_screenshot(bluestack), confidence=0.8)
        
        if hasOkButton:
            if hasRetryButton:
                return 'retry'
            else:
                return 'gachaend'
        else:
            if gachaEnd:
                return 'gachaend'
            return 'gacha'

    def goHome(port, bluestack):
        start = time()
        while time() - start < 3:
            keyevent('KEYCODE_BACK', port)
            if imageWait('app_exit', bluestack, 1):
                click(506, 556, port)
                return True

        return False
    
    def startGacha10(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(76, 664, port) # 모집 클릭
        sleep(0.5)
        click(992, 114, port) # 상시 모집
        sleep(0.5)
        click(1144, 636, port) # 10연차 클릭

    def startNewbie10(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(76, 664, port) # 모집 클릭
        sleep(0.5)
        click(1144, 636, port) # 10연차 클릭

    def getMail(port, bluestack):
        global startTime

        Gacha.goHome(port, bluestack)
        click(1182, 38, port) # 메일함
        sleep(0.5)
        click(1049, 636, port) # 메일함
        if imageWait('mail', bluestack):
            sleep(1)
            click(1049, 636, port) # 메일함
            if Gacha.goHome(port, bluestack):
                print(f"getMail {int(time()-startTime)}s {port}")
                return True
            return False

        elif imageWait('mail2', bluestack): # 메일 이미 받음
            sleep(1)
            click(1049, 636, port) # 메일함
            Gacha.goHome(port, bluestack)
            if Gacha.goHome(port, bluestack):
                print(f"getMail {int(time()-startTime)}s {port}")
                return True
            return False
        else:
            return False
        
    def getCurrentStatus(port, bluestack):
        if search('img/gacha.png' ,background_screenshot(bluestack), confidence=0.8):
            return 'home'
        
        if search('img/check_gacha_end.png' ,background_screenshot(bluestack), confidence=0.8):
            return 'gachaMain'

        return 'unknown'

    def gachaLoop(port, bluestack):
        global gachaNum

        status = Gacha.getCurrentStatus(port, bluestack)
        if status != 'unknown':
            if gachaNum > 5:
                Gacha.startGacha10(port, bluestack)
                imageWait('gacha_start', bluestack)
            else:
                Gacha.startNewbie10(port, bluestack)
                imageWait('gacha_start', bluestack)
            gachaNum += 1
            print(f'Gacha {gachaNum}', port)
            return False

        click(528, 489, port)
        click(1191, 43, port)
        
        result = Gacha.checkGachaRetry(bluestack)
        if result == 'retry':
        
            click(786, 632, port) # 다시 뽑기
            gachaNum += 1
            print(f'Gacha {gachaNum}', port)
            return False

        elif result == 'gachaend':
            if gachaNum == 5:
                click(614,623, port)
                sleep(1)
                Gacha.startGacha10(port, bluestack)
                imageWait('gacha_start', bluestack)
                gachaNum += 1
                print('change to normal gacha', port)
                print(f'Gacha {gachaNum}', port)

            else:
                click(634, 623, port) # 확인 (뽑기 끝)
                if imageWait('check_gacha_end', bluestack):
                    print('Gacha End', port)
                    return True
        return False

    def goSado(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(459, 666, port) # 사도
        if imageWait('isSadoRoom', bluestack):
            print('sadoCheck Enter')
            return True
        return False
        
    def checkSado(port, bluestack, whitelist=[257, 2163, 2036, 1874]):
        lst = ocr()
        print("사도 OCR 결과 :", lst)
        img = background_screenshot(bluestack)
        # save img
        img.save(f'save/{time()}.png')
        targetNum = 0
        for target in whitelist:
            for i in lst:
                if i == target:
                    targetNum += 1

        print("발견 사도 :", targetNum)
        if targetNum >= 2:
            print("사도 발견")
            return True
        
        print("사도 미발견")
        return False

    def cacheReset(port):
        Gacha.goHome(port, bluestack)
        click(1231, 38, port) # 메뉴
        sleep(0.5)
        click(765, 310, port) # 설정
        sleep(0.5)
        click(1013, 151, port) # guitar
        sleep(0.5)
        click(933, 544, port) # cache 클리어
        sleep(0.5)
        click(779, 551, port) # 확인

    def beforeTutoGacha(port, bluestack):
        terms(port, bluestack)
        guest_login_1(port, bluestack)
        naming(port, bluestack)
        jab(port, bluestack)
        go(port, bluestack)
        nextstage(port, bluestack)
        eventstage(port, bluestack)
        thirdstage(port, bluestack)
        table(port, bluestack)
        table2(port, bluestack)
        selectdeck(port, bluestack)
        timefast(port, bluestack)
        lock(port, bluestack)
        exit(port, bluestack)
        gacha(port, bluestack)
        gacha_1(port, bluestack)
        gacha2(port, bluestack)
        gacha_start(port, bluestack)
        dialog(port, bluestack)
        universal(port, bluestack)
        return gacha_skip(port, bluestack)

def errorTask(port, bluestack):
    restartApp(port, bluestack)
    sleep(3)

isTutorialGachaStart = False
isTutorialGachaEnd = False
getMail = False
gachaEnd = False
isSadoRoom = False
checkEnd = False
noClickStack = 0
startTime = time()
resizeBluestack(bluestack)
while True:
    prevClickNum = clicknum[port]
    attendance(port, bluestack)

    if not isTutorialGachaStart:
        isTutorialGachaStart = Gacha.beforeTutoGacha(port, bluestack)
    elif not isTutorialGachaEnd:
        gacha_skip(port, bluestack)
        universal(port, bluestack)
        isTutorialGachaEnd = Gacha.checkGachaEnd(bluestack) # 첫번째 가차 종료 체크

    elif not getMail:
        getMail = Gacha.getMail(port, bluestack) # 메일 수령 후 상시 10연차 시작

    elif not gachaEnd:
        gachaEnd = Gacha.gachaLoop(port, bluestack)

    elif not isSadoRoom:
        isSadoRoom = Gacha.goSado(port, bluestack)

    elif Gacha.checkSado(port, bluestack):
        print('Find Sado')
        break
    else:
        Gacha.cacheReset(port)
        isTutorialGachaStart = False
        isTutorialGachaEnd = False
        getMail = False
        gachaEnd = False
        isSadoRoom = False
        checkEnd = False
        startTime = time()

    # 아래는 비정상 Loop 처리

    if prevClickNum == clicknum[port]: # No click
        noClickStack += 1
    else:
        noClickStack = 0

    if noClickStack == 100:
        noClickStack = 0
        errorTask(port, bluestack)
        isTutorialGachaStart = True
        isTutorialGachaEnd = True
        getMail = True
        gachaEnd = True
        print('errorTask', port)
