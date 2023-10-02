from time import sleep, time
from logic import *
import os

class Gacha:
    # 가차 끝났는지 체크
    def checkGachaEnd(bluestack):
        if search('img/check_gacha_end.png' ,background_screenshot(bluestack), confidence=0.8):
            return True
        else:
            return False
        
    # 가차 중에 가차 다시하기 버튼이 있는지 확인.
    # 확인 버튼만 있으면 다시하기를 못하니까 가차 끝난걸로 간주.
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

    # 트릭컬 홈으로 이동, 백 버튼을 반복적으로 어플 나가기 나올 때까지 누름
    def goHome(port, bluestack):
        start = time()
        while time() - start < 3:
            keyevent('KEYCODE_BACK', port)
            if imageWait('app_exit', bluestack, 2):
                click(506, 556, port)
                sleep(1)

                return True

        return False
    
    # 홈으로 이동 후, 10연차 초기 세팅에 따라 픽업 or 상시 설정
    def startGacha10(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(76, 664, port) # 모집 클릭
        imageWait('check_gacha_end', bluestack)
        if Macro.pickUp:
            click(812, 114, port)
        else:
            click(992, 114, port) # 상시 모집
        imageWait('gacha10', bluestack)
        click(1144, 636, port) # 10연차 클릭

    # 홈으로 이동 후, 뉴비 10연차
    def startNewbie10(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(76, 664, port) # 모집 클릭
        imageWait('check_gacha_end', bluestack)
        click(1144, 636, port) # 10연차 클릭

    # 홈으로 이동 후 메일 수령
    def getMail(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(1182, 38, port) # 메일함
        imageWait('mail3', bluestack)
        click(1049, 636, port) # 메일 수령
        if imageWait('mail', bluestack):
            sleep(2)
            click(662, 630, port) # 빈화면 터치
            print(f"getMail {int(time()-Macro.startTime)}s {port}")
            return True

        elif imageWait('mail2', bluestack): # 메일 이미 받음
            sleep(1)
            click(1049, 636, port)
            print(f"getMail {int(time()-Macro.startTime)}s {port}")
            return True
        else:
            return False
        
    # 현재 상태 체크 홈 or 모집 탭 or 알수없음
    def getCurrentStatus(port, bluestack):
        if search('img/gacha.png' ,background_screenshot(bluestack), confidence=0.8):
            return 'home'
        
        if search('img/check_gacha_end.png' ,background_screenshot(bluestack), confidence=0.8):
            return 'gachaMain'

        return 'unknown'
    
    # 항상 인식 시켜야 하는 로직들
    def alwaysLoop(port, bluestack):
        attendance(port, bluestack)  # 출석
        homestart(port, bluestack)  # 홈 화면에서 어플 클릭
        jab(port, bluestack)  # 볼 땡기기

    # 가차 루프, 메일 수령이 확인되면 돌아간다
    # 현재 상태를 확인하고 홈 or 모집 탭이면 가차 시작
    # 상태가 알 수 없으면 가차 중인 걸로 간주한다. 가차 중이면 skip 이랑 볼따구 좌표 클릭
    def gachaLoop(port, bluestack):
        status = Gacha.getCurrentStatus(port, bluestack)
        if status != 'unknown':
            if Macro.gachaNum > 5 or not Macro.newbie:
                Gacha.startGacha10(port, bluestack)
                imageWait('gacha_start', bluestack)
            else:
                Gacha.startNewbie10(port, bluestack)
                imageWait('gacha_start', bluestack)
            Macro.gachaNum += 1
            print(f'Gacha {Macro.gachaNum}', port)
            return False

        click(528, 489, port) # 볼따구
        click(1191, 43, port) # skip 버튼
        
        result = Gacha.checkGachaRetry(bluestack)  # 가차 중에 가차 다시하기 버튼이 있는지 확인.
        if result == 'retry':  # 가차 다시하기 버튼이 있음
            click(786, 632, port) # 다시 뽑기
            Macro.gachaNum += 1
            print(f'Gacha {Macro.gachaNum}', port)
            return False

        elif result == 'gachaend':  # 가차가 끝남
            if Macro.gachaNum == 5 and Macro.newbie:  # 5번째 가차 끝남 -> 초보자 뽑기 끝났으니 상시 or 픽업으로 이동
                click(614,623, port)
                sleep(1)
                Gacha.startGacha10(port, bluestack)
                imageWait('gacha_start', bluestack)
                Macro.gachaNum += 1
                print('change to normal gacha', port)
                print(f'Gacha {Macro.gachaNum}', port)

            else:  # 가챠 전부 끝남
                click(634, 623, port) # 확인 (뽑기 끝)
                if imageWait('check_gacha_end', bluestack):
                    print('Gacha End', port)
                    return True
        return False

    # 사도 탭으로 이동
    def goSado(port, bluestack):
        Gacha.goHome(port, bluestack)
        click(459, 666, port) # 사도
        if imageWait('isSadoRoom', bluestack):
            print('sadoCheck Enter')
            return True
        return False
    
    # 사도 탭에서 사용 가능, 사도 갯수 구하는 함수. sado 폴더 안에있는 이미지 인식함
    def countSado(port, bluestack):
        sadoImgList = []
        sadoList = []
        for i in os.listdir('sado'):
            sadoImgList.append(Image.open(f'sado/{i}')) 
            sadoList.append(i[:-4])
        
        targetNum = 0
        for i, img in enumerate(sadoImgList):
            if search(img, background_screenshot(bluestack), 0.83):
                print('Find :', sadoList[i])
                targetNum += 1
        print('Total Find Num :', targetNum)
        return targetNum
        
    # 목표 사도 몇마리 있는지 확인하고, stopNum 이상이면 True 반환
    def checkSado(port, bluestack):
        targetNum = Gacha.countSado(port, bluestack)
        background_screenshot(bluestack).save(f'save/{time()}.png')
        if targetNum >= Macro.stopNum:
            print("사도 발견")
            return True
        
        print("사도 미발견")
        return False

    # 캐시 클리어
    def cacheReset(port):
        Gacha.goHome(port, Macro.bluestack)
        click(1231, 38, port) # 메뉴
        imageWait('reset1', Macro.bluestack)
        click(765, 310, port) # 설정
        imageWait('reset2', Macro.bluestack)
        click(1013, 151, port) # guitar
        imageWait('reset3', Macro.bluestack)
        click(933, 544, port) # cache 클리어
        imageWait('reset4', Macro.bluestack)
        click(779, 551, port) # 확인

    # 튜토리얼 가차 이전까지 로직 모음 gacha_skip 에서 True 반환시 이쪽 로직은 사용 안함.
    def beforeTutoGacha(port, bluestack):
        terms(port, bluestack)
        guest_login_1(port, bluestack)
        naming(port, bluestack) # 이름 짓기
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
        gacha_start(port, bluestack)
        dialog(port, bluestack)
        universal(port, bluestack)
        return gacha_skip(port, bluestack)
