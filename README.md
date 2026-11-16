# 메리-크리스마스 🎄

글자로 그리는 3D 크리스마스트리예요. 점들을 3D로 만들어 화면에 비추고, 밝기에 따라 ` .,:;-=+*#%@` 중 한 글자를 골라 트루컬러로 찍어요.

눈 쌓인 땅 → 빛 회오리 → 트리 → 장식 볼 → 전구 → 별 → 하트 → 선물 → 눈 순서로 하나씩 생기고, 다 생기면 전구에 빛이 줄줄이 달려요.

## 터미널에서 (`tree.py`)

```
python3 tree.py      # 끝내기: Ctrl+C
```

- 필요: 파이썬 3 + numpy (`python3 -m pip install numpy`, 홈브루 파이썬이면 `brew install numpy`)
- 터미널 창은 가로 96칸 × 세로 54줄 이상
- 24비트 색을 쓰니 iTerm2 나 VS Code 터미널을 권해요 (맥 기본 터미널은 색이 다르게 나올 수 있어요)
- 색·개수·시간은 파일 맨 위에 이름과 한글 설명으로 모여 있어요 (`N_LIGHTS`, `N_HEARTS`, `HOLD_TIME` …)

## 브라우저에서 (`index.html`)

`index.html` 을 열면 브라우저 속에 터미널이 열려요. `python3 tree.py` 를 입력하고 Enter 를 누르면 트리가 재생돼요. 설치도 서버도 필요 없어요 (같은 그림 계산을 JavaScript로 옮겼어요).

- 끝내기: `Ctrl+C` · `Esc` · `q`
- 그 밖의 명령: `ls`, `help`, `clear`, `echo`, `cat tree.py`



## 결과



https://github.com/user-attachments/assets/5b29e218-a693-40c9-8657-9322a2795727









