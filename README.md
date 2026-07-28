# Physical AI Project

Physical AI 사전캠프 과제를 주차별로 정리한 저장소입니다.

## 과제 내용

- **Week 1**: 웹캠 영상에 grayscale, blur, edge 검출을 적용하고 FPS를 표시했습니다.
- **Week 2**: HSV 색상 범위를 이용해 빨간색 물체를 찾고 중심 좌표를 표시했습니다.
- **Week 3**: 물체의 픽셀 좌표를 이동, 스케일, 회전 행렬을 이용해 실세계 좌표로 변환하고 그래프로 확인했습니다.

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
```

영상 파일을 사용하려면 `--source` 옵션을 추가합니다.

```bash
python week3/main.py --source sample_video.mp4
```

## 조작 방법

- `s`: 현재 화면 저장
- `q`: 종료
- `a` / `d`: 3주차 회전각 조절
- `+` / `-`: 3주차 스케일 조절
