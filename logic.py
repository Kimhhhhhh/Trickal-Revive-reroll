import os
from time import sleep, time
from bluestack import *

# 이미지 인식 후 로직 관련된 함수들

# 약관동의
def terms(port, bluestack):
    coords = search('img/terms.png' ,background_screenshot(bluestack))
    if not coords:
        return False

    click(727,626, port)
    print(f"약관 {int(time()-Macro.startTime)}s {port}")

# 게스트 로그인
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

# 볼 땡기기
def jab(port, bluestack):
    coords = search('img/jab.png' ,background_screenshot(bluestack), 0.5)
    if not coords:
        return False
    
    click(559, 416, port)
    click(745, 311, port)
    click(804, 499, port)
    click(631, 618, port)
    click(771, 651, port)
    click(644, 246, port)
    click(951, 115, port)
    click(540, 651, port)
    click(1234, 355, port)
    click(1154,601, port) #
    click(1173,423, port) #
    click(618,573, port) #
    click(847, 538, port) #
    click(719, 688, port) #
    click(945, 493, port) #
    print(f'볼잡기 {int(time()-Macro.startTime)}s {port}')

# 이름 짓기
def naming(port, bluestack, name='temp'):
    coords = search('img/naming.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(662, 348, port)                                       
    typing(name, port)
    sleep(0.8)
    click(665, 522, port)
    click(665, 522, port)
    print(f'이름 {int(time()-Macro.startTime)}s {port}')

# 확인버튼
def ok(port, bluestack):
    coords = search('img/ok.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(coords[0], coords[1], port)

# 전투 및 튜토리얼 일반적인 진행
def arrow(port, bluestack):
    target = ['arrow2', 'arrow4', 'arrow5', 'arrow6', 'arrow8', 'arrow9']
    targetimg = [i[:-4] for i in os.listdir('img') if 'arrow' in i]

    for i in target:
        coords = search(f'img/{i}.png' ,background_screenshot(bluestack), confidence=0.7)
        if coords:            
            click(631, 618, port)
            click(771, 651, port)
            click(644, 246, port)
            click(951, 115, port)
            click(540, 651, port)
            click(1234, 355, port) # 전투 다음 페이지
            click(899, 638, port)
            click(390, 654, port)
            return

# 영춘 대사 or 영춘 가이드
def youngchoon(port, bluestack):
    target = ['youngchoon', 'youngchoon2', 'youngchoon3', 'youngchoon4']
    # youngchoon이 포함된 img 폴더의 이미지들을 전부 찾아서
    targetimg = [i[:-4] for i in os.listdir('img') if 'youngchoon' in i]

    for i in target:
        coords = search(f'img/{i}.png' ,background_screenshot(bluestack), confidence=0.8)
        if coords:
            click(1154,601, port) # 모험
            click(1081,423, port) # 침략
            click(673,423, port) # 1-1
            click(618,573, port) # 마고
            click(847, 538, port) # 빨간애
            click(719, 688, port) # 마지막나가기
            click(945, 493, port) # 빈자리
            click(825, 269, port) # 이벤트
            return
        
# 보편적으로 인식 시키는 이미지 로직들
def universal(port, bluestack):
    arrow(port, bluestack)
    ok(port,bluestack)
    youngchoon(port,bluestack)

# 출발 버튼
def go(port, bluestack):
    coords = search('img/go.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1020, 667, port)

# 다음 스테이지 버튼
def nextstage(port, bluestack):
    coords = search('img/nextstage.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1140, 458, port)
    click(1140, 657, port)

# 이벤트 스테이지
def eventstage(port, bluestack):
    coords = search('img/eventstage.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1140, 657, port)

# 1-3 스테이지 입장
def thirdstage(port, bluestack):
    coords = search('img/thirdstage.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(644, 451, port)

# 덱 선택
def selectdeck(port, bluestack):
    coords = search('img/selectdeck.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1148, 563, port)

# 배속
def timefast(port, bluestack):
    coords = search('img/timefast.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1167, 38, port)
    print(f'배속 {int(time()-Macro.startTime)}s {port}')
    
# 패 잠금
def lock(port, bluestack):
    coords = search('img/lock.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(369, 675, port)
    print(f'lock {int(time()-Macro.startTime)}s {port}')

# 홈 화면 좌측 하단 모집
def gacha(port, bluestack):
    coords = search('img/gacha.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(66, 658, port)

# 튜토가차 영춘 대사
def gacha_1(port, bluestack):
    coords = search('img/gacha_1.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1172, 658, port)

# 가챠 진입 체크
def gacha_start(port, bluestack):
    coords = search('img/gacha_start.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(524, 487, port)

# 가챠 스킵 버튼 -> 함수가 처음 콜 받았을 때, Macro.isTutorialGachaStart 가 True로 전환
def gacha_skip(port, bluestack):
    coords = search('img/gacha_skip.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1234, 37, port)
    return True

# 대화 관련 로직
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

# 속성, 시너지
def table(port, bluestack):
    coords = search('img/table.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(28, 129, port)
    print(f'속성 {int(time()-Macro.startTime)}s {port}')

def table2(port, bluestack):
    coords = search('img/table2.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(131, 129, port)

# 출석 체크
def attendance(port, bluestack):
    coords = search('img/attendance.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1230, 39, port)
    sleep(0.5)
    click(1235, 39, port)

def exit(port, bluestack):
    coords = search('img/exit.png' ,background_screenshot(bluestack))
    if not coords:
        return False
    
    click(1172, 658, port)

# 에러 or 비정상 루프에서 앱 재시작
def errorTask(port, bluestack):
    restartApp(port, bluestack)
    sleep(3)

# 홈 화면에서 트릭컬 어플 클릭
def homestart(port, bluestack):
    coords = search('img/homestart.png' ,background_screenshot(bluestack), 0.8)
    if coords:
        click(coords[0], coords[1], port)
        print('homestart Click')