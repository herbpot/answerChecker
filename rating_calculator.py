def main() :
    
    try :
        num = int(input('학생수를 입력하세요 >>>'))
        clculate(num)
    except ValueError as V :
        print(V + 'error please tyr again')
        main()

def clculate(num) :
    global i
    rank = [0,0,0,0,0,0,0,0,0]
    rank_ = [4,11,23,40,60,77,89,96,100]
    i = 0
    for i in range(9) :
        rank[i] = round(num * rank_[i] / 100)
        print(str(rank[i]) + '등까지' + str(i+1) + '등급입니다')



#main()