from logic import *
from gacha import Gacha

if __name__ == '__main__':
    sleep(1)
    resizeBluestack(Macro.bluestack)
    previmg = background_screenshot(Macro.bluestack)
    while True:
        prevClickNum = Macro.clicknum[Macro.port]
        Gacha.alwaysLoop(Macro.port, Macro.bluestack)  # 어떤 상태든 항상 인식

        if not Macro.isTutorialGachaStart:
            Macro.isTutorialGachaStart = Gacha.beforeTutoGacha(Macro.port, Macro.bluestack)  # 첫번째 가차 시작 전 까지

        elif not Macro.isTutorialGachaEnd:
            gacha_skip(Macro.port, Macro.bluestack)
            universal(Macro.port, Macro.bluestack)
            Macro.isTutorialGachaEnd = Gacha.checkGachaEnd(Macro.bluestack)  # 첫번째 가차 종료 체크

        elif not Macro.getMail:
            Macro.getMail = Gacha.getMail(Macro.port, Macro.bluestack)  # 메일 수령

        elif not Macro.gachaEnd:
            Macro.gachaEnd = Gacha.gachaLoop(Macro.port, Macro.bluestack)  # 가차 루프

        elif not Macro.isSadoRoom:
            Macro.isSadoRoom = Gacha.goSado(Macro.port, Macro.bluestack)  # 사도 확인하기 위해 이동

        elif Gacha.checkSado(Macro.port, Macro.bluestack):  # 사도 확인
            print('Find Sado')
            break

        else:
            Gacha.cacheReset(Macro.port)  # 캐리 리셋
            Macro.reset()

        # 아래는 비정상 Loop 처리
        # if locate(previmg ,background_screenshot(Macro.bluestack)): # 화면이 안바뀜
        #     noScreenChangeStack += 1
        # else:
        #     noScreenChangeStack = 0
        #     previmg = background_screenshot(Macro.bluestack)

        # if noScreenChangeStack % 20 == 0 and noScreenChangeStack != 0:
        #     print('noScreenChangeStack', noScreenChangeStack)

        # if noScreenChangeStack == 100:
        #     noScreenChangeStack = 0
        #     isTutorialGachaStart = False
        #     isTutorialGachaEnd = False
        #     getMail = False
        #     gachaEnd = False
        #     isSadoRoom = False
        #     checkEnd = False
        #     gachaNum = 0
        #     startTime = time()
        #     errorTask(port, Macro.bluestack)
        #     print('errorTask', port)



        # if prevClickNum == Macro.clicknum[port]: # No click
        #     noClickStack += 1
        # else:
        #     noClickStack = 0

        # if noClickStack == 100:
        #     noClickStack = 0
        #     errorTask(port, Macro.bluestack)
        #     isTutorialGachaStart = True
        #     isTutorialGachaEnd = True
        #     getMail = True
        #     gachaEnd = True
        #     print('errorTask', port)
