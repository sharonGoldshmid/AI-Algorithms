#writen by Sharon Goldshmid 212118731

import CSProblem
import copy

def solve(n):
    CSProblem.present(backtrack(CSProblem.create(n)))

def backtrack(p):
    var=next_var(p)# MRV-Most constrained variable or Minimum Remaining Values
    if var==None:
        return p
    dom=sorted_domain(p, var)# LCV-least constraining value
    for i in dom:
        bu=copy.deepcopy(p)
        CSProblem.assign_val(bu, var, i)
        propagate_constraints(bu, var)#
        bu=backtrack(bu)
        if CSProblem.is_solved(bu):
            return bu
    return p

def sorted_domain(p, v, LCV=True): #מחזיר ערך שיוצב בדומיין של העמודה עליה הופעלה הפונקציה
    if LCV==False:
        return CSProblem.domain(p,v)
#:כרגע מוחזר הדומיין כמו שהוא, בלי חשיבות לסדר, לכן
#true נמחק הערך השלישי בקריאה לפונקציה זו כדי שיתקבל הערך backtrack בפונקציה
#:נרצה להחזיר העתק של הדומיין כך ש
#הערכים יהיו מסודרים בסדר עולה ע"פ ההשפעה שלהם על העמודות האחרות

#my code here
    domain = CSProblem.domain(p,v)
    f= lambda x: num_of_del_vals([p,v,x])
    return sorted(domain,key=f)
    
    

def num_of_del_vals(l): #מונה כמה ערכים ימחקו מהדומיינים האחרים אם נבחר בערך זה
#l=[problem, the variable, the val. assigned to the var.]
#returns the num. of vals. erased from vars domains after assigning x to v
    count=0
    for inf_v in CSProblem.list_of_influenced_vars(l[0], l[1]):
        for i in CSProblem.domain(l[0], inf_v):
            if not CSProblem.is_consistent(l[0], l[1], inf_v, l[2], i):
                count+=1
    return count
        
def next_var(p, MRV=True):
#p is the problem
#MRV - Minimum Remained Values
#Returns next var. to assign
#If MRV=True uses MRV heuristics
#If MRV=False returns first non-assigned var.
    if MRV==False:
        u=CSProblem.get_list_of_free_vars(p)
        if u==[]:
            return None
        else:
            return u[0]
#:כרגע העמודות נבדקות לפי הסדר שהן מופיעות על הלוח, לכן
#true נמחק הערך השני בקריאה לפונקציה זו כדי שיתקבל הערך backtrack בפונקציה

#my code here
    v=CSProblem.get_list_of_free_vars(p)
    if v==[]:
        return None #הכל עודכן - סיימנו לחפש פיתרון
    d_min=[v[0]]
    for i in v: #חיפוש העמודה/ות בעלת הדומיין המינימלי
        if CSProblem.domain_size(p,i) < CSProblem.domain_size(p,d_min[0]):
            d_min=[i]
        else:
            if CSProblem.domain_size(p,i) == CSProblem.domain_size(p,d_min[0]):
                d_min += [i]
    if len(d_min)==1:
        return d_min[0]
    #אם יש כמה עמודות בעלות גודל מינימלי נחזיר את העמודה שמשפיעה על יותר עמודות
    affect=0
    keep_v=d_min[0]
    for i in d_min: #:עבור כל עמודה בעלת דומיין מינימלי
        count_i=0
        for j in CSProblem.list_of_influenced_vars(p, i): #עבור על העמודות שלא עודכנו
            for x in CSProblem.domain(p, j):#בדוק האם יתקיים עדכון והעלה את המונה
                if not CSProblem.is_consistent(p, j, i, x, CSProblem.get_val(p, i)):
                    count_i += 1
                    break #עדכון אחד עבור כל עמודה שתעודכן
        if count_i > affect:#שמירת העמודה שמשפיעה על יותר עמודות אחרות
            affect = count_i
            keep_v = i
    return keep_v
    
           
def propagate_constraints(p, v):
#מחיקת ערכים לפי אילוצים בדומיינים של שאר העמודות לאחר שנבחר ערך לעמודה עליה הופעלה הפונקציה
    for i in CSProblem.list_of_influenced_vars(p, v):
        for x in CSProblem.domain(p, i):
            if not CSProblem.is_consistent(p, i, v, x, CSProblem.get_val(p, v)):
                CSProblem.erase_from_domain(p, i, x)
        
    
    
solve(100)
"""
לפני שינוי: לקח למחשב פחות משניה למצוא פתרון אפשרי
כששיניתי את הלוח לגודל 20 לקח למחשב 30 שניות לעשות זאת
לקח למחשב פחות משניה למצוא פתרון next_var אחרי עדכון הפונקציה
לכן העליתי את גודל הלוח ל30 ואז ל50, והוא פתר את הבעיה תוך פחות משניה
אז הגדלתי את הלוח ל100
כעת לוקח למחשב 35 שניות למצוא פתרון
המחשב פתר את הבעיה תוך 5 שניות sorted_domain אחרי עדכון הפונקציה
:) מסקנה: הפונקציות כתובות טוב ומבצעות את תפקידן כראוי 
"""


        
