# Physical AI Project - Week 1

실시간 영상 입력 파이프라인 과제입니다.

## 실행

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python week1/main.py
```

## 조작

- `q`: 종료
- `s`: 현재 화면을 `result.png`로 저장

## 동영상 파일로 대체 실행

```bash
python week1/main.py --source sample_video.mp4 --limit-video-fps 30
```

## 제출 구조

```text
physical-ai-project/
├── week1/
│   └── main.py
├── requirements.txt
├── README.md
└── result.png
```

`result.png`는 실행 중 `s` 키를 눌러 저장합니다. FPS 수치가 보여야 합니다.
