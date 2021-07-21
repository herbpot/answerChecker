import pymysql
from pymysql.err import MySQLError
import rating_calculator

def start() : #데이터베이스 접속
    global conn
    try :
        conn = pymysql.connect(
            user = 'student',
            password = 'haseongh.goe.go.kr',
            host = 'nel.o-r.kr',
            port = 3306,
            charset = 'utf8'
        )

    except pymysql.err.OperationalError as error :
        print(str(error) + '! restarting')
        start()
                
    global cursor
    cursor = conn.cursor()

    #sql문
    sql2 = '''USE HASEONG '''
    sql = 'SELECT * FROM SCORE'
    sql3 = 'select * from answer'
    #sql 실행문
    cursor.execute(sql2)
    cursor.execute(sql)
    cursor.execute(sql3)
    #확인용 메세지
    #print('done')

start()

#######################################################################

def main() : #매인코드
    global stunum
    print("가체점기를 사용해 주셔서 감사합니다(하성고 전용)")
    
    while True :
        try :
            stunum = str(input('학번을 입력하세요 >>>'))
            break
        except :
            print('숫자로 입력하세요')
    manu()


def manu() :
    while True :
        print('사용할 기능을 선택하세요')
        try :
            ans = int(input('1.가체점 2.순위확인 3.끝내기 >>>'))
            if ans == 1 :
                print('가체점을 실행합니다')
                value()
                maincheck()
            elif ans == 2 :
                print('순위를 확인합니다')
                ranking()
            elif ans == 3 :
                break
        except ValueError :
            print('다시 입력하세요')


def maincheck() : #문제 개수 입력
    global problnum
    problnum = int(input('문제수를 입력하세요 >>>'))
    ansinput()
    check()
    save()
    manu()


def value() : #답지입력
    testname = str(input('시험이름을 입력하세요 예시)2학기기말고사 >>>'))
    global testcode
    print('''
    1-국어
    2-영어
    3-수학
    4-사회
    5-과학
    6-영어
    7-한국사
    ''')
    testcode = int(input('과목코드를 입력하세요 >>>'))
    global answer
    answer = {}
    answer_q = []
    answer_s = []
    try :
        sql = f'''select answer from ans where testname = '{testname}' and testcode = '{testcode}' '''
        cursor.execute(sql)
        for i in cursor:
            answer_q[i] = list(cursor.fetchall())[i]
        sql = f'''select answer from ans where testname = '{testname}_ans' and testcode = '{testcode}_ans' '''
        cursor.execute(sql)
        for i in cursor:
            answer_s[i] = list(cursor.fetchall())[i]
        print(answer_q,answer_s)

    except MySQLError as error :
        print(error + 'please try again')
        value()

    
    for i in answer_s :
        
        answer[i] = int(answer_s[i])
        print('답 입력중')

    print(answer)
    #    answer = {'답' : '점수' , '1' : 1 , '2' : 2 , '3' : 3}


def ansinput() : #학생답 수집
    i = 1
    global proans
    proans = {}
    try :
        while i < problnum + 1 :
            proans[str(i)] = int(input(str(i) + '번쨰 답을 입력하세요 >>>'))
            i = i + 1
    
    except ValueError :
        print(str(ValueError) + '! please try again')
        ansinput()

    print('입력 완료')
    return proans


def check() : #체점
    i = 1
    global count
    count = 0
    global score
    score = 0
    print(problnum)
    print(proans)
    global proscore
    proscore = 0
    
    while i < problnum + 1 :
        try :
            score = answer[str(proans[str(i)])]
            proscore = proscore + score
        except KeyError :
            print(str(i) + '번 틀렸습니다')
        i = i + 1
    print(str(proscore) + '점입니다')


def save() : #데이터 저장
    sql5 = f'''INSERT INTO SCORE
    VALUES ({stunum}, {testcode}, {proscore})'''
    try :
        cursor.execute(sql5)
    
    except MySQLError as sqlerror:
        print(str(sqlerror) + '! please try again')
        
    #확인용 메세지
    #print('done')

    
def ranking() : #순위 확인
    sql6 = f'''SELECT ID FROM SCORE ORDER WHERE SUBCODE = '{testcode}' BY SCORE DESC'''
    try : 
        cursor.execute(sql6)
    except MySQLError as error :
        print(str(error) + 'please try again')
    a = 1
    print(cursor)
    for i in cursor :
        a = a + 1
        print(i)
        if stunum == i :
            print(f'{stunum}님은 {a}등 입니다')
            print('------등급표------')
            rating_calculator.clculate(42)
            
            
    #확인용 메세지
    #print('done')

main()

conn.commit()
conn.close()