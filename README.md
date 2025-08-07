# 파이썬 게임 개발 프로젝트

이 프로젝트는 파이썬을 사용한 게임 개발을 위한 기본 환경을 제공합니다.

## 🎮 지원하는 게임 라이브러리

- **pygame**: 2D 게임 개발을 위한 가장 인기있는 라이브러리
- **arcade**: 현대적이고 사용하기 쉬운 2D 게임 라이브러리
- **pyglet**: OpenGL 기반의 게임 라이브러리

## 🚀 시작하기

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
```

### 2. 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 3. 게임 실행

```bash
python main.py
```

## 📁 프로젝트 구조

```
protoType/
├── main.py              # 기본 게임 파일
├── requirements.txt      # 필요한 라이브러리 목록
├── README.md           # 프로젝트 설명
├── .gitignore          # Git 무시 파일 목록
├── src/                # 소스 코드 폴더
│   ├── __init__.py
│   ├── game.py         # 게임 로직
│   ├── player.py       # 플레이어 클래스
│   └── enemy.py        # 적 클래스
├── assets/             # 게임 리소스 폴더
│   ├── images/         # 이미지 파일들
│   ├── sounds/         # 사운드 파일들
│   └── fonts/          # 폰트 파일들
└── tests/              # 테스트 파일들
    └── __init__.py
```

## 🎯 기본 게임 기능

현재 `main.py`에는 다음과 같은 기본 기능이 포함되어 있습니다:

- ✅ 기본 게임 루프
- ✅ 이벤트 처리 (키보드, 마우스)
- ✅ 화면 그리기
- ✅ FPS 제어
- ✅ 게임 종료 처리

## 🛠️ 개발 도구

- **pytest**: 테스트 실행
- **black**: 코드 포맷팅
- **flake8**: 코드 린팅

## 📚 학습 리소스

### pygame
- [pygame 공식 문서](https://www.pygame.org/docs/)
- [pygame 튜토리얼](https://www.pygame.org/wiki/tutorials)

### arcade
- [arcade 공식 문서](https://arcade.academy/)
- [arcade 예제들](https://arcade.academy/examples/)

### pyglet
- [pyglet 공식 문서](https://pyglet.readthedocs.io/)

## 🎨 게임 개발 팁

1. **게임 루프**: 항상 이벤트 처리 → 업데이트 → 그리기 순서를 유지하세요
2. **FPS**: 60 FPS가 일반적인 게임 속도입니다
3. **리소스 관리**: 이미지와 사운드는 한 번 로드하고 재사용하세요
4. **충돌 감지**: pygame의 Rect 객체를 활용하세요
5. **상태 관리**: 게임 상태(메뉴, 플레이, 일시정지 등)를 명확히 구분하세요

## 🐛 문제 해결

### pygame 설치 오류
```bash
# Windows에서 pygame 설치 오류 시
pip install pygame --pre
```

### 가상환경 문제
```bash
# 가상환경이 활성화되지 않는 경우
deactivate  # 기존 환경 비활성화
python -m venv venv --clear  # 새로 생성
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. 이 저장소를 포크하세요
2. 새로운 기능 브랜치를 만드세요
3. 변경사항을 커밋하세요
4. 브랜치에 푸시하세요
5. Pull Request를 생성하세요

---

**즐거운 게임 개발 되세요! 🎮**
