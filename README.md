# answerChecker

학교 시험 자동 채점 및 순위 관리 시스템입니다.

## 개요

answerChecker는 하성고등학교를 위해 개발된 시험 자동 채점 프로그램입니다. MySQL 데이터베이스에 저장된 답안과 학생의 답을 비교하여 자동으로 채점하고, 전체 순위 및 등급을 계산합니다.

## 주요 기능

- **자동 채점**: 답안 입력 시 자동으로 점수 계산
- **답안 관리**: 과목별 시험 답안 저장
- **순위 확인**: 시험 결과 기반 순위 조회
- **등급 계산**: rating_calculator 모듈로 등급 산출
- **데이터베이스 저장**: MySQL에 시험 결과 영구 저장

## 기술 스택

- **Python 3.x**
- **PyMySQL** - MySQL 데이터베이스 연동
- **MySQL** - 데이터 저장

## 프로젝트 구조

```
answerChecker/
├── checker.py              # 메인 채점 프로그램
├── answerinput.py          # 답안 입력 모듈
├── rating_calculator.py    # 등급 계산 모듈
└── .hwp                    # 문서 파일
```

## 데이터베이스 구조

### SCORE 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| ID | INT | 학번 |
| SUBCODE | INT | 과목코드 |
| SCORE | INT | 점수 |

### ans 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| testname | VARCHAR | 시험명 |
| testcode | INT | 과목코드 |
| answer | TEXT | 답안 |

## 설치 및 실행

### 사전 요구사항

- Python 3.x
- MySQL 서버
- 하성고 네트워크 접근 권한

### 1. 의존성 설치

```bash
pip install pymysql
```

### 2. 데이터베이스 설정

```sql
CREATE DATABASE HASEONG;
USE HASEONG;

CREATE TABLE SCORE (
    ID INT,
    SUBCODE INT,
    SCORE INT,
    PRIMARY KEY (ID, SUBCODE)
);

CREATE TABLE ans (
    testname VARCHAR(100),
    testcode INT,
    answer TEXT,
    PRIMARY KEY (testname, testcode)
);
```

### 3. 실행

```bash
python checker.py
```

## 사용 방법

### 1. 학번 입력

```
가체점기를 사용해 주셔서 감사합니다(하성고 전용)
학번을 입력하세요 >>> 12345
```

### 2. 기능 선택

```
사용할 기능을 선택하세요
1.가체점 2.순위확인 3.끝내기 >>> 1
```

### 3. 시험 정보 입력

```
시험이름을 입력하세요 예시)2학기기말고사 >>> 2학기중간고사
과목코드를 입력하세요 >>> 3

과목 코드:
1 - 국어
2 - 영어
3 - 수학
4 - 사회
5 - 과학
6 - 영어
7 - 한국사
```

### 4. 답안 입력

```
문제수를 입력하세요 >>> 20
1번쨰 답을 입력하세요 >>> 1
2번쨰 답을 입력하세요 >>> 2
...
20번쨰 답을 입력하세요 >>> 4
```

### 5. 결과 확인

```
입력 완료
85점입니다
```

### 6. 순위 확인

```
사용할 기능을 선택하세요
1.가체점 2.순위확인 3.끝내기 >>> 2

12345님은 5등 입니다
------등급표------
[등급 정보 출력]
```

## 핵심 기능 구현

### 1. 데이터베이스 연결

```python
def start():
    global conn
    try:
        conn = pymysql.connect(
            user = 'student',
            password = 'haseongh.goe.go.kr',
            host = 'nel.o-r.kr',
            port = 3306,
            charset = 'utf8'
        )
    except pymysql.err.OperationalError as error:
        print(str(error) + '! restarting')
        start()

    global cursor
    cursor = conn.cursor()
    cursor.execute('USE HASEONG')
```

### 2. 답안 불러오기

```python
def value():
    testname = str(input('시험이름을 입력하세요 >>>'))
    testcode = int(input('과목코드를 입력하세요 >>>'))

    # 답안 조회
    sql = f"select answer from ans where testname = '{testname}' and testcode = '{testcode}'"
    cursor.execute(sql)

    # 점수 조회
    sql = f"select answer from ans where testname = '{testname}_ans' and testcode = '{testcode}_ans'"
    cursor.execute(sql)
```

### 3. 학생 답 입력

```python
def ansinput():
    i = 1
    global proans
    proans = {}
    try:
        while i < problnum + 1:
            proans[str(i)] = int(input(str(i) + '번쨰 답을 입력하세요 >>>'))
            i = i + 1
    except ValueError:
        print(str(ValueError) + '! please try again')
        ansinput()
    return proans
```

### 4. 채점

```python
def check():
    i = 1
    global proscore
    proscore = 0

    while i < problnum + 1:
        try:
            score = answer[str(proans[str(i)])]
            proscore = proscore + score
        except KeyError:
            print(str(i) + '번 틀렸습니다')
        i = i + 1

    print(str(proscore) + '점입니다')
```

### 5. 결과 저장

```python
def save():
    sql = f'''INSERT INTO SCORE
    VALUES ({stunum}, {testcode}, {proscore})'''
    try:
        cursor.execute(sql)
    except MySQLError as sqlerror:
        print(str(sqlerror) + '! please try again')
```

### 6. 순위 조회

```python
def ranking():
    sql = f'''SELECT ID FROM SCORE WHERE SUBCODE = '{testcode}' ORDER BY SCORE DESC'''
    try:
        cursor.execute(sql)
    except MySQLError as error:
        print(str(error) + 'please try again')

    a = 1
    for i in cursor:
        a = a + 1
        if stunum == i:
            print(f'{stunum}님은 {a}등 입니다')
            rating_calculator.calculate(42)  # 등급 계산
```

## 사용 예시

### 시나리오: 수학 시험 채점

```
1. 학번 입력: 12345
2. 기능 선택: 1 (가체점)
3. 시험명: 2학기중간고사
4. 과목코드: 3 (수학)
5. 문제수: 20
6. 답 입력: 1, 2, 3, 4, 1, 2, 3, 4, ... (20개)
7. 결과: 85점입니다
```

## 보안 고려사항

⚠️ **주의**: 현재 코드는 다음과 같은 보안 문제가 있습니다:

### 1. SQL Injection 취약점

```python
# 취약한 코드
sql = f"select answer from ans where testname = '{testname}'"

# 개선안
sql = "select answer from ans where testname = %s"
cursor.execute(sql, (testname,))
```

### 2. 하드코딩된 인증 정보

```python
# 개선안
import os
from dotenv import load_dotenv

load_dotenv()
conn = pymysql.connect(
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASS'),
    host = os.getenv('DB_HOST')
)
```

## 제한사항

- **학교 전용**: 하성고 내부 네트워크에서만 작동
- **단일 사용자**: 동시 다중 사용자 미지원
- **중복 채점**: 같은 시험을 여러 번 채점 가능
- **답안 수정 불가**: 입력 후 수정 기능 없음

## 개선 방향

### 1. 웹 인터페이스

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/grade', methods=['POST'])
def grade():
    answers = request.form.getlist('answers')
    score = calculate_score(answers)
    return render_template('result.html', score=score)
```

### 2. 중복 채점 방지

```python
# 이미 채점한 경우 경고
sql = f"SELECT * FROM SCORE WHERE ID = {stunum} AND SUBCODE = {testcode}"
cursor.execute(sql)
if cursor.fetchone():
    print("이미 채점한 시험입니다. 덮어쓰시겠습니까? (y/n)")
```

### 3. 답안 수정 기능

```python
def modify_answer(question_num):
    print(f"현재 답: {proans[str(question_num)]}")
    new_answer = int(input("새로운 답 입력 >>> "))
    proans[str(question_num)] = new_answer
```

## 트러블슈팅

### 데이터베이스 연결 실패

```
OperationalError: (2003, "Can't connect to MySQL server")
```

해결: MySQL 서버 실행 확인 및 네트워크 연결 확인

### 인코딩 오류

```python
# UTF-8 설정 추가
conn = pymysql.connect(
    charset = 'utf8mb4',  # 이모지 지원
    use_unicode = True
)
```

## 라이선스

하성고등학교 내부용으로 제작된 프로젝트입니다.
