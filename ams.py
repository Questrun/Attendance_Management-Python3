import sys
import mysql.connector
global admnos
admnos=[]


def connect():
    con=mysql.connector.connect(host='localhost',database='database',user='username',password='password')
    return con
            
def addstudent():
    global admnos
    con=connect()
    cursor=con.cursor()
    admno=input('enter admission number=')
    admnos.append(admno)
    rno=int(input('enter roll number='))
    sname=input("enter student name=")
    standard=int(input('enter class='))
    section=input('enter section=')
    aadharno=input("enter aadhar number=")
    fname=input("enter father's name=")
    qry="insert into student_rec values({},{},'{}',{},'{}',{},'{}')".format(admno,rno,sname,standard,section,aadharno,fname)
    cursor.execute(qry)
    con.commit()
    cursor.close()
    cursor1=con.cursor()
    cursor1.execute("insert into atten_rec (admno) values (%s)"%(admno))
    con.commit()
    cursor1.close()
    con.close()
    print("STUDENT ADDED SUCCESSFULL")
    
def deleterecord():
    global admnos
    admno=input("enter admission number to be deleted:")
    con=connect()
    cursor=con.cursor()
    qry="delete from student_rec where admno={}".format(admno)
    cursor.execute(qry)
    Y="delete from atten_rec where admno={}".format(admno)
    cursor.execute(Y)
    con.commit()
    for x in admnos:
        if x == admno:
            admnos.remove(admno)
            print("RECORD DELETED")
        
def display():
    con=connect()
    cursor=con.cursor()
    qry="select * from student_rec"
    cursor.execute(qry)
    n=cursor.fetchall()
    print('='*70)
    for x in n:
        print('addmision number:',x[0])
        print('roll number:',x[1])
        print('student name:',x[2])
        print('class:',x[3])
        print('section:',x[4])
        print('aadhar number:',x[5])
        print('fathers name:',x[6])
        print('='*70)
                
def searchrecord():
    admno=input("enter admission number to be searched:")
    t=not_in_admnos(admno)
    if t == False :
        return
    con=connect()
    cursor=con.cursor()
    qry="select rollno,sname,standard,section,aadharno,fname from student_rec where admno={}".format(admno)
    cursor.execute(qry)
    n=cursor.fetchone()
    for x in n:
        print(x)
    print('='*70)
    
def not_in_admnos(admno):
    for x in admnos:
        if x == admno:
            return True
    print("Record not found")
    return False

def attendance():
    global admnos
    d=input('enter date(ddmm):')
    con=connect()
    cursor=con.cursor()
    qry="alter table atten_rec add column if not exists d{} char".format(d)
    cursor.execute(qry)
    while True:
                    global admnos
                    admno=input('enter admission number to mark attendence:')
                    t=not_in_admnos(admno)
                    if t == False :
                        break
                    att=input('mark attendance(A/P):')
                    qryy="update atten_rec set d{}='{}' where admno={}".format(d,att,admno)
                    cursor.execute(qryy)
                    con.commit()
                    cont=input('Do you want to continue(y/n):')
                    if cont=="n":
                        break
                    if(cont != "y" and cont != "n"):
                        print('INVALID INPUT')

def check_atten_rec():
    global admnos
    admno=input("enter admission number to be searched:")
    t=not_in_admnos(admno)
    if t == False :
        return
    month=int(input("Enter month in mm format to check attendance record for:"))
    conn=connect()
    cursor=conn.cursor(buffered=True)
    qry="select * from atten_rec where admno={}".format(admno)
    cursor.execute(qry)
    dobj=cursor.fetchall()
    darr=dobj[0]
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    conn.commit()
    cursor.close()
    conn.close()
    countp=0
    counta=0
    thirty_one=[1,3,5,7,8,10,12]
    #print("Running")
    for x in range(1,num_fields-1):
        d=field_names[x]
        print(darr[x])
        mm=d[3:]
        dd=d[1:3]
        if int(mm) == month and darr[x] == "P" :
           countp=countp+1
        if int(mm) == month and darr[x] == "A" :
           counta=counta+1
        #print(mm)
        #print(dd)
    print("Present:%s"%(countp))
    print("Absent:%s"%(counta))
    #print("Running")
    if month in thirty_one:
         print("Holidays:%s"%(31-(counta+countp)))
    elif month == 2:
         print("Holidays:%s"%(28-(counta+countp)))
    else:
         print("Holidays:%s"%(30-(counta+countp)))
    #print(field_names)
    #print(dobj)
        
print ("Welcome to Attendance Management Python 3.9 CLI") #Greetings
print ("Developed by Student Name Class School") # Program Info
try:
    con=connect()
    cursor=con.cursor()
    cursor.execute("create table if not exists student_rec (admno text UNIQUE,rollno int,sname text,standard text,section char,aadharno text,fname text)")
    cursor.execute("create table if not exists atten_rec (admno text UNIQUE)")
    con.commit()
    cursor.close()
    cursor1=con.cursor()
    cursor1.execute("select admno from student_rec")
    dobj=cursor1.fetchall()
    print(dobj)
    for x in dobj:
        admnos.append(x[0])
    con.commit()
    cursor1.close()
    con.close()
                
    while True:
    
    
        print('='*70)
        print('******************** ATTENDANCE MANAGEMENT SYSTEM ********************')
        print('='*70)
        print('***************************** MAIN MENU ******************************')
        print('1.add students')
        print('2.remove student')
        print('3.display all students')
        print('4.search specific student')
        print('5.mark attendance')
        print('6.check attendance')
        print('7.exit')
        print('='*70)

    
        c=int(input('enter choice='))

        if c==1:
            addstudent()
                        
        elif c==2:
            deleterecord()
        
        elif c==3:
            display()
        
        elif c==4:
            searchrecord()
        
        elif c==5:
            attendance()

        elif c==6:
            check_atten_rec()
                                        
        elif c==7:
            print('~EXITING...')
            sys.exit()
        else:
            print('INVALID CHOICE')
        print(admnos)
except Exception as e:
    print("Something went wrong "+str(e)+"\n")
    exit()
print ("Exiting.... Have a nice day!")
