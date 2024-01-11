### 파일/디렉토리

- client: 클라이언트 구현
- venv: 파이선 환경 저장
- requirements.txt: 파이선 패키지 목록
- sample.py: 파이선 예제

### 실행 방법

```
# 환경 설정
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 예제 실행
python sample.py -f "wav 파일 경로"

python sample.py -f "wav 파일 경로" -e whisper

```

### 참고
- stt에 기본 엔진과 whisper를 사용할 수 있습니다. 기본 엔진은 실행이 빠르고 음절 분할이 정확하지만 들리는 그대로 문장을 만들기 때문에 문장 정확도는 낮을 수 있습니다. whisper는 whisper 라지모델을 사용하므로 문장 정확도가 더 높을 수 있습니다.
