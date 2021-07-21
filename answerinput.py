import pymysql

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

start()

l = []
l_s = []

def setans() :    
    try :
        global testcode
        global testname
        global ans    
        
        testcode = 00
        ans = 0
        testname = str(input('시험이름을 입력하세요 >>>'))
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
        ans = int(input('저장할 답의 개수를 입력하세요(최대 50개) >>>'))

    except ValueError as V:
        print(str(V) + '!' +'please try again')
        setans()
    #except TypeError as T :
    #    print(str(T) + '!' +'please try again')
    #    setans()
        
    if ans > 50 :
        setans()
    input(ans)


def input_(time) :
    try :    
        for i in range(time + 1) :
            ans = int(input(f'{i}번 답 >>>'))
            l.append(ans)
            ans = int(input(f'{i}번 점수 >>>'))
            l_s.append(ans)
    except :
        print('error! please try again')
        input_()

setans()

l = tuple(l)
sql6 = f'''insert into ans
values('{testname}','{testcode}','{l}')'''

sql7 = f'''insert into ans
values('{testname}_ans','{testcode}_ans','{l_s}')'''

sql2 = '''USE HASEONG '''

cursor.execute(sql2)

cursor.execute(sql6)
cursor.execute(sql7)

conn.commit()
conn.close()

print('done')
