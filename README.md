# BlueStack 5 전용 트릭컬 리바이브 리세마라 매크로
Python으로 작성된 트릭컬 리바이브 리세마라 매크로입니다. <br>
Pytesseract를 사용한 OCR로 뽑기가 끝난 뒤 사도를 확인하는게 특징입니다. <br>
볼그림 넷 중 둘 나오면 매크로는 멈춥니다.
되는대로 만들어서 굉장히 코드가 난잡합니다. 감사합니다.

## Requirements
- adb.exe
    - 환경변수로 등록해야합니다.
    - https://4urdev.tistory.com/77

- tesseract-ocr
    - https://github.com/UB-Mannheim/tesseract/wiki
    - Tesseract installer for Windows를 다운로드 후 설치하면 됩니다.
    - 설치 경로는 C:/Program Files/Tesseract-OCR 입니다.
    - C:/Program Files/Tesseract-OCR/tesseract.exe에 해당하는 파일이 있어야합니다.

- Bluestack 5 (중요)
    - 매크로를 실행을 위한 앱 플레이어입니다.
    - 성능 설정은 따로 테스트하지 못했습니다.
    - 광고를 꺼야합니다.
    - 디스플레이 설정
        - 화면해상도 가로모드 1280x720
        - 픽셀 밀도 320 DPI

- Windows 디스플레이 설정
    - 디스플레이 해상도 1920x1080
    - 배율 100%

- Python (필수아님)
    - 직접 Python 스크립트를 실행시키고 싶다면 필요합니다.
    - Python 3.11.5

## Installation
- Release에서 압축된 파일을 다운로드 받은후, 압축을 해제합니다.

## Usage
`명령프롬프트`에서 실행시킵니다. `macro.exe`가 있는 경로에서 아래의 명령을 보냅니다.
```
macro.exe [port] [AppPlayerNum]
```
1. `port`는 ADB에 연결하기 위한 포트입니다.
    - 블루스택 앱플레이어 설정 -> 고급기능 설정에서 127.0.0.1:[port]를 확인할 수 있습니다. 4자리 숫자입니다.

2. `AppPlayerNum`은 Bluestack 윈도우 핸들을 얻기 위한 값입니다.
    - 블루스택의 좌측 상단에 BlueStacks App Player가 있는데, 우측의 숫자를 의미합니다. <br>숫자가 없이 BlueStacks App Player만 있다면 값으로 0을 넣어주시면 됩니다.

> 여러 배럭의 매크로를 돌리고 싶으시면, 그 만큼 프로그램을 실행시키면 됩니다.

## History
- v1.0.1
    - 배포파일에 save 폴더 추가.
    - 비정상 Loop 및 멈춤 현상 개선.
    - 초보자 뽑기 5회 진행 후, 상시 뽑기로 전환하는 방식으로 가차 진행.
