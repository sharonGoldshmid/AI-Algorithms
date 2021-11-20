#sharon goldshmid 212118731

import copy
VIC=10**20 #The value of a winning board (for max) 
LOSS=-VIC #The value of a losing board (for max)
TIE=0 #The value of a tie
SIZE=4 #The length of a winning sequence
COMPUTER=SIZE+1 #Marks the computer's cells on the board
HUMAN=1 #Marks the human's cells on the board

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. number of empty cells
'''
def create():
#Returns an empty board. The human plays first.
    board=[]
    for i in range(6):
        board=board+[7*[0]]
    return [board, 0.00001, HUMAN, 42]

def value(s):
#Returns the heuristic value of s
    return s[1]

def printState(s):
#Prints the board. The empty cells are printed as numbers = the cells name(for input)
#If the game ended prins who won.
    for r in range(len(s[0])):
        print("\n --  --  --  --  --  --  --  --\n|", end="")
        for c in range(len(s[0][0])):
            if s[0][r][c]==COMPUTER:
                print("X  |", end="")
            elif s[0][r][c]==HUMAN:
                print("O  |", end="")
            else:
                if r*7+c <10:
                    print(r*7+c," |", end="")
                else:
                    print(r*7+c, "|", end="")
    print("\n --  --  --  --  --  --  --  --\n")
    if value(s)==VIC:
        print("Ha ha ha I won!")
    elif value(s)==LOSS:
        print("You did it!")
    elif value(s)==TIE:
        print("It's a TIE")

def isFinished(s):
#Seturns True iff the game ended
    return s[1] in [LOSS, VIC, TIE]

def isHumTurn(s):
#Returns True iff it the human's turn to play
    return s[2]==HUMAN

def whoIsFirst(s):
#The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you. : "))==1:
        s[2]=COMPUTER
    else:
        s[2]==HUMAN

def checkSeq(s,r1,c1,r2,c2):
# r1, c1 are in the board. if r2,c2 not on board returns 0.
# Checks the seq. from r1,c1 to r2,c2. If all X returns VIC. If all O returns LOSS.
# If no Os returns 1. If no Xs returns -1, Othewise returns 0.
    if r2<0 or c2<0 or r2>=len(s[0]) or c2>=len(s[0][0]):
        return 0 #r2, c2 are illegal
    dr=(r2-r1)//(SIZE-1) #the horizontal step from cell to cell
    dc=(c2-c1)//(SIZE-1) #the vertical step from cell to cell
    sum=0
    for i in range(SIZE):#summing the values in the seq.
        sum+=s[0][r1+i*dr][c1+i*dc]
    if sum==COMPUTER*SIZE:
        return VIC
    if sum==HUMAN*SIZE:
        return LOSS
    numFull = sum//COMPUTER + sum%COMPUTER #סכום מספר דסקיות ברביעיה
    if sum<COMPUTER: #אם רק משתמש- הפסד
        return -1*2**(numFull*5)
    if sum%COMPUTER==0: #אם רק מחשב- ניצחון
        return 2**(numFull*5)
    return 0 #אם לא הוחזר ערך עד כה- לא ניתן להשלים לרצף ברביעיה הזאת כי לפחות תא אחד תפוס עבור כל שחקן

"""
בחרתי לתת סימון של 2 בחזקת מספר הדסקיות כדי שתהיה העדפה מובהקת בין רצף לא שלם של
אותו השחקן לבין מספרגדול הרבה יותר של רצפים הנובעים מאריח יחיד שנמצא במקום המאפשר זאת
ובאמת רואים את ההבדל שהתוצאות היו הרבה יותר טובות
עדיף להשתמש במספר הדסקיות ולא בסכום כדי שערך היוריסטי יהיה נכון גם עבור תור הבנאדם
שהניקוד על הדיסקיות שלו נמוכות הרבה יותר
הקטנתי את עומק החיפוש ל5 כי זה לקח יותר מדי זמן, והתוצאות עדיין טובות מאוד
"""    

def makeMove(s,r,c):
# Puts mark (for huma. or comp.) in r,c
# switches turns
# and re-evaluates the heuristic value.
# Assumes the move is legal.
    s[0][r][c]=s[2] # marks the board
    s[3]-=1 # one less empty cell
    s[2]=COMPUTER+HUMAN-s[2] # switches turns
    dr=[-SIZE+1, -SIZE+1, 0, SIZE-1] # the next lines compute the heuristic val.
    dc=[0, SIZE-1, SIZE-1, SIZE-1]
    s[1]=0.00001
    for row in range(len(s[0])):
        for col in range(len(s[0][0])):
            for i in range(len(dr)):
                t=checkSeq(s,row,col,row+dr[i],col+dc[i])
                if t in [LOSS,VIC]:
                    s[1]=t
                    return
                else:
                    s[1]+=t
    if s[3]==0:
        s[1]=TIE

#לא מצאתי מה לשנות כאן למרות שהתבקשנו, במקום זה שיניתי את הפונקציה
#checkSeq
#ע"מ לקבל היוריסטיקה טובה יותר
    
   
def inputMove(s):
# Reads, enforces legality and executes the user's move.
    printState(s)
    flag=True
    while flag:
        move=int(input("Enter your next move: "))
        r=move//7
        c=move%7
        if r<0 or r>=len(s[0]) or c<0 or c>=len(s[0][0]) or s[0][r][c]!=0 or (r<5 and s[0][r+1][c]==0): #I added if the box under is empty
            print("Ilegal move.")
        else:
            flag=False
            makeMove(s,r,c)
            
def getNext(s):
# returns a list of the next states of s
    ns=[]
    for c in range(len(s[0][0])):
        for r in range(len(s[0])):
            if s[0][r][c]!=0 and r==0: #go to the next coll if its full
                break
            if s[0][r][c]==0 and (r==5 or s[0][r+1][c]!=0): #look for the last empty box in this coll
                tmp=copy.deepcopy(s)
                makeMove(tmp,r,c)
                ns+=[tmp]
                break
    ns.sort(key = value)
    return ns
"""
:הפונקציה תמיין את הבנים לפי הערך היוריסטי מהקטן לגדול, לכן
abmax בקובץ אלפאביתא בפונקציה
נעשה רוורס לרשימה כדי שתהיה ממוינת לפי ערך היוריסטי מהגדול לקטן

זה מאפשר לעשות עומק חיפוש של 7 מה שידרוש בערך 3 שניות חיפוש
לעומת עומק 7 בלי המיון שדורש בערך 21 שניות חיפוש
כעת התוצאות טובות יותר כי הגדנו את העומק
"""
