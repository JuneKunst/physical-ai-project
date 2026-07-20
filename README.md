# Physical AI Project - Week 1

웹캠 영상을 받아서 간단한 전처리를 적용하는 과제 정리

적용한 처리 과정

1. 웹캠 또는 영상 파일 입력
2. Grayscale 변환
3. Gaussian Blur 적용
4. Canny edge 검출
5. 원본 화면과 edge 화면을 나란히 출력
6. 화면에 FPS 표시

## 실행 방법

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python week1/main.py
```

영상 파일로 실행하려면 다음처럼 실행

```bash
python week1/main.py --source sample_video.mp4
```

## 조작 방법

- `s`: 현재 화면을 `result.png`로 저장
- `q`: 종료

## 제출 파일

```text
physical-ai-project/
├── week1/main.py
├── requirements.txt
├── README.md
└── result.png
```
