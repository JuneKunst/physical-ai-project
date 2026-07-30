# Physical AI Project

Physical AI 사전캠프 과제를 주차별로 정리한 저장소입니다.

## 과제 내용

- **Week 1**: 웹캠 영상에 grayscale, blur, edge 검출을 적용하고 FPS를 표시했습니다.
- **Week 2**: HSV 색상 범위를 이용해 빨간색 물체를 찾고 중심 좌표를 표시했습니다.
- **Week 3**: 물체의 픽셀 좌표를 이동, 스케일, 회전 행렬을 이용해 실세계 좌표로 변환하고 그래프로 확인했습니다.
- **Week 4**: 앞에서 만든 기능을 sense, compute, act 순서로 연결하고 단계별 처리 시간을 확인했습니다.

주차별 학습 내용은 `notes` 폴더에 정리했습니다.

## 미니 프로젝트

- [MoMA 작품 CSV 챗봇](mini-kaggle-chatbot/README.md): 작품 이미지, 작가, 재료와 작품 분류를 검색합니다.

## 실행 방법

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

실행할 주차의 파일을 선택하면 됩니다.

```bash
python week1/main.py
python week2/main.py
python week3/main.py
python week4/main.py
```

영상 파일을 사용하려면 `--source` 옵션을 추가합니다.

```bash
python week3/main.py --source sample_video.mp4
```

## 조작 방법

- `s`: 현재 화면 저장
- `q`: 종료
- `a` / `d`: 3·4주차 회전각 조절
- `+` / `-`: 3·4주차 스케일 조절
