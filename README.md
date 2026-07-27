# Physical AI Project

Physical AI 사전 과제 정리 저장소입니다.

## 설치

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Week 1

웹캠 영상을 받아서 간단한 전처리를 적용하는 과제입니다.

처리 과정:

1. 웹캠 또는 영상 파일 입력
2. Grayscale 변환
3. Gaussian Blur 적용
4. Canny edge 검출
5. 원본 화면과 edge 화면을 나란히 출력
6. 화면에 FPS 표시

실행:

```bash
python week1/main.py
```

영상 파일로 실행:

```bash
python week1/main.py --source sample_video.mp4
```

## Week 2

1주차 실시간 루프 위에 색 기반 물체 인식을 추가했습니다.

처리 과정:

1. 웹캠 또는 영상 파일 입력
2. HSV 색 공간 변환
3. 빨간색 영역 마스킹
4. Contour 검출
5. 작은 노이즈 제거
6. 바운딩 박스, 중심점, 중심 좌표 표시
7. 중심 좌표와 면적을 터미널에 출력
8. 원본 화면과 Mask 화면을 나란히 출력
9. 화면에 FPS 표시

실행:

```bash
python week2/main.py
```

영상 파일로 실행:

```bash
python week2/main.py --source sample_video.mp4
```

## Week 3

2주차에서 구한 물체의 중심 픽셀 좌표를 실세계 좌표로 변환합니다.

처리 과정:

1. 빨간색 물체 중 면적이 가장 큰 물체 인식
2. 이미지 중앙을 원점으로 이동
3. 스케일 행렬로 픽셀 단위 변환
4. 회전 행렬로 축 방향 보정
5. 픽셀 좌표와 실세계 좌표를 화면과 터미널에 표시
6. 최근 좌표를 matplotlib 산점도로 표시

실행:

```bash
python week3/main.py
```

영상 파일로 실행:

```bash
python week3/main.py --source sample_video.mp4
```

## 조작 방법

- `s`: 현재 화면 저장
  - Week 1 기본 저장 파일: `result.png`
  - Week 2 기본 저장 파일: `result_week2.png`
  - Week 3 기본 저장 파일: `result_week3.png`
- `a` / `d`: Week 3 회전각을 5도씩 조절
- `+` / `-`: Week 3 스케일 조절
- `q`: 종료

## 제출 파일 구조

```text
physical-ai-project/
├── week1/
│   └── main.py
├── week2/
│   └── main.py
├── week3/
│   ├── main.py
│   └── transform.py
├── requirements.txt
└── README.md
```
