from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk 
from tkinter import messagebox
from validate_email import validate_email
import mysql.connector
import random
import re
import datetime
import xlsxwriter


mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="lib")
mycursor=mydb.cursor()
mycursor.execute("create table if not exists accounts(name varchar(500),dob varchar(500),rollno BIGINT, branch varchar(500), sem varchar(500), phoneno BIGINT, address varchar(500), username varchar(500), password varchar(500), date varchar(500),ibn1 varchar(500),ibi1 BIGINT,ibid1 varchar(500),ibrd1 varchar(500),ibn2 varchar(500),ibi2 BIGINT,ibid2 varchar(500),ibrd2 varchar(500),ibn3 varchar(500),ibi3 BIGINT,ibid3 varchar(500),ibrd3 varchar(500),ibn4 varchar(500),ibi4 BIGINT,ibid4 varchar(500),ibrd4 varchar(500),photopath varchar(500))")
#mycursor.execute("drop table books")
mycursor.execute("create table if not exists books(bookname varchar(1000),bookno BIGINT,authorname varchar(1000), category varchar(1000), edition varchar(1000),publisher varchar(1000), quantity BIGINT, price BIGINT,instock BIGINT)")
def maxbooks(sr):
    mycursor.execute( "SELECT * FROM accounts WHERE rollno = %s  or rollno = %s",(sr,sr))
    c=mycursor.fetchone()
    if c[10]==None or c[14]==None or c[18]==None or c[22]==None :
        return False
    else:
        return True
def globalbooksxist(bni):
    booknid=-1
    try:
        booknid=int(bni)
    except ValueError:
        booknid=-1
    mycursor.execute( "SELECT * FROM books WHERE bookno = %s or bookname= %s",(booknid,bni))
    cc=mycursor.fetchall()
    if len(cc)==0:
       return True
    else:
       return False
def rollexi(sr):
    mycursor.execute( "SELECT * FROM accounts WHERE rollno = %s  or rollno = %s",(sr,sr))
    c=mycursor.fetchone()
    if c == None:
        return True
    else:
        return False

def logout(root):
    if messagebox.askokcancel("Quit", "Do you Want Log Out?",parent=root):
        root.destroy()
        
def close_main(root):#to close main window with warning
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
def lib_pass_eval(u,p,root):
    
    if(u.get()=="admin@admin.com" and p.get()=="admin"):
    #if(u.get()=="" and p.get()==""):
        u.delete(0, END)
        p.delete(0, END)
        lib_menu()
    else:
        root2 = Tk()
        root2.withdraw()
        messagebox.showwarning("Warning", "Invalid username or password",parent=root)
        
def stu_pass_eval(u,p,root):
    uu=u.get()
    pp=p.get()
    mycursor.execute( "SELECT * FROM accounts WHERE username = %s and password = %s",(uu,pp))
    c=mycursor.fetchone()
    if c==None:
        root2 = Tk()
        root2.withdraw()
        messagebox.showwarning("Warning", "Invalid username or password",parent=root)
    else:
        u.delete(0, END)
        p.delete(0, END)
        stu_menu(uu,pp)
def pass_valid(password):
    flag = 0
    while True: 
            if (len(password)<8): 
                    flag = -1
                    break
            elif not re.search("[a-z]", password): 
                    flag = -1
                    break
            elif not re.search("[A-Z]", password): 
                    flag = -1
                    break
            elif not re.search("[0-9]", password): 
                    flag = -1
                    break
            elif not re.search("[_@$]", password): 
                    flag = -1
                    break
            elif re.search("\s", password): 
                    flag = -1
                    break
            else: 
                    return False 
    if flag ==-1: 
        return True
def stu_exist(u,p,r):
    try:
        p=int(p)
        r=int(r)
        mycursor.execute( "SELECT * FROM accounts WHERE username = %s  or rollno = %s",(u,int(r)))
        c=mycursor.fetchone()
        if c == None:
            return False
        else:
            return True
    except:
        return False
def lib_menu():
    def returnbookf3(sp,bp,fine,button1):
        mycursor.execute("UPDATE books SET instock =%s WHERE bookno =%s",(bp[8]+1,bp[1]))
        mydb.commit()
        if sp[11]==bp[1]:
            mycursor.execute("UPDATE accounts SET ibn1 = %s, ibi1 = %s, ibid1 = %s, ibrd1 = %s WHERE rollno = %s ",(None,None,None,None,sp[2]))
            mydb.commit()
        elif sp[15]==bp[1]:
            mycursor.execute("UPDATE accounts SET ibn2 = %s, ibi2 = %s, ibid2 = %s, ibrd2 = %s WHERE rollno = %s ",(None,None,None,None,sp[2]))
            mydb.commit()
        elif sp[19]==bp[1]:
            mycursor.execute("UPDATE accounts SET ibn3 = %s, ibi3 = %s, ibid3 = %s, ibrd3 = %s WHERE rollno = %s ",(None,None,None,None,sp[2]))
            mydb.commit()
        else:
            mycursor.execute("UPDATE accounts SET ibn4 = %s, ibi4 = %s, ibid4 = %s, ibrd4 = %s WHERE rollno = %s ",(None,None,None,None,sp[2]))
            mydb.commit()
        if fine >0:
            messagebox.showinfo("Info", "The Book Has Been Returned Successfully\nThe fine Has is Rs "+str(fine)+"/-",parent=root)
        else:
            messagebox.showinfo("Info", "The Book Has Been Returned Successfully",parent=root)
        w.delete(button1)
    def returnbookf2(idnog,idno,newroot,c,sr):
        if idnog=="":
            messagebox.showwarning("Warning", "All Fields Are Mandatory",parent=newroot)
        elif not str.isdigit(idnog):
            messagebox.showwarning("Warning", "Invalid Book No.",parent=newroot)
        elif c[11]!=int(idnog) and c[15]!=int(idnog) and c[19]!=int(idnog) and c[23]!=int(idnog):
             messagebox.showwarning("Warning", "Provide The Book No. Among The Issued Books",parent=newroot)
        else:
            idno.delete(0, END)
            idno.insert(0, "")
            newroot.destroy()
            mycursor.execute("SELECT * FROM accounts WHERE rollno = %s and rollno = %s",(int(sr),int(sr)))
            sp=mycursor.fetchone()
            mycursor.execute("SELECT * FROM books WHERE bookno = %s and bookno = %s",(int(idnog),int(idnog)))
            bp=mycursor.fetchone()
            k=datetime.date(int(sp[13][0:4]), int(sp[13][5:7]), int(sp[13][8:10]) )
            kk=datetime.datetime.now().date()
            fine=(kk-k).days
            if fine <=0:
                fine=0
            if sp[11]==int(idnog):
                m=11
            elif sp[15]==int(idnog):
                m=15
            elif sp[19]==int(idnog):
                m=19
            else:
                m=23
            w.delete("all")
            w.create_text(320,50,fill="slateblue", font="Calibri 35  ",text="Book Return Details  ")
            w.create_text(300,110,fill="light blue", font="Calibri 20  ",text="Studnet Name     :"+sp[0])
            w.create_text(300,140,fill="light blue", font="Calibri 20  ",text="Student Roll No.    :"+str(sp[2]))
            w.create_text(300,180,fill="light blue",font="Calibri 20  ",text="Book Name  :"+bp[0])
            w.create_text(300,220,fill="light blue",font="Calibri 20  ",text="Book Id No.   :"+str(bp[1]))
            w.create_text(300,260,fill="light blue",font="Calibri 20  ",text="Issued Date     :"+sp[m+1])
            w.create_text(300,300,fill="light blue",font="Calibri 20  ",text="Return Date :"+sp[m+1])
            w.create_text(300,340,fill="light blue",font="Calibri 20  ",text="Returning Date :"+str(kk))
            w.create_text(300,380,fill="red",font="Calibri 20  ",text="Fine :"+str(fine))
            button1 = Button( root,text = "Return",  anchor = W,command=lambda :returnbookf3(sp,bp,fine,button1_window))
            button1.configure(width = 15,height=1,  relief = FLAT,anchor=CENTER,bg="yellow")
            button1_window = w.create_window(240,400, anchor=NW, window=button1)







            
            

             
    def returnbookfinal(sr):
        global clicc
        clicc=False
        def callback(event):
            global clicc
            if clicc == False:
                idno.delete(0, END)         
                idno.config(fg = "black")
                clicc=True
        if sr=="":
            messagebox.showwarning("Warning", "All Fields Are Mandatory",parent=root)
        elif not str.isdigit(sr):
            messagebox.showwarning("Warning", "Invalid Roll No.",parent=root)
        elif rollexi(int(sr)):
            messagebox.showwarning("Warning", "Roll No. Does Not Exist",parent=root)
        else:
            mycursor.execute( "SELECT * FROM accounts WHERE rollno = %s and rollno = %s",(int(sr),int(sr)))
            c=mycursor.fetchone()
            if c[10]==None and c[14]==None and c[18]==None and c[22]==None :
                messagebox.showwarning("Warning", "No Books Are Issued On Your Behalf",parent=root)
            else:
                newroot=Tk()
                newroot.configure(background="burlywood3")
                newroot.overrideredirect(True)
                newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))

                close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
                close_win.place(x=1322, y=0, width=45)
                    
                labelfont = ('times', 30,"italic", 'bold')
                head_label=Label(newroot,text="Books Issued",bg="burlywood3",fg="brown",font=labelfont)
                head_label.grid(row=0, column=0,columnspan=3,sticky=W)
                k=0
                count=0
                m=2
                labelfont = (10)
                Label(newroot,text="",bg="burlywood3",fg="brown",font=labelfont).grid(row=1,column=0,rowspan=2)
                while(k<16):
                    if c[10+k]!=None:
                        m=m+1
                        Label(newroot,text=str(count+1),bg="burlywood3",fg="brown",font=labelfont).grid(row=m,column=0)
                        Label(newroot,text="Book Name",bg="burlywood3",fg="brown",font=labelfont).grid(row=m,column=1)
                        Label(newroot,text=":"+str(c[10+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m,column=2,sticky=W)
                        Label(newroot,text="Book Id No.",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+1,column=1)
                        Label(newroot,text=":"+str(c[11+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m+1,column=2,sticky=W)
                        Label(newroot,text="Issued Date",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+2,column=1)
                        Label(newroot,text=":"+str(c[12+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m+2,column=2,sticky=W)
                        Label(newroot,text="Return Date",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+3,column=1)
                        Label(newroot,text=":"+str(c[13+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m+3,column=2,sticky=W)
                        Label(newroot,text="",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+8,column=0,rowspan=2)
                    k=k+4
                    m=m+9
                    count=count+1
                Label(newroot,text="",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+8,column=0,rowspan=2)    
                idno=Entry(newroot,fg="gray")
                idno.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
                idno.insert(0, "Enter Book Id No.")           # Set default text at cursor position 0.
                retbook=Button(newroot,text="Return",bg="red",command= lambda :returnbookf2(idno.get(),idno,newroot,c,sr))
                idno.place(x=500,y=300)
                retbook.place(x=535,y=325)

            
    def returnbook(w):
        w.delete("all")
        global clic
        clic=False
        def callback(event):
            global clic
            if clic == False:
                rollno.delete(0, END)         
                rollno.config(fg = "black")
                clic=True
        rollno=Entry(root,fg="gray")
        rollno.configure(width = 30, relief = FLAT)
        rollno_window = w.create_window(320,40, anchor=NW, window=rollno)

        button1 = Button( root,text = "Submit",  anchor = W,command=lambda :returnbookfinal(rollno.get()))
        button1.configure(width = 15,height=1,  relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(530,40, anchor=NW, window=button1)
        rollno.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
        rollno.insert(0, "Enter Roll No.")           # Set default text at cursor position 0.

    def studentlist(w):

        def stuex(event):
            try:
                mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="lib")
                mycursor=mydb.cursor()
                mycursor.execute("create table if not exists accounts(name varchar(1000),dob varchar(1000),rollno BIGINT, branch varchar(1000), sem varchar(1000), phoneno BIGINT, address varchar(1000), username varchar(1000), password varchar(1000), date varchar(1000))")

                mycursor.execute("SELECT * FROM accounts")
                c=mycursor.fetchall()
                workbook = xlsxwriter.Workbook('accounts.xlsx')
                worksheet = workbook.add_worksheet()
                row=0
                col=0
                worksheet.write(row, col,  "Name")
                worksheet.write(row, col+1,  "D.O.B")
                worksheet.write(row, col+2,  "Roll No.")
                worksheet.write(row, col+3,  "Branch")
                worksheet.write(row, col+4,  "SEM/YEAR")
                worksheet.write(row, col+5,  "Phone No.")
                worksheet.write(row, col+6,  "Address")
                worksheet.write(row, col+7,  "Username")
                worksheet.write(row, col+8,  "Password")
                worksheet.write(row, col+9,  "Date")
                worksheet.write(row, col+10,  "book_name1")
                worksheet.write(row, col+11,  "book_id1")
                worksheet.write(row, col+12,  "book_issdate1")
                worksheet.write(row, col+13,  "book_retdate1")
                worksheet.write(row, col+14,  "book_name2")
                worksheet.write(row, col+15,  "book_id2")
                worksheet.write(row, col+16,  "book_issdate2")
                worksheet.write(row, col+17,  "book_retdate2")
                worksheet.write(row, col+18,  "book_name3")
                worksheet.write(row, col+19,  "book_id3")
                worksheet.write(row, col+20,  "book_issdate3")
                worksheet.write(row, col+21,  "book_retdate3")
                worksheet.write(row, col+22,  "book_name4")
                worksheet.write(row, col+23,  "book_id4")
                worksheet.write(row, col+24,  "book_issdate4")
                worksheet.write(row, col+25,  "book_retdate4")
                worksheet.write(row, col+26,  "PhotoPath")
                col=0
                row=1
                for x in c:
                    for i in x:
                        if i==None:
                            i="None"
                        worksheet.write(row, col,  i)
                        col=col+1
                    row=row+1
                    col=0
                workbook.close()
                #root2=Tk()
                #root2.withdraw()
                messagebox.showinfo("Info", "The Student List Has Been Downloaded In The Form Of EXCEL Sheet In Your Working Directory",parent=newroot)

            except:
                #root2=Toplevel()
                #root2.withdraw()
                messagebox.showwarning("Warning", "The Student List EXCEL Sheet Is Opened Somewhere\nCannot Do Changes\nClose The EXCEL Sheet And Try Again",parent=newroot)


        newroot=Tk()
        newroot.configure(background="burlywood3")
        newroot.overrideredirect(True)
        newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))
        mycursor.execute( "SELECT * FROM accounts ")
        det=mycursor.fetchall()
        
        close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
        close_win.place(x=1322, y=0, width=45)

        labelfont = ('times', 30,"italic", 'bold')
        head_label=Label(newroot,text="Students List",bg="burlywood3",fg="brown",font=labelfont)
        head_label.grid(row=0, column=0,columnspan=3,sticky=W)
        Label(newroot,text="S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=0,sticky=W)
        Label(newroot,text="Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=1,sticky=W)
        Label(newroot,text="D.O.B  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=2,sticky=W)
        Label(newroot,text="Roll No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=3,sticky=W)
        Label(newroot,text="Branch ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=4,sticky=W)
        Label(newroot,text="SEM/YEAR  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=5,sticky=W)
        Label(newroot,text="Contact No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=6,sticky=W)
        Label(newroot,text="Email ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=7,sticky=W)
        m=0
        labelfont = (10)
        for i in det:
            m=m+1
            newl1=Label(newroot,text=str(m)+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0,sticky=W)
            newl2=Label(newroot,text=i[0]+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1,sticky=W)
            newl3=Label(newroot,text=str(i[1])+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2,sticky=W)
            newl4=Label(newroot,text=str(i[2])+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3,sticky=W)
            newl5=Label(newroot,text=i[3]+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4,sticky=W)
            newl6=Label(newroot,text=i[4]+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5,sticky=W)
            newl7=Label(newroot,text=str(i[5])+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6,sticky=W)
            newl8=Label(newroot,text=str(i[7])+"        ",bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7,sticky=W)

        Label(newroot,text="\n",bg="burlywood3",fg="royalblue",font=10).grid(row=m+2,column=7,sticky=W)            
        labell=Label(newroot,text="Click Here To Download The Student List As EXCEL Sheet ",bg="burlywood3",fg="royalblue",font=10)
        labell.grid(row=m+3,column=0,columnspan=8,sticky=W)
        labell.bind("<Button-1>", stuex)
        
    def issubookfinal(sr,bi,w,j=0):
        if j!=0:
            j.destroy()
        if sr=="" or bi=="":
            messagebox.showwarning("Warning", "All Fields Are Mandatory",parent=root)
        elif not str.isdigit(sr):
            messagebox.showwarning("Warning", "Invalid Roll No.",parent=root)
        elif rollexi(int(sr)):
            messagebox.showwarning("Warning", "Roll No. Does Not Exist",parent=root)
        elif globalbooksxist(bi):
            messagebox.showwarning("Warning", "No Book Exist With Given BookName Or BookId No. ",parent=root)
        elif maxbooks(sr):
            messagebox.showwarning("Warning", "The Student Have Already Issued 4 Books\nOnly Maximum Of 4 Can Be Issued To A Student ",parent=root)   
        else:
            isd = str(datetime.datetime.now().date())
            rtd = str(datetime.datetime.now().date() + datetime.timedelta(30))
            booknid=-1
            try:
                booknid=int(bi)
            except ValueError:
                booknid=-1
            mycursor.execute( "SELECT * FROM books WHERE bookno = %s or bookname= %s",(booknid,bi))
            x=mycursor.fetchall()
            if len(x)==1:
                for cc in x:
                    if cc[8]==0:
                        messagebox.showinfo("Info", "The Book You Have Requested Is Out Of Stock\nBook Name : "+cc[0]+"\nBook No. : "+str(cc[1]),parent=root)
                        w.delete("all")
                        w.create_text(490,50,fill="slateblue", font="Calibri 25  ",text="The Book You Have Requested Is Likely To Be Returned By The Students\n On The Following Dates")
                        mycursor.execute( "SELECT * FROM accounts WHERE ibi1 = %s  or ibi1 = %s",(cc[1],cc[1]))
                        kk=mycursor.fetchall()
                        ll=150
                        for jj in kk:
                            w.create_text(340,ll,fill="light blue", font="Calibri 20  ",text=jj[13])
                            ll=ll+30

                        mycursor.execute( "SELECT * FROM accounts WHERE ibi2 = %s  or ibi2 = %s",(cc[1],cc[1]))
                        kk=mycursor.fetchall()
                        for jj in kk:
                            w.create_text(340,ll,fill="light blue", font="Calibri 20  ",text=jj[17])
                            ll=ll+30
                            
                        mycursor.execute( "SELECT * FROM accounts WHERE ibi3 = %s  or ibi3 = %s",(cc[1],cc[1]))
                        kk=mycursor.fetchall()
                        for jj in kk:
                            w.create_text(340,ll,fill="light blue", font="Calibri 20  ",text=jj[21])
                            ll=ll+30

                        mycursor.execute( "SELECT * FROM accounts WHERE ibi4 = %s  or ibi4= %s",(cc[1],cc[1]))
                        kk=mycursor.fetchall()
                        for jj in kk:
                            w.create_text(340,ll,fill="light blue", font="Calibri 20  ",text=jj[25])
                            ll=ll+30
                        
                    else:
                        mycursor.execute( "SELECT * FROM accounts WHERE rollno = %s  or rollno = %s",(sr,sr))
                        c=mycursor.fetchone()
                        if cc[1]==c[11] or cc[1]==c[15] or cc[1]==c[19] or cc[1]==c[23] :
                            messagebox.showinfo("Info", "Same Books Cannot Be Issued To a Student \nBook Name : "+cc[0]+"\nBook No. : "+str(cc[1]),parent=root)
                        else:
                            if c[10]==None:
                                mycursor.execute("UPDATE accounts SET ibn1 = %s, ibi1 = %s, ibid1 = %s, ibrd1 = %s WHERE rollno = %s ",(cc[0],cc[1],isd,rtd,sr))
                                mydb.commit()
                            elif c[14]==None:
                                mycursor.execute("UPDATE accounts SET ibn2 = %s, ibi2 = %s, ibid2 = %s, ibrd2 = %s WHERE rollno = %s ",(cc[0],cc[1],isd,rtd,sr))
                                mydb.commit()
                            elif c[18]==None:
                                mycursor.execute("UPDATE accounts SET ibn3 = %s, ibi3 = %s, ibid3 = %s, ibrd3 = %s WHERE rollno = %s ",(cc[0],cc[1],isd,rtd,sr))
                                mydb.commit()
                            else:
                                mycursor.execute("UPDATE accounts SET ibn4 = %s, ibi4 = %s, ibid4 = %s, ibrd4 = %s WHERE rollno = %s ",(cc[0],cc[1],isd,rtd,sr))
                                mydb.commit()

                            w.delete("all")
                            w.create_text(320,50,fill="slateblue", font="Calibri 35  ",text="Book Issue Details  ")
                            w.create_text(300,110,fill="light blue", font="Calibri 20  ",text="Studnet Name     :"+c[0])
                            w.create_text(300,140,fill="light blue", font="Calibri 20  ",text="Student Roll No.    :"+str(c[2]))
                            w.create_text(300,180,fill="light blue",font="Calibri 20  ",text="Book Name  :"+cc[0])
                            w.create_text(300,220,fill="light blue",font="Calibri 20  ",text="Book Id No.   :"+str(cc[1]))
                            w.create_text(300,260,fill="light blue",font="Calibri 20  ",text="Issued Date     :"+isd)
                            w.create_text(300,300,fill="light blue",font="Calibri 20  ",text="Return Date :"+rtd)
                            messagebox.showinfo("Info", "The Book Has Been Issued Successfully",parent=root)
                            mycursor.execute("UPDATE books SET instock = %s WHERE bookno = %s ",(cc[8]-1,cc[1]))
                            mydb.commit()
                
            else:
                newroot=Tk()
                newroot.configure(background="burlywood3")
                newroot.overrideredirect(True)
                newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))

                close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
                close_win.place(x=1322, y=0, width=45)
                
                labelfont = ('times', 30,"italic", 'bold')
                labelfont2 = ('times', 20,"italic", 'bold')
                head_label=Label(newroot,text="Search Results",bg="burlywood3",fg="brown",font=labelfont)
                head_label.grid(row=0, column=0,columnspan=3,sticky=W)
                Label(newroot,text="Multiple Books Are Found With Same Name. Enter The Book Id No. Below To Issue The specific Book",bg="burlywood3",fg="brown",font=labelfont2).grid(row=1, column=0,columnspan=10,sticky=W)
                Label(newroot,text="  S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=0)
                Label(newroot,text="  Book Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=1)
                Label(newroot,text="  Book Id No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=2)
                Label(newroot,text="  Author Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=3)
                Label(newroot,text="  Category  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=4)
                Label(newroot,text="  Edition  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=5)
                Label(newroot,text="  Publisher  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=6)
                Label(newroot,text="  Quantity  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=7)
                Label(newroot,text="  Price  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=8)
                Label(newroot,text="  In Stock  ",bg="burlywood3",fg="royalblue",font=10).grid(row=2,column=9)
                m=1
                labelfont = (10)
                for i in x:
                    m=m+1
                    newl1=Label(newroot,text=str(m-1),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0)
                    newl2=Label(newroot,text=i[0],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1)
                    newl3=Label(newroot,text=str(i[1]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2)
                    newl4=Label(newroot,text=i[2],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3)
                    newl5=Label(newroot,text=i[3],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4)
                    newl6=Label(newroot,text=i[4],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5)
                    newl7=Label(newroot,text=i[5],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6)
                    newl8=Label(newroot,text=str(i[6]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7)
                    newl9=Label(newroot,text=str(i[7]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=8)
                    newl10=Label(newroot,text=str(i[8]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=9)
                bookidno=Entry(newroot)
                sub=Button(newroot,text="Issue",fg="black",bg="red",command=lambda :issubookfinal(sr,bookidno.get(),w,newroot))
                Label(newroot,text="\n",bg="burlywood3").grid(row=m+2,column=4)
                bookidno.grid(row=m+4,column=4,columnspan=2)
                sub.grid(row=m+6,column=4,columnspan=2)   
                        
            
            
    def issuebook(w):
   
        w.delete("all")
        global click
        click=False
        def callback(event):
            global click
            if click == False:
                category.delete(0, END)         
                category.config(fg = "black")
                click=True

        w.create_text(410,150,fill="aquamarine2", font="Calibri 35  ",text="Enter The Details Below")
        w.create_text(285,210,fill="yellow3", font="Calibri 20  ",text="Student Roll No.")
        w.create_text(300,250,fill="yellow3", font="Calibri 20  ",text="Book Name/Id No.")

        student_name=Entry(root,bg = "light cyan")
        student_name.configure(width = 30, relief = FLAT)
        student_name_window = w.create_window(415,205, anchor=NW, window=student_name)

        book_name=Entry(root,bg ="light cyan")
        book_name.configure(width = 30, relief = FLAT)
        book_name_window = w.create_window(415,245, anchor=NW, window=book_name)
        
        button1 = Button( root,text = "Issue Book",  anchor = W,command=lambda :issubookfinal(student_name.get(),book_name.get(),w))        
        button1.configure(width = 15,height=1, relief = FLAT,anchor=CENTER,bg="tan2")
        button1_window = w.create_window(355,283, anchor=NW, window=button1)
        
    
    def book_exist_for_del(w,root,bookni,j):
        
        def delbookfinal(idn,qn,i,idnum,qnum):
            def idexi():
                for k in i:
                    if int(idn) == k[1]:
                        return False
                return True

            def valq():
                for k in i:
                    if int(idn) == k[1] and int(qn)>k[8]:
                        return True
                    return False
            
            if(idn=="" or qn=="" or idn=="Enter The Quantity" or qn=="Enter The Quantity"):
                messagebox.showwarning("Warning", "Please Enter The Details",parent=newroot)
            elif (not str.isdigit(idn) or not str.isdigit(qn)):
                messagebox.showwarning("Warning", "Invalid Id No. or Quantty No.",parent=newroot)
            elif (idexi()):
                messagebox.showwarning("Warning", "Enter The Correct Id No.",parent=newroot)
            elif (valq()):
                messagebox.showwarning("Warning", "The quantity Is Out Of Range",parent=newroot)
            else:
                 mycursor.execute( "SELECT * FROM books WHERE bookno = %s and bookno = %s",(int(idn),int(idn)))
                 cc=mycursor.fetchone()
                 if int(qn)==cc[6]:
                                   mycursor.execute("DELETE FROM books WHERE bookno = %s and bookno = %s",(int(idn),int(idn)))
                                   mydb.commit()
                                   messagebox.showinfo("Info", "Book Has Been Deleted Permanently",parent=newroot)
                                   newroot.destroy()
                                   w.delete("all")
                                   w.create_text(360,200,fill="slateblue", font="Calibri 25  ",text="The Book Has Been Deleted Permanently")
                                   
                                  
                 else:
                                   mycursor.execute("UPDATE books SET quantity =%s,instock=%s WHERE bookno = %s",((cc[6]-int(qn)),(cc[8]-int(qn)),int(idn)))
                                   mydb.commit()
                                   messagebox.showinfo("Info", "The Quantity Of The Book Has Been Reduced Succesfully",parent=newroot)
                                   newroot.destroy()
                                   mycursor.execute("SELECT * FROM books WHERE bookno = %s and bookno = %s",(int(idn),int(idn)))
                                   p=mycursor.fetchone()
                                   w.delete("all")
                                   w.create_text(350,50,fill="slateblue", font="Calibri 25  ",text="After Reducing The Quantity Book Details Are  ")
                                   w.create_text(300,110,fill="light blue", font="Calibri 20  ",text="Book Name     :"+p[0])
                                   w.create_text(300,150,fill="light blue", font="Calibri 20  ",text="Book Id  No.    :"+str(p[1]))
                                   w.create_text(300,190,fill="light blue",font="Calibri 20  ",text="Author Name  :"+p[2])
                                   w.create_text(300,230,fill="light blue",font="Calibri 20  ",text="Category   :"+p[3])
                                   w.create_text(300,270,fill="light blue",font="Calibri 20  ",text="Edition     :"+str(p[4]))
                                   w.create_text(300,310,fill="light blue",font="Calibri 20  ",text="Publisher :"+p[5])
                                   w.create_text(300,350,fill="light blue",font="Calibri 20  ",text="Quantity :"+str(p[6]))
                                   w.create_text(300,390,fill="light blue",font="Calibri 20  ",text="Price :"+str(p[7]))
                                   w.create_text(300,430,fill="light blue",font="Calibri 20  ",text="Instock :"+str(p[8]))
                                   
                
        global clickk
        clickk=False
        def callback(event):
            global clickk
            if clickk == False:
                idnum.delete(0, END)         
                idnum.config(fg = "black")
                clickk=True

        global clickk2
        clickk2=False
        def callback2(event):
            global clickk2
            if clickk2 == False:
                qnum.delete(0, END)         
                qnum.config(fg = "black")
                clickk2=True
                
        booknid=-1
        try:
            booknid=int(bookni)
        except ValueError:
            booknid=-1
        mycursor.execute( "SELECT * FROM books WHERE bookno = %s or bookname= %s",(booknid,bookni))
        cc=mycursor.fetchall()
        if len(cc)==0:
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "No Book Exist With Given BookName Or BookId No. ",parent=root)
        else:
            newroot=Tk()
            newroot.configure(background="burlywood3")
            newroot.overrideredirect(True)
            newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))

            close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
            close_win.place(x=1322, y=0, width=45)
            
            labelfont = ('times', 30,"italic", 'bold')
            head_label=Label(newroot,text="Search Results",bg="burlywood3",fg="brown",font=labelfont)
            head_label.grid(row=0, column=0,columnspan=3,sticky=W)
            Label(newroot,text="  S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=0)
            Label(newroot,text="  Book Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=1)
            Label(newroot,text="  Book Id No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=2)
            Label(newroot,text="  Author Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=3)
            Label(newroot,text="  Category  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=4)
            Label(newroot,text="  Edition  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=5)
            Label(newroot,text="  Publisher  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=6)
            Label(newroot,text="  Quantity  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=7)
            Label(newroot,text="  Price  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=8)
            Label(newroot,text="  In Stock  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=9)
            m=0
            labelfont = (10)
            for i in cc:
                m=m+1
                newl1=Label(newroot,text=str(m),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0)
                newl2=Label(newroot,text=i[0],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1)
                newl3=Label(newroot,text=str(i[1]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2)
                newl4=Label(newroot,text=i[2],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3)
                newl5=Label(newroot,text=i[3],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4)
                newl6=Label(newroot,text=i[4],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5)
                newl7=Label(newroot,text=i[5],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6)
                newl8=Label(newroot,text=str(i[6]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7)
                newl9=Label(newroot,text=str(i[7]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=8)
                newl10=Label(newroot,text=str(i[8]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=9)
            mycursor.execute( "SELECT * FROM books WHERE bookno = %s or bookname= %s",(booknid,bookni))
            cc=mycursor.fetchall()
            j.delete(0, END)
            j.insert(0, "")
            idnum=Entry(newroot,fg = "gray")
            idnum.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
            idnum.insert(0, "Enter The Id Number")           # Set default text at cursor position 0.
            qnum=Entry(newroot,fg = "gray")
            qnum.bind("<Button-1>", callback2)   # Bind a mouse-click to the callback function.
            qnum.insert(0, "Enter The Quantity")            # Set default text at cursor position 0.
            sub=Button(newroot,text="Delete",fg="black",bg="red",command=lambda :delbookfinal(idnum.get(),qnum.get(),cc,idnum,qnum))
            Label(newroot,text="\n",bg="burlywood3").grid(row=m+2,column=4)
            idnum.grid(row=m+4,column=4,columnspan=2)
            qnum.grid(row=m+5,column=4,columnspan=2)
            sub.grid(row=m+6,column=4,columnspan=2)
            
    def delbook(w):
        w.delete("all")
        global clickk
        clickk=False
        def callback(event):
            global clickk
            if clickk == False:
                bookname1.delete(0, END)         
                bookname1.config(fg = "black")
                clickk=True
        bookname1=Entry(root,fg="gray")
        bookname1.configure(width = 30, relief = FLAT)
        bookname1_window = w.create_window(320,40, anchor=NW, window=bookname1)

        button1 = Button( root,text = "Search Book",  anchor = W,command=lambda :book_exist_for_del(w,root,bookname1.get(),bookname1))
        button1.configure(width = 15,height=1,  relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(530,40, anchor=NW, window=button1)
        bookname1.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
        bookname1.insert(0, "Enter Book Name Or Book Id No.")           # Set default text at cursor position 0.

        
    def book_exist(w,root,bookni,j):
        booknid=-1
        try:
            booknid=int(bookni)
        except ValueError:
            booknid=-1
        mycursor.execute( "SELECT * FROM books WHERE bookno = %s or bookname= %s",(booknid,bookni))
        cc=mycursor.fetchall()
        if len(cc)==0:
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "No Book Exist With Given BookName Or BookId No. ",parent=root)
        else:
            newroot=Tk()
            newroot.configure(background="burlywood3")
            newroot.overrideredirect(True)
            newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))

            close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
            close_win.place(x=1322, y=0, width=45)
            
            labelfont = ('times', 30,"italic", 'bold')
            head_label=Label(newroot,text="Search Results",bg="burlywood3",fg="brown",font=labelfont)
            head_label.grid(row=0, column=0,columnspan=3,sticky=W)
            Label(newroot,text="  S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=0)
            Label(newroot,text="  Book Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=1)
            Label(newroot,text="  Book Id No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=2)
            Label(newroot,text="  Author Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=3)
            Label(newroot,text="  Category  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=4)
            Label(newroot,text="  Edition  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=5)
            Label(newroot,text="  Publisher  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=6)
            Label(newroot,text="  Quantity  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=7)
            Label(newroot,text="  Price  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=8)
            Label(newroot,text="  In Stock  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=9)
            m=0
            labelfont = (10)
            for i in cc:
                m=m+1
                newl1=Label(newroot,text=str(m),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0)
                newl2=Label(newroot,text=i[0],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1)
                newl3=Label(newroot,text=str(i[1]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2)
                newl4=Label(newroot,text=i[2],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3)
                newl5=Label(newroot,text=i[3],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4)
                newl6=Label(newroot,text=i[4],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5)
                newl7=Label(newroot,text=i[5],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6)
                newl8=Label(newroot,text=str(i[6]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7)
                newl9=Label(newroot,text=str(i[7]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=8)
                newl10=Label(newroot,text=str(i[8]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=9)
            j.delete(0, END)
            j.insert(0, "")  
        
    def searchbook(w):
        w.delete("all")
        global clickk
        clickk=False
        def callback(event):
            global clickk
            if clickk == False:
                bookname1.delete(0, END)         
                bookname1.config(fg = "black")
                clickk=True
        bookname1=Entry(root,fg="gray")
        bookname1.configure(width = 30, relief = FLAT)
        bookname1_window = w.create_window(320,40, anchor=NW, window=bookname1)

        button1 = Button( root,text = "Search Book",  anchor = W,command=lambda :book_exist(w,root,bookname1.get(),bookname1))
        button1.configure(width = 15,height=1,  relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(530,40, anchor=NW, window=button1)
        bookname1.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
        bookname1.insert(0, "Enter Book Name Or Book Id No.")           # Set default text at cursor position 0.

    def booklist():
        def bookex(event):
            try:
                mycursor.execute("SELECT * FROM books")
                c=mycursor.fetchall()
                workbook2 = xlsxwriter.Workbook('books.xlsx')
                worksheet2 = workbook2.add_worksheet()
                row=0
                col=0
                worksheet2.write(row, col,  "Book Name")
                worksheet2.write(row, col+1,  "Book ID No.")
                worksheet2.write(row, col+2,  "Author Name")
                worksheet2.write(row, col+3,  "Category")
                worksheet2.write(row, col+4,  "Addition")
                worksheet2.write(row, col+5,  "Publisher")
                worksheet2.write(row, col+6,  "Quantity")
                worksheet2.write(row, col+7,  "Price")
                worksheet2.write(row, col+8,  "Instock")
                col=0
                row=1
                for x in c:
                    for i in x:
                        if i==None:
                            i="None"
                        worksheet2.write(row, col,  i)
                        col=col+1
                    row=row+1
                    col=0
                workbook2.close()
                #root2=Toplevel()
                #root2.withdraw()
                messagebox.showinfo("Info", "The Book List Has Been Downloaded In The Form Of EXCEL Sheet In Your Working Directory",parent=newroot)

            except:
                #root2=Toplevel()
                #root2.withdraw()
                messagebox.showwarning("Warning", "The Book List EXCEL Sheet Is Opened Somewhere\nCannot Do Changes\nClose The EXCEL Sheet And Try Again",parent=newroot)




            
        newroot=Tk()
        newroot.configure(background="burlywood3")
        newroot.overrideredirect(True)
        newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))
        mycursor.execute( "SELECT * FROM books ")
        det=mycursor.fetchall()
        
        close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
        close_win.place(x=1322, y=0, width=45)

        labelfont = ('times', 30,"italic", 'bold')
        head_label=Label(newroot,text="Book List",bg="burlywood3",fg="brown",font=labelfont)
        head_label.grid(row=0, column=0,columnspan=3,sticky=W)
        Label(newroot,text="  S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=0)
        Label(newroot,text="  Book Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=1)
        Label(newroot,text="  Book Id No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=2)
        Label(newroot,text="  Author Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=3)
        Label(newroot,text="  Category  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=4)
        Label(newroot,text="  Edition  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=5)
        Label(newroot,text="  Publisher  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=6)
        Label(newroot,text="  Quantity  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=7)
        Label(newroot,text="  Price  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=8)
        Label(newroot,text="  In Stock  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=9)
        m=0
        labelfont = (10)
        for i in det:
            m=m+1
            newl1=Label(newroot,text=str(m),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0)
            newl2=Label(newroot,text=i[0],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1)
            newl3=Label(newroot,text=str(i[1]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2)
            newl4=Label(newroot,text=i[2],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3)
            newl5=Label(newroot,text=i[3],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4)
            newl6=Label(newroot,text=i[4],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5)
            newl7=Label(newroot,text=i[5],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6)
            newl8=Label(newroot,text=str(i[6]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7)
            newl9=Label(newroot,text=str(i[7]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=8)
            newl10=Label(newroot,text=str(i[8]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=9)
        
        Label(newroot,text="\n",bg="burlywood3",fg="royalblue",font=10).grid(row=m+2,column=7,sticky=W)            
        labell=Label(newroot,text="Click Here To Download The Book List As EXCEL Sheet ",bg="burlywood3",fg="royalblue",font=10)
        labell.grid(row=m+3,column=0,columnspan=8,sticky=W)
        labell.bind("<Button-1>", bookex)


        
    def addbook(w):
        


        def bookidexi(bi):
            bii=(bi,)
            mycursor.execute( "SELECT * FROM books WHERE bookno = %s ",(bii))
            c=mycursor.fetchone()
            if c == None:
                return False
            else:
                return True
        def bookexi(bn,an,e,pu,pr):
            mycursor.execute( "SELECT * FROM books WHERE bookname = %s and authorname=%s and edition =%s and publisher = %s and price = %s",(bn,an,e,pu,pr))
            c=mycursor.fetchone()
            if c == None:
                return False
            else:
                return True
        def bookexiadd(bn,bi,an,c,e,pu,pr):
            mycursor.execute( "SELECT * FROM books WHERE bookname = %s and bookno =%s and authorname=%s and category =%s and  edition =%s and publisher = %s and price =%s",(bn,int(bi),an,c,e,pu,int(pr)))
            c=mycursor.fetchone()
            if c == None:
                return False
            else:
                return True
            
        def intid(bi):
            try:
                bi=int(bi)
                return False
            except:
                return True
        def inted(e):
            try:
                e=int(e)
                return False
            except:
                return True
        def intqu(q):
            try:
                q=int(q)
                return False
            except:
                return True
        def intpr(pr):
            try:
                pr=int(pr)
                return False
            except:
                return True
        def save_book(bn,bi,an,c,e,pu,q,pr,w):
            if bn=="" or bi=="" or an=="" or c=="" or e=="" or pu=="" or q=="" or pr=="":
                messagebox.showwarning("Warning", "All Fields Are Mandatory",parent=root)

            elif intid(bi):
                messagebox.showwarning("Warning", "Invalid  Id No.",parent=root)

            elif inted(e):
                messagebox.showwarning("Warning", "Invalid Edition",parent=root)

            elif intqu(q):
                messagebox.showwarning("Warning", "Invalid  Quantity",parent=root)

            elif intpr(pr):
                messagebox.showwarning("Warning", "Invalid  Price",parent=root)

            elif bookexiadd(bn,bi,an,c,e,pu,pr):
                mycursor.execute( "SELECT * FROM books WHERE bookname = %s and bookno =%s and authorname=%s and category =%s and  edition =%s and publisher = %s and price =%s",(bn,int(bi),an,c,e,pu,int(pr)))
                cc=mycursor.fetchone()
                num=int(cc[6])+int(q)
                num2=int(cc[8])+int(q)
                mycursor.execute("UPDATE books SET quantity =%s , instock =%s WHERE bookname = %s and bookno =%s and authorname=%s and category =%s and  edition =%s and publisher = %s and price =%s", (num,num2,bn,int(bi),an,c,e,pu,int(pr)))
                mydb.commit()
                messagebox.showinfo("Info", "Book Already Exist And It's Quantity Has Been Modified",parent=root)
                book_name.delete(0,END)
                book_id.delete(0,END)
                author_name.delete(0,END)
                category.delete(0,END)
                edition.delete(0,END)
                publisher.delete(0,END)
                quantity.delete(0,END)
                price.delete(0,END)
                category.config(fg="gray")
                category.insert(0,"novel/mag/acad")
                global click
                click=False
                
                
            elif bookidexi(bi):
                messagebox.showwarning("Warning", "Book Id No. Already Exist",parent=root)

            elif bookexi(bn,an,e,pu,pr):
                messagebox.showwarning("Warning", "Same Book Cannot Exist With Two Different Id Nos. ",parent=root)

            else:
                mycursor.execute("INSERT INTO books(bookname ,bookno ,authorname , category , edition ,publisher , quantity , price ,instock ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(bn,int(bi),an,c,e,pu,int(q),int(pr),int(q)))

                mydb.commit()
                root2 = Tk()
                root2.withdraw()
                messagebox.showinfo("Info", "Book Saved successfully",parent=root)
                book_name.delete(0,END)
                book_id.delete(0,END)
                author_name.delete(0,END)
                category.delete(0,END)
                edition.delete(0,END)
                publisher.delete(0,END)
                quantity.delete(0,END)
                price.delete(0,END)
                category.config(fg="gray")
                category.insert(0,"novel/mag/acad")
                #global click
                click=False




        
        w.delete("all")
        global click
        click=False
        def callback(event):
            global click
            if click == False:
                category.delete(0, END)         
                category.config(fg = "black")
                click=True

        w.create_text(380,50,fill="aquamarine2", font="Calibri 35  ",text="Enter The BookDetails Below")
        w.create_text(260,100,fill="yellow3", font="Calibri 20  ",text="Book Name")
        w.create_text(260,130,fill="yellow3", font="Calibri 20  ",text="Book Id No.")
        w.create_text(270,160,fill="yellow3", font="Calibri 20  ",text="Author Name")
        w.create_text(245,190,fill="yellow3", font="Calibri 20  ",text="Category")
        w.create_text(235,220,fill="yellow3", font="Calibri 20  ",text="Edition")
        w.create_text(245,250,fill="yellow3", font="Calibri 20  ",text="Publisher")
        w.create_text(240,280,fill="yellow3", font="Calibri 20  ",text="Quantity")
        w.create_text(221,310,fill="yellow3", font="Calibri 20  ",text="Price")

        #w.create_line(197,50,197,400)
        #w.create_line(355,50,355,400)

        book_name=Entry(root,bg = "light cyan")
        book_name.configure(width = 30, relief = FLAT)
        book_name_window = w.create_window(355,93, anchor=NW, window=book_name)

        book_id=Entry(root,bg ="light cyan")
        book_id.configure(width = 30, relief = FLAT)
        book_id_window = w.create_window(355,123, anchor=NW, window=book_id)

        author_name=Entry(root,bg="light cyan")
        author_name.configure(width = 30, relief = FLAT)
        author_name_window = w.create_window(355,153, anchor=NW, window=author_name)


        category=Entry(root,bg="light cyan",fg="gray")
        category.configure(width = 30, relief = FLAT)
        category_window = w.create_window(355,183, anchor=NW, window=category)
        category.bind("<Button-1>", callback)
        category.insert(0, "novel/mag/acad")

        edition=Entry(root,bg="light cyan")
        edition.configure(width = 30, relief = FLAT)
        edition_window = w.create_window(355,213, anchor=NW, window=edition)

        publisher=Entry(root,bg = "light cyan")
        publisher.configure(width = 30, relief = FLAT)
        publisher_window = w.create_window(355,243, anchor=NW, window=publisher)


        quantity=Entry(root,bg="light cyan")
        quantity.configure(width = 30, relief = FLAT)
        quantity_window = w.create_window(355,273, anchor=NW, window=quantity)

        price=Entry(root,bg="light cyan")
        price.configure(width = 30, relief = FLAT)
        price_window = w.create_window(355,303, anchor=NW, window=price)


        button1 = Button( root,text = "Save Books",  anchor = W,command =lambda: save_book(book_name.get(),
                                                                                           book_id.get(),
                                                                                           author_name.get(),
                                                                                           category.get(),
                                                                                           edition.get(),
                                                                                           publisher.get(),
                                                                                           quantity.get(),
                                                                                           price.get(),w))

        
        button1.configure(width = 15,height=1, relief = FLAT,anchor=CENTER,bg="tan2")
        button1_window = w.create_window(355,333, anchor=NW, window=button1)

    def up_exist_show(w,root,u):
        roll=0
        try:
            roll=int(u)
        except ValueError:
            roll=0
        mycursor.execute( "SELECT * FROM accounts WHERE username = %s or rollno= %s",(u,roll))
        c=mycursor.fetchone()
        if c==None:
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "Invalid username or Roll No.",parent=root)
        else:
            w.delete("all")
            mycursor.execute( "SELECT * FROM accounts WHERE username = %s or rollno = %s",(u,roll))
            c=mycursor.fetchone()

            try:
                im=Image.open(c[26])  #This is the correct location and spelling for my image location
                im = im.resize((150, 150), Image.ANTIALIAS) #The (250, 250) is (height, width)
                photo=ImageTk.PhotoImage(im)
                root.one=photo
                w.create_image(700,50+20, image=photo,anchor='nw',state="normal")
     
            except:
                pass
            w.create_text(300,30+10,fill="cyan", font="Calibri 30  ",text="Student Details")
            w.create_text(300,30+60,fill="light blue", font="Calibri 20  ",text="NAME      :"+c[0])
            w.create_text(300,65+60,fill="light blue", font="Calibri 20  ",text="D.O.B     :"+c[1])
            w.create_text(300,100+60,fill="light blue",font="Calibri 20  ",text="ROLL NO.  :"+str(c[2]))
            w.create_text(300,135+60,fill="light blue",font="Calibri 20  ",text="BRANCH    :"+c[3])
            w.create_text(300,170+60,fill="light blue",font="Calibri 20  ",text="SEM/YEAR      :"+c[4])
            w.create_text(300,205+60,fill="light blue",font="Calibri 20  ",text="PHONE NO. :"+str(c[5]))
            w.create_text(300,240+60,fill="light blue",font="Calibri 20  ",text="ADDRESS   :"+c[6])
            w.create_text(300,275+60,fill="light blue",font="Calibri 20  ",text="E-MAIL    :"+c[7])
            w.create_text(300,310+60,fill="light blue",font="Calibri 20  ",text="REGISTERED ON   :"+c[9])
            
            
            

   
    def show(w,root):
        w.delete("all")
        global clickk
        clickk=False
        def callback(event):
            global clickk
            if clickk == False:
                username.delete(0, END)         
                username.config(fg = "black")
                clickk=True
        username=Entry(root,fg="gray")
        username.configure(width = 30, relief = FLAT)
        username_window = w.create_window(320,40, anchor=NW, window=username)

        button1 = Button( root,text = "View Profile",  anchor = W,command=lambda :up_exist_show(w,root,username.get()))
        button1.configure(width = 15,height=1, activebackground = "#33B5E5", relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(530,40, anchor=NW, window=button1)
        username.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
        username.insert(0, "Enter username Or Roll No.")           # Set default text at cursor position 0.





    def dele_last(w,r,u):
        w.delete("all")
        #print(r,u)
        mycursor.execute( "DELETE FROM accounts WHERE username = %s or rollno= %s",(u,r))
        mydb.commit()
        messagebox.showinfo("Info", "Account Deleted successfully",parent=root)



    def up_exist_del(w,r,u):
        roll=0
        try:
            roll=int(u)
        except ValueError:
            roll=0
        mycursor.execute( "SELECT * FROM accounts WHERE username = %s or rollno= %s",(u,roll))
        c=mycursor.fetchone()
        if c==None:
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "Invalid username or Roll No.",parent=root)
        elif c[10]!=None or c[14]!=None or c[18]!=None or c[22]!=None:
            messagebox.showwarning("Warning", "The Student Have Not Returned The Issued Books",parent=root)
        else:
            w.delete("all")
            mycursor.execute( "SELECT * FROM accounts WHERE username = %s or rollno = %s",(u,roll))
            c=mycursor.fetchone()


            
          #adding photo
            try:
                im=Image.open(c[26])  #This is the correct location and spelling for my image location
                im = im.resize((150, 150), Image.ANTIALIAS) #The (250, 250) is (height, width)
                photo=ImageTk.PhotoImage(im)
                root.one=photo
                w.create_image(700,50+20, image=photo,anchor='nw',state="normal")
         
            except:
                pass

            w.create_text(300,30+10,fill="cyan", font="Calibri 30  ",text="Student Details")
            w.create_text(300,30+60,fill="light blue", font="Calibri 20  ",text="NAME      :"+c[0])
            w.create_text(300,65+60,fill="light blue", font="Calibri 20  ",text="D.O.B     :"+c[1])
            w.create_text(300,100+60,fill="light blue",font="Calibri 20  ",text="ROLL NO.  :"+str(c[2]))
            w.create_text(300,135+60,fill="light blue",font="Calibri 20  ",text="BRANCH    :"+c[3])
            w.create_text(300,170+60,fill="light blue",font="Calibri 20  ",text="SEM/YEAR      :"+c[4])
            w.create_text(300,205+60,fill="light blue",font="Calibri 20  ",text="PHONE NO. :"+str(c[5]))
            w.create_text(300,240+60,fill="light blue",font="Calibri 20  ",text="ADDRESS   :"+c[6])
            w.create_text(300,275+60,fill="light blue",font="Calibri 20  ",text="E-MAIL    :"+c[7])
            w.create_text(300,310+60,fill="light blue",font="Calibri 20  ",text="REGISTERED ON   :"+c[9])
            button1 = Button( root,text = "Do You Want to Delete This Account",  anchor = W,command=lambda :dele_last(w,roll,u))
            button1.configure(width = 30, activebackground = "#33B5E5", relief = FLAT,anchor=CENTER,bg="gray")
            button1_window = w.create_window(240,340+70, anchor=NW, window=button1)



        
    def dele_stu(w):
        w.delete("all")
        global clickk
        clickk=False
        def callback(event):
            global clickk
            if clickk == False:
                username.delete(0, END)         
                username.config(fg = "black")
                clickk=True
        username=Entry(root,fg="gray")
        username.configure(width = 30, relief = FLAT)
        username_window = w.create_window(320,40, anchor=NW, window=username)

        button1 = Button( root,text = "View Profile",  anchor = W,command=lambda :up_exist_del(w,root,username.get()))
        button1.configure(width = 15,height=1, relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(530,40, anchor=NW, window=button1)
        username.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
        username.insert(0, "Enter username Or Roll No.")           # Set default text at cursor position 0.

      
    root=Toplevel()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.configure(background='ivory4')

    #labels and buttons
    w = Canvas(root, width=1000, height=500,bg="ivory4",bd=0)
    labelfont = ('Helvetica', 30,"italic", 'bold')
    main_head=Label(root,text=" LIBRARY MANAGEMENT SYSTEM ",bg="ivory4",fg="thistle3",font=labelfont)
    sub_head=Label(root,text=" Welcome Librarian",bg="ivory4",fg="thistle3",font=('Helvetica', 20,"italic"))
    add_stu=Button(root, text="Add Student", fg="black", bg="powder blue", command=lambda :stupass())
    del_stu=Button(root, text="Delete Student", fg="black", bg="powder blue", command=lambda :dele_stu(w))
    stu_pro=Button(root, text="Student Profile", fg="black", bg="powder blue", command=lambda :show(w,root))
    add_book=Button(root, text="Add Book", fg="black", bg="powder blue", command=lambda :addbook(w))
    search_book=Button(root, text="Search Book", fg="black", bg="powder blue", command=lambda :searchbook(w))
    del_book=Button(root, text="Delete Book", fg="black", bg="powder blue", command=lambda :delbook(w))
    issue_book=Button(root, text="Issue Book", fg="black", bg="powder blue", command=lambda :issuebook(w))
    return_book=Button(root, text="Return Book", fg="black", bg="powder blue", command=lambda :returnbook(w))
    student_list=Button(root, text="Students List", fg="black", bg="powder blue", command=lambda :studentlist(w))
    book_list=Button(root, text="Book List", fg="black", bg="powder blue", command=booklist)
    close_win = Button(root, text="close", fg="black", bg="red", command=lambda :logout(root))

    #placing labels and buttons
    w.place(x=350,y=130)    
    main_head.place(x=350, y=40)
    sub_head.place(x=85, y=130)
    add_stu.place(x=100, y=180,width=110)
    stu_pro.place(x=100, y=230,width=110)
    del_stu.place(x=100, y=280,width=110)
    add_book.place(x=100, y=330,width=110)
    search_book.place(x=100, y=380,width=110)
    del_book.place(x=100, y=430,width=110)
    issue_book.place(x=100, y=480,width=110)
    return_book.place(x=100, y=530,width=110)
    student_list.place(x=100, y=580,width=110)
    book_list.place(x=100, y=630,width=110)
    close_win.place(x=1322, y=0,width=45)

    root.mainloop()


def libpass():
    root=Tk()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    #labels
    root.configure(background='tan')
    root.title("login page")
    #root.geometry("500x300")
    heading = Label(root, text="Welcome Librarian", bg="tan",font=('times',20,'italic','bold'),fg="green")
    username = Label(root, text="Username", bg="tan")
    password=Label(root,text="Password",bg="tan")

    #placing labels
    heading.place(x=524,y=300)
    username.place(x=500,y = 360)
    password.place(x=500,y=380)


    #entry options
    username_field=Entry(root)
    password_field=Entry(root,show="*")


    #placing entry options
    username_field.place(x = 562,y=360,width=200)
    password_field.place(x = 562,y=380,width=200)

    #submit and close button
    close_win = Button(root, text="close", fg="black", bg="red", command=root.destroy)
    submit=Button(root,text="submit",fg="black",bg="red",command=lambda :lib_pass_eval(username_field,password_field,root))

    #placing submit and close button
    submit.place(x = 632, y = 400)
    close_win.place(x=1322, y=0,width=45)

    root.mainloop()

def stu_menu(u,p):

    def book_existt(w,root,bookni):
        booknid=-1
        try:
            booknid=int(bookni)
        except ValueError:
            booknid=-1
        mycursor.execute( "SELECT * FROM books WHERE bookno = %s or bookname= %s",(booknid,bookni))
        cc=mycursor.fetchall()
        if len(cc)==0:
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "No Book Exist With Given BookName Or BookId No. ",parent=root)
        else:
            newroot=Tk()
            newroot.configure(background="burlywood3")
            newroot.overrideredirect(True)
            newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))

            close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
            close_win.place(x=1322, y=0, width=45)
            
            labelfont = ('times', 30,"italic", 'bold')
            head_label=Label(newroot,text="Search Results",bg="burlywood3",fg="brown",font=labelfont)
            head_label.grid(row=0, column=0,columnspan=3,sticky=W)
            Label(newroot,text="  S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=0)
            Label(newroot,text="  Book Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=1)
            Label(newroot,text="  Book Id No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=2)
            Label(newroot,text="  Author Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=3)
            Label(newroot,text="  Category  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=4)
            Label(newroot,text="  Edition  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=5)
            Label(newroot,text="  Publisher  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=6)
            Label(newroot,text="  Quantity  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=7)
            Label(newroot,text="  Price  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=8)
            Label(newroot,text="  In Stock  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=9)
            m=0
            labelfont = (10)
            for i in cc:
                m=m+1
                newl1=Label(newroot,text=str(m),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0)
                newl2=Label(newroot,text=i[0],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1)
                newl3=Label(newroot,text=str(i[1]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2)
                newl4=Label(newroot,text=i[2],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3)
                newl5=Label(newroot,text=i[3],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4)
                newl6=Label(newroot,text=i[4],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5)
                newl7=Label(newroot,text=i[5],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6)
                newl8=Label(newroot,text=str(i[6]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7)
                newl9=Label(newroot,text=str(i[7]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=8)
                newl10=Label(newroot,text=str(i[8]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=9)
            
        
    def searchbookk(w):
        w.delete("all")
        global clickk
        clickk=False
        def callback(event):
            global clickk
            if clickk == False:
                bookname1.delete(0, END)         
                bookname1.config(fg = "black")
                clickk=True
        bookname1=Entry(root,fg="gray")
        bookname1.configure(width = 30, relief = FLAT)
        bookname1_window = w.create_window(320,40, anchor=NW, window=bookname1)

        button1 = Button( root,text = "Search Book",  anchor = W,command=lambda :book_existt(w,root,bookname1.get()))
        button1.configure(width = 15,height=1,  relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(530,40, anchor=NW, window=button1)
        bookname1.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
        bookname1.insert(0, "Enter Book Name Or Book Id No.")           # Set default text at cursor position 0.


    
    def booklistt():
        def bookex(event):
            try:
                mycursor.execute("SELECT * FROM books")
                c=mycursor.fetchall()
                workbook2 = xlsxwriter.Workbook('books.xlsx')
                worksheet2 = workbook2.add_worksheet()
                row=0
                col=0
                worksheet2.write(row, col,  "Book Name")
                worksheet2.write(row, col+1,  "Book ID No.")
                worksheet2.write(row, col+2,  "Author Name")
                worksheet2.write(row, col+3,  "Category")
                worksheet2.write(row, col+4,  "Addition")
                worksheet2.write(row, col+5,  "Publisher")
                worksheet2.write(row, col+6,  "Quantity")
                worksheet2.write(row, col+7,  "Price")
                worksheet2.write(row, col+8,  "Instock")
                col=0
                row=1
                for x in c:
                    for i in x:
                        if i==None:
                            i="None"
                        worksheet2.write(row, col,  i)
                        col=col+1
                    row=row+1
                    col=0
                workbook2.close()
                #root2=Toplevel()
                #root2.withdraw()
                messagebox.showinfo("Info", "The Book List Has Been Downloaded In The Form Of EXCEL Sheet In Your Working Directory",parent=newroot)

            except:
                #root2=Toplevel()
                #root2.withdraw()
                messagebox.showwarning("Warning", "The Book List EXCEL Sheet Is Opened Somewhere\nCannot Do Changes\nClose The EXCEL Sheet And Try Again",parent=newroot)

                        









        
        newroot=Tk()
        newroot.configure(background="burlywood3")
        newroot.overrideredirect(True)
        newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))
        mycursor.execute( "SELECT * FROM books ")
        det=mycursor.fetchall()
        
        close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
        close_win.place(x=1322, y=0, width=45)

        labelfont = ('times', 30,"italic", 'bold')
        head_label=Label(newroot,text="Book List",bg="burlywood3",fg="brown",font=labelfont)
        head_label.grid(row=0, column=0,columnspan=3,sticky=W)
        Label(newroot,text="  S. No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=0)
        Label(newroot,text="  Book Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=1)
        Label(newroot,text="  Book Id No.  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=2)
        Label(newroot,text="  Author Name  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=3)
        Label(newroot,text="  Category  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=4)
        Label(newroot,text="  Edition  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=5)
        Label(newroot,text="  Publisher  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=6)
        Label(newroot,text="  Quantity  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=7)
        Label(newroot,text="  Price  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=8)
        Label(newroot,text="  In Stock  ",bg="burlywood3",fg="royalblue",font=10).grid(row=1,column=9)
        m=0
        labelfont = (10)
        for i in det:
            m=m+1
            newl1=Label(newroot,text=str(m),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=0)
            newl2=Label(newroot,text=i[0],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=1)
            newl3=Label(newroot,text=str(i[1]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=2)
            newl4=Label(newroot,text=i[2],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=3)
            newl5=Label(newroot,text=i[3],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=4)
            newl6=Label(newroot,text=i[4],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=5)
            newl7=Label(newroot,text=i[5],bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=6)
            newl8=Label(newroot,text=str(i[6]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=7)
            newl9=Label(newroot,text=str(i[7]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=8)
            newl10=Label(newroot,text=str(i[8]),bg="burlywood3",fg="royalblue",font=labelfont).grid(row=m+1,column=9)

        Label(newroot,text="\n",bg="burlywood3",fg="royalblue",font=10).grid(row=m+2,column=7,sticky=W)            
        labell=Label(newroot,text="Click Here To Download The Book List As EXCEL Sheet ",bg="burlywood3",fg="royalblue",font=10)
        labell.grid(row=m+3,column=0,columnspan=8,sticky=W)
        labell.bind("<Button-1>", bookex)



    def dell(w):
      w.delete("all")

    def booksissued(w):
        w.delete("all")
        mycursor.execute( "SELECT * FROM accounts WHERE username = %s and username = %s",(u,u))
        c=mycursor.fetchone()
        if c[10]==None and c[14]==None and c[18]==None and c[22]==None :
            messagebox.showwarning("Warning", "No Books Are Issued On Your Behalf",parent=root)
        else:
            newroot=Tk()
            newroot.configure(background="burlywood3")
            newroot.overrideredirect(True)
            newroot.geometry("{0}x{1}+0+0".format(newroot.winfo_screenwidth(), newroot.winfo_screenheight()))

            close_win=Button(newroot,text="close",fg="black",bg="red",command=newroot.destroy)
            close_win.place(x=1322, y=0, width=45)
                
            labelfont = ('times', 30,"italic", 'bold')
            head_label=Label(newroot,text="Books Issued",bg="burlywood3",fg="brown",font=labelfont)
            head_label.grid(row=0, column=0,columnspan=3,sticky=W)
            k=0
            count=0
            m=2
            labelfont = (10)
            Label(newroot,text="",bg="burlywood3",fg="brown",font=labelfont).grid(row=1,column=0,rowspan=2)
            while(k<16):
                if c[10+k]!=None:
                    m=m+1
                    Label(newroot,text=str(count+1),bg="burlywood3",fg="brown",font=labelfont).grid(row=m,column=0)
                    Label(newroot,text="Book Name",bg="burlywood3",fg="brown",font=labelfont).grid(row=m,column=1)
                    Label(newroot,text=":"+str(c[10+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m,column=2,sticky=W)
                    Label(newroot,text="Book Id No.",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+1,column=1)
                    Label(newroot,text=":"+str(c[11+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m+1,column=2,sticky=W)
                    Label(newroot,text="Issued Date",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+2,column=1)
                    Label(newroot,text=":"+str(c[12+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m+2,column=2,sticky=W)
                    Label(newroot,text="Return Date",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+3,column=1)
                    Label(newroot,text=":"+str(c[13+k]),bg="burlywood3",fg="brown",font=labelfont).grid(row=m+3,column=2,sticky=W)
                    Label(newroot,text="",bg="burlywood3",fg="brown",font=labelfont).grid(row=m+8,column=0,rowspan=2)
                k=k+4
                m=m+9
                count=count+1

            
            
                 
    def show(w,u,root):
      w.delete("all")
      u=(u,)
      mycursor.execute( "SELECT * FROM accounts WHERE username = %s",(u))
      c=mycursor.fetchone()
    
      #adding photo
      try:
          im=Image.open(c[26])  #This is the correct location and spelling for my image location
          im = im.resize((150, 150), Image.ANTIALIAS) #The (250, 250) is (height, width)
          photo=ImageTk.PhotoImage(im)
          root.one=photo
          w.create_image(700,50+20, image=photo,anchor='nw',state="normal")
     
      except:
          pass


      w.create_text(300,30+10,fill="cyan", font="Calibri 30  ",text="My Profile ")
      w.create_text(300,30+60,fill="light blue", font="Calibri 20  ",text="NAME      :"+c[0])
      w.create_text(300,65+60,fill="light blue", font="Calibri 20  ",text="D.O.B     :"+c[1])
      w.create_text(300,100+60,fill="light blue",font="Calibri 20  ",text="ROLL NO.  :"+str(c[2]))
      w.create_text(300,135+60,fill="light blue",font="Calibri 20  ",text="BRANCH    :"+c[3])
      w.create_text(300,170+60,fill="light blue",font="Calibri 20  ",text="SEM/YEAR      :"+c[4])
      w.create_text(300,205+60,fill="light blue",font="Calibri 20  ",text="PHONE NO. :"+str(c[5]))
      w.create_text(300,240+60,fill="light blue",font="Calibri 20  ",text="ADDRESS   :"+c[6])
      w.create_text(300,275+60,fill="light blue",font="Calibri 20  ",text="E-MAIL    :"+c[7])
      w.create_text(300,310+60,fill="light blue",font="Calibri 20  ",text="REGISTERED ON   :"+c[9])


      
    def delpass(w,u,p):
        w.delete("all")
        w.create_text(300,180,fill="light blue", font="Calibri 20  ",text="username         :")
        w.create_text(300,215,fill="light blue", font="Calibri 20  ",text="old password   :")
        w.create_text(300,250,fill="light blue",font="Calibri 20  ",text="new password :")

        button1 = Button( root,text = "Change password",  anchor = W,command=lambda :up_exist(w,root,username.get(),old_password.get(),new_password.get()))
        button1.configure(width = 15, activebackground = "#33B5E5", relief = FLAT,anchor=CENTER,bg="yellow")
        button1_window = w.create_window(320,285, anchor=NW, window=button1)

        username=Entry(root)
        username.configure(width = 30, relief = FLAT)
        username_window = w.create_window(390,175, anchor=NW, window=username)

        old_password=Entry(root)
        old_password.configure(width = 30, relief = FLAT)
        old_password_window = w.create_window(390,210, anchor=NW, window=old_password)

        new_password=Entry(root)
        new_password.configure(width = 30, relief = FLAT)
        new_password_window = w.create_window(390,245, anchor=NW, window=new_password)

    def up_exist(w,r,u,op,np):
        mycursor.execute( "SELECT * FROM accounts WHERE username = %s and password = %s",(u,op))
        c=mycursor.fetchone()
        if c==None:
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "Invalid username or password",parent=root)
        else:
            mycursor.execute("UPDATE accounts SET password = %s WHERE password = %s", (np,op))
            mydb.commit()
            messagebox.showinfo("Info", "Password successfully Changed",parent=root)
    

    
        
    root=Toplevel()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.configure(background='DarkSeaGreen4')

    mycursor.execute( "SELECT * FROM accounts WHERE username = %s",(u,))
    pp=mycursor.fetchone()

     
    #labels and buttons
    w = Canvas(root, width=1000, height=500,bg="DarkSeaGreen4",bd=0)
    labelfont = ('Helvetica', 30,"italic", 'bold')
    main_head=Label(root,text=" LIBRARY MANAGEMENT SYSTEM ",bg="DarkSeaGreen4",fg="wheat3",font=labelfont)
    sub_head=Label(root,text=" Welcome "+pp[0],bg="DarkSeaGreen4",fg="wheat3",font=('Helvetica', 20,"italic"))
    my_pro=Button(root, text="My Profile", fg="black", bg="gray57", command=lambda :show(w,u,root))
    search_book=Button(root, text="Search Book", fg="black", bg="gray57", command=lambda :searchbookk(w))
    books_issued=Button(root, text="Books Issued", fg="black", bg="gray57", command=lambda :booksissued(w))
    book_list=Button(root, text="Book List", fg="black", bg="gray57", command=booklistt)
    change_pass=Button(root, text="Change Password", fg="black", bg="gray57", command=lambda :delpass(w,u,p))
    close_win = Button(root, text="close", fg="black", bg="red", command=lambda :logout(root))



    


    #placing labels and buttons
    w.place(x=350,y=130)
    main_head.place(x=350, y=40)
    sub_head.place(x=85, y=130)
    my_pro.place(x=100, y=180,width=110)
    search_book.place(x=100, y=230,width=110)
    books_issued.place(x=100,y=280,width=110)
    book_list.place(x=100, y=330,width=110)
    change_pass.place(x=100, y=380,width=110)
    close_win.place(x=1322, y=0,width=45)

    root.mainloop()


  


def stulog():
    root=Tk()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    #labels
    root.configure(background='yellow')
    root.title("login page")
    #root.geometry("500x300")
    close_win = Button(root, text="close", fg="black", bg="red", command=root.destroy)
    heading = Label(root, text="Welcome Student", bg="yellow",font=('times',20,'italic','bold'),fg="green")
    username = Label(root, text="Username", bg="yellow")
    password=Label(root,text="Password",bg="yellow")

    #placing labels
    heading.place(x=524,y=300)
    username.place(x=500,y = 360)
    password.place(x=500,y=380)


    #entry options
    username_field=Entry(root)
    password_field=Entry(root,show="*")


    #placing entry options
    username_field.place(x = 562,y=360,width=200)
    password_field.place(x = 562,y=380,width=200)
    close_win.place(x=1322, y=0,width=45)
    #submit button
    submit=Button(root,text="submit",fg="black",bg="red",command=lambda :stu_pass_eval(username_field,password_field,root))
    submit.place(x = 632, y = 400)


    root.mainloop()
    
def stuhome():
    root=Tk()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.configure(background='dark cyan')

    close_win = Button(root, text="close", fg="black", bg="red", command=root.destroy)
    heading = Label(root, text="Welcome Student", bg="dark cyan", font=('times', 20, 'italic', 'bold'), fg="green")
    new_acc = Label(root, text="Create New Account", bg="dark cyan", font=('times', 15, ), fg="indigo")
    exit_acc= Label(root, text="Already Have Account", bg="dark cyan",font=('times',15,),fg="indigo")

    heading.place(x=500, y=300)
    new_acc.place(x=500, y=360)
    exit_acc.place(x=500, y=415)
    close_win.place(x=1322, y=0,width=45)

    signup=Button(root,text="signup",fg="Black",bg="dark grey",command=lambda:stupass())
    signin=Button(root,text="signin",fg="Black",bg="dark grey",command=lambda:stulog())

    signup.place(x = 500,y=385,width=200)
    signin.place(x = 500,y=440,width=200)
    root.mainloop()

def stupass():
    global tempdir
    tempdir=""
    def choosefile():
        global tempdir
        tempdir =   filedialog.askopenfilename(parent=root, initialdir= "/",title="choose your photo",filetype=(("jpg","*.jpg"),("png","*.png"),("All Files","*.*")))
    def check_dob(d):
        try:
            datetime.datetime.strptime(d, "%d-%m-%Y")
            return False
        except:
            return True

    def check_em(u):
        isvalid=validate_email(u)
        if isvalid==True:
            return False
        else:
            return True
        
    def stureg(n,d,r,b,s,p,a,u,pa,rpa,root,filepath):
        if(n=="" or d=="" or r=="" or b=="" or s=="" or p=="" or a=="" or u=="" or pa=="" or rpa==""):
            root1 = Tk()
            root1.withdraw()
            messagebox.showwarning("Warning", "All Fields Are Mandatory",parent=root)

        elif filepath=="" :
            root1 = Tk()
            root1.withdraw()
            messagebox.showwarning("Warning", "Please Select A Photo",parent=root)
        elif check_dob(d):
            root2 = Tk()
            root2.withdraw()
            messagebox.showwarning("Warning", "Invalid D.O.B Format",parent=root)

        elif check_em(u):
            root3 = Tk()
            root3.withdraw()
            messagebox.showwarning("Warning", "Invalid E-Mail",parent=root)

        elif pa != rpa:
            root4 = Tk()
            root4.withdraw()
            messagebox.showwarning("Warning", "Password Does Not Match",parent=root)

           
        elif  (pass_valid(pa)):
            root5 = Tk()
            root5.withdraw()
            messagebox.showwarning("Warning", "The password must contain\nMinimum 8 characters\nAt least one alphabet should be of Upper Case [a-z]\nAt least one alphabet should be of Upper Case [A-Z]\nAt least 1 number or digit between [0-9]\nAt least 1 character from [!,@,#,$,%,^,&,*,_ ]",parent=root)

        elif stu_exist(u,p,r):
            root6 = Tk()
            root6.withdraw()
            messagebox.showwarning("Warning", "Username already exist!!",parent=root)

        else:
            try:
                r=int(r)
                p=int(p)
                now = str(datetime.datetime.now().date())
                mycursor.execute("create table if not exists accounts(name varchar(500),dob varchar(500),rollno BIGINT, branch varchar(500), sem varchar(500), phoneno BIGINT, address varchar(500), username varchar(500), password varchar(500), date varchar(500),ibn1 varchar(500),ibi1 BIGINT,ibid1 varchar(500),ibrd1 varchar(500),ibn2 varchar(500),ibi2 BIGINT,ibid2 varchar(500),ibrd2 varchar(500),ibn3 varchar(500),ibi3 BIGINT,ibid3 varchar(500),ibrd3 varchar(500),ibn4 varchar(500),ibi4 BIGINT,ibid4 varchar(500),ibrd4 varchar(500),photopath varchar(500))")
                mycursor.execute("INSERT INTO accounts (name,dob, rollno, branch, sem, phoneno, address, username, password, date, photopath) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)",(n,d,r,b,s,p,a,u,pa,now,filepath))
                mydb.commit()
                root2 = Tk()
                root2.withdraw()
                messagebox.showinfo("Info", "Account Registered successfully",parent=root)
                name_field.delete(0,END)
                dob_field.delete(0,END) 
                dob_field.config(fg = "gray")
                dob_field.insert(0, "dd-mm-yyyy")
                global click
                click=False
                roll_field.delete(0,END) 
                contact_no_field.delete(0,END)
                address_field.delete(0,END)
                email_id_field.delete(0,END)
                pass_field.delete(0,END)
                repass_field.delete(0,END)
                global tempdir
                tempdir=""
            except:
                root6 = Tk()
                root6.withdraw()
                messagebox.showwarning("Warning", "Invalid Roll No. or Contact No",parent=root)


        
    global click
    click=False
    def callback(event):
        global click
        if click == False:
            dob_field.delete(0, END)         
            dob_field.config(fg = "black")
            click=True
    root = Tk()
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    #labels
    root.configure(background='light blue') 
    root.title("registration form")
    heading = Label(root, text="Registration Form", bg="light blue",font=('times',20,'italic','bold'),fg="green") 
    name = Label(root, text="Name", bg="light blue")
    dob=Label(root,text="D.O.B",bg="light blue")
    roll_no = Label(root, text="Rollno No.", bg="light blue") 
    branch = Label(root, text="Branch", bg="light blue") 
    sem = Label(root, text="Sem/Year", bg="light blue") 
    contact_no = Label(root, text="Contact No.", bg="light blue")  
    address = Label(root, text="Address", bg="light blue")
    email_id = Label(root, text="Email id", bg="light blue")
    passw = Label(root, text="Password", bg="light blue")
    re_pass = Label(root, text="Re-Password", bg="light blue")
    warn=Label(root, text="**All Fields Are Mandatory",fg="red", bg="light blue")

    
    
    #placing labels
    heading.place(x=560, y=275-50)
    name.place(x=525, y=325-50)
    dob.place(x=525, y=350-50)
    roll_no.place(x=525, y=375-50)
    branch.place(x=525, y=400-50)
    sem.place(x=525, y=425-50)
    contact_no.place(x=525, y=450-50)
    address.place(x=525, y=475-50)
    email_id.place(x=525, y=500-50)
    passw.place(x=525, y=525-50)
    re_pass.place(x=525, y=550-50)
    warn.place(x=645, y=700)
    
    #entry options
    name_field = Entry(root)
    dob_field=Entry(root,fg = "gray")
    dob_field.bind("<Button-1>", callback)   # Bind a mouse-click to the callback function.
    dob_field.insert(0, "dd-mm-yyyy")           # Set default text at cursor position 0.

    
    roll_field = Entry(root) 
    
    brnch_var= StringVar(root)
    brnch_var.set('CSE') # set the default option
    BranchMenu = OptionMenu(root,brnch_var,'CSE','ECE','IT','EEE','MECH','CIVIL','AUTO')
    BranchMenu.config(bg="white",anchor='w')

    sem_var= StringVar(root)
    sem_var.set('1/1') # set the default option
    SemMenu = OptionMenu(root, sem_var,'1/1','2/1','3/2','4/2','5/3','6/3','7/4','8/4')
    SemMenu.config(bg="white",anchor='w')

    
    contact_no_field = Entry(root)
    address_field = Entry(root)
    email_id_field = Entry(root) 
    pass_field = Entry(root,show="*")
    repass_field = Entry(root,show="*")
    choosefile=Button(root,text="chose your photo",fg="black",bg="bisque2",command=choosefile)
    close_win = Button(root, text="close", fg="black", bg="red", command=root.destroy)
 

    #placing entry options
    name_field.place(x=600, y=325-50, relwidth=0.15,relheight=0.03)
    dob_field.place(x=600, y=350-50, relwidth=0.15,relheight=0.03)
    roll_field.place(x=600, y=375-50, relwidth=0.15,relheight=0.03)
    BranchMenu.place(x=600, y=400-50, relwidth=0.15,relheight=0.03) 
    SemMenu.place(x=600, y=425-50, relwidth=0.15,relheight=0.03)
    contact_no_field.place(x=600, y=450-50, relwidth=0.15,relheight=0.03)  
    address_field.place(x=600, y=475-50, relwidth=0.15,relheight=0.03)
    email_id_field.place(x=600, y=500-50, relwidth=0.15,relheight=0.03)
    pass_field.place(x=600, y=525-50, relwidth=0.15,relheight=0.03)
    repass_field.place(x=600, y=550-50, relwidth=0.15,relheight=0.03)
    choosefile.place(x=600, y=575-50+3, relwidth=0.15,relheight=0.03)
    close_win.place(x=1322, y=0,width=45)
     
    submit = Button(root, text="Submit", fg="Black",bg="Red",command=lambda:stureg(name_field.get(),
                                                                                   dob_field.get(),
                                                                                   roll_field.get(),
                                                                                   brnch_var.get(),
                                                                                   sem_var.get(),
                                                                                   contact_no_field.get(),
                                                                                   address_field.get(),
                                                                                   email_id_field.get(),
                                                                                   pass_field.get(),
                                                                                   repass_field.get(),
                                                                                   root,tempdir))


    submit.place(x=685, y=600) 
    root.mainloop() 








def main():
    root=Tk()
    root.configure(background="light green")
    #root.geometry('1500x600')#size of window
    
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.title("LBMS")

##    bg_pic_add= PhotoImage(file = "tracklib.png")
##    background_photo = Label(root, image=bg_pic_add)
##    

    
    labelfont = ('times', 30,"italic", 'bold')
    head_label=Label(root,text=" LIBRARY MANAGEMENT SYSTEM ",bg="light green",fg="steelblue",font=labelfont)
    #head_label.config(height=3, width=20)  
    select_label=Label(root,text="Please Choose Any Option To login",bg="light green",font=('times',20,'italic'),fg="violet")
    #Label(root,text="",bg="light green").grid(row=2,column=0)
    stu_button=Button(root,text="1.Student",command=stuhome,bg="light blue")
    #Label(root,text="",bg="light green").grid(row=4,column=0)
    lib_button=Button(root,text="2.Librarian",command=libpass,bg="light blue")
    close_app=Button(root,text="3.Close Aplication",bg="light blue",command=lambda :close_main(root))
    icon=PhotoImage(file="lms.png")#to store address of image
    photo_label=Label(root,image=icon)
    close_win=Button(root,text="close",fg="black",bg="red",command=lambda :close_main(root))#close main_application

##    background_photo.place(x=0, y=0, relwidth=1, relheight=1)
    head_label.place(x=320, y=25)
    select_label.place(x=100, y=100)
    stu_button.place(x=250, y=200, relwidth=0.10)
    lib_button.place(x=250, y=250, relwidth=0.10)
    close_app.place(x=250, y=300, relwidth=0.10)
    photo_label.place(x=700, y=150)
    close_win.place(x=1322, y=0, width=45)


 
    root.mainloop()

















if __name__=="__main__":
    main()

                  
