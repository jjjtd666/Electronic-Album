# -*- coding: utf-8 -*-
"""
聲明：本專案程式碼由本小組從0開始寫起，絕無抄襲，系統架構完全由本組構思設計

涵式庫需求: mysqlclient、pillow、pyqrcode

Created on Fri Jun  1 20:49:34 2018

"""

import sys
import os
import random
from datetime import datetime
import functools # 檢測Mouse_Click涵式庫
import shutil # 複製影像涵式庫
import MySQLdb # 資料庫
import ftplib # FTP
import pyqrcode #QRCODE

from PIL import Image,ImageFilter,ImageDraw,ImageFont #convert to jpg , image effect

# pyqt5
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton, QLabel, QCheckBox, QLineEdit, QFileDialog, QComboBox, QAction, QMenuBar
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor

# 信箱
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#連接 MYSQL 資料庫
db = MySQLdb.connect(host="106.105.25.121",user="admin", passwd="admin", db="album", charset="utf8")
cursor = db.cursor()
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;') # 設定資料庫的環境為UTF-8
db.commit(); # 確認SQL指令
print("MYSQL資料庫連接成功．．．")

date = str(datetime.now()) # 取得現在時間

class Member(): # 使用者類別
    
    def __init__(self):
        
        self.nickname = ""
        self.account = ""
        self.album = []
        
        for i in range(0,8): # 使用者相簿狀態  0為未啟用 1為未啟用 預設0
            self.album.append(0)
    
        self.picture = [[0 for x in range(16)] for y in range(9)]   # 使用者相片狀態 for 二維陣列 0為未啟用 1為啟用 預設0

    def LoadData(self): # 讀取資料庫的使用者相簿資訊
        
        for i in range(0,8):
            select = "SELECT * FROM pictures WHERE account='" + self.account + "' AND albumid = '" + str(i) + "'"
            cursor.execute(select)
            result = cursor.fetchall() #以list的方式回傳欲查詢的資料
            if cursor.rowcount != 0: #當回傳的列數不等於0的時候
                self.album[i] = 1
                rt.labelstate[i] = True
                for r in result:
                    rt.textstr[i] = r[18]
                    for j in range(3,18): # 由資料庫中的pictures第三行之後開始讀取
                        if r[j] == 1:
                            self.picture[i][j-3] = 1
                                        
    def SaveData(self): # 保存至資料庫
        for i in range(0,8):
            if self.album[i] == 1:
                for j in range(0,15):
                    string = "UPDATE pictures SET pic"+str(j)+"='"+str(self.picture[i][j])+"' WHERE account='" + self.account + "' AND albumid = '" + str(i) + "'"
                    cursor.execute(string)
                    db.commit()
                t = rt.textstr[i]
                string = "UPDATE pictures SET aname='"+str(t)+"' WHERE account='" + self.account + "' AND albumid = '" + str(i) + "'"
                cursor.execute(string)
                db.commit()
                
    def SaveDataForPicutre(self,albumid,picid):
        string = "UPDATE pictures SET pic"+str(picid)+"='"+str(self.picture[albumid][picid])+"' WHERE account='" + self.account + "' AND albumid = '" + str(albumid) + "'"
        cursor.execute(string)
        db.commit()
        
    def SaveDataForAName(self,albumid):
        t = rt.textstr[albumid]
        string = "UPDATE pictures SET aname='"+str(t)+"' WHERE account='" + self.account + "' AND albumid = '" + str(albumid) + "'"
        cursor.execute(string)
        db.commit()
        
    def WriteLog(self,text): # 儲存log至src/log/log.txt
        f = open('src/log/log.txt', 'a', encoding = 'UTF-8')
        print(text)
        f.writelines(text+"\n")
        f.close()
        
           

class Login(QWidget): # 登入視窗
    
    def __init__(self):
        
        super().__init__() # 繼承QWidget所有父類別的方法與函數
        self.initUI() # 視窗的初始化設定涵數
        
    def initUI(self):  
        
        self.setGeometry(700, 400, 400, 400)   
        self.setWindowTitle('電子相簿管理系統 Version 1.0')
        self.setFixedSize(400, 400) # 固定視窗
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        
        self.setAutoFillBackground(True) # 自動將顏色填滿
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(230, 203, 27)) # 設定背景顏色為 RGB
        self.setPalette(p)
        
        self.label = QLabel(self)
        pixmap = QPixmap('src/images/login.jpg')
        pixmap_s = pixmap.scaled(135, 90)
        self.label.setPixmap(pixmap_s)
        self.label.resize(135,90)
        self.label.move(125,30)
                
        self.textlabel = QLabel(self)
        self.textlabel.setText('輸入您的帳號')
        self.textlabel.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        self.textlabel.resize(200,16)
        self.textlabel.move(160,135)
        
        self.textlabel1 = QLabel(self)
        self.textlabel1.setText('輸入您的密碼')
        self.textlabel1.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        self.textlabel1.resize(200,16)
        self.textlabel1.move(160,210)
        
        self.textbox = QLineEdit(self) # 如同QLineEdit 等同 textbox
        self.textbox.move(120, 155)
        self.textbox.resize(150,20)
        
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(120, 230)
        self.textbox1.resize(150,20)
        
        self.btn1 = QPushButton('登入', self)
        self.btn1.move(120,310) 
        self.btn1.clicked.connect(lambda:self.OnClickButton(0))
        self.btn1.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.btn2 = QPushButton('註冊', self)
        self.btn2.move(200,310) 
        self.btn2.clicked.connect(lambda:self.OnClickButton(1))
        self.btn2.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.show()
        
    def OnClickButton(self,e):
        
        if e == 0:
            if self.textbox.text() == "" or self.textbox1.text() == "": 
                QMessageBox.question(self, '提示',"您的帳密尚有空格未填寫", QMessageBox.Ok)
                return
                
            select = "SELECT * FROM accounts WHERE account='" + self.textbox.text() + "'";
            cursor.execute(select)
            result = cursor.fetchall()
            if cursor.rowcount == 0:
                QMessageBox.question(self, '提示',"您的帳號或密碼不正確", QMessageBox.Ok)
            else:
                for row in result:
                  #detect password
                  if row[3] == self.textbox1.text():
                      log.hide()
                      rt.show()
                      QMessageBox.question(self, '提示',"登入成功", QMessageBox.Ok)
                      mb.nickname = str(row[1]) # 將資料庫的暱稱載入到腳本中
                      mb.account = str(row[2])# 將資料庫的帳號載入到腳本中
                      mb.LoadData()# 將資料庫中使用者的相片狀況載入到腳本中
                      rt.UpdateLabel() # 更新相簿為登入使用者的label
                      mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 成功登入 日期:{:}".format(mb.nickname,mb.account,date))
                  else:
                      QMessageBox.question(self, '提示',"您的帳號或密碼不正確", QMessageBox.Ok)
        else:
            log.hide()
            reg.show()
            
            

class Register(QWidget): # 註冊視窗
    
    def __init__(self):
        
        super().__init__()
        self.initUI()
        
    def initUI(self):  
        
        self.setGeometry(700, 400, 400, 400)   
        self.setWindowTitle('電子相簿管理系統 Version 1.0')
        self.setFixedSize(400, 400)
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(230, 203, 27))
        self.setPalette(p)
        
        self.label = QLabel(self)
        pixmap = QPixmap('src/images/register.jpg')
        pixmap_s = pixmap.scaled(370, 100)
        self.label.setPixmap(pixmap_s)
        self.label.resize(370,100)
        self.label.move(20,30)
        
        self.textlabel = QLabel(self)
        self.textlabel.setText('請輸入您想註冊的暱稱')
        self.textlabel.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        self.textlabel.move(130,140)
        
        self.textlabel2 = QLabel(self)
        self.textlabel2.setText('請輸入您想註冊的帳號')
        self.textlabel2.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        self.textlabel2.move(130,190)
        
        self.textlabel3 = QLabel(self)
        self.textlabel3.setText('請輸入您想註冊的密碼')
        self.textlabel3.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        self.textlabel3.move(130,240)
        
        self.textbox = QLineEdit(self)
        self.textbox.move(120, 160)
        self.textbox.resize(150,20)
        
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(120, 210)
        self.textbox1.resize(150,20)
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(120, 260)
        self.textbox2.resize(150,20)
        
        self.btn1 = QPushButton('註冊', self)
        self.btn1.move(120,310) 
        self.btn1.clicked.connect(lambda:self.OnClickButton(0))
        self.btn1.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.btn2 = QPushButton('取消註冊', self)
        self.btn2.move(200,310) 
        self.btn2.clicked.connect(lambda:self.OnClickButton(1))
        self.btn2.setFont(QFont("微軟正黑體",10,QFont.Bold))  

        self.show()
        
    def OnClickButton(self,e):
        
        if e == 0: # 當按下註冊按鈕時
            if self.textbox.text() == "" or self.textbox1.text() == "" or self.textbox2.text() == "": 
                QMessageBox.question(self, '提示',"您的資料尚有空格未填寫", QMessageBox.Ok)
                return
                
            select = "SELECT * FROM accounts WHERE account='" + self.textbox1.text() + "'"; # 檢測是否有相同的帳號,回傳列數,當有列數時則代表有人申請過
            cursor.execute(select)
            if cursor.rowcount == 0:
                str1 = "INSERT INTO accounts (username,account,password) VALUES('" + self.textbox.text() + "','" + self.textbox1.text() + "','" + self.textbox2.text() + "')"
                cursor.execute(str1)
                db.commit()
                QMessageBox.question(self, '提示',"註冊成功！", QMessageBox.Ok)
                path = "src/users/" + self.textbox1.text()
                os.makedirs(path)
                reg.hide()
                log.show()
                self.AutoCreateAlbum()
                mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 完成第一次的帳號註冊 日期:{:}".format(self.textbox.text(),self.textbox1.text(),date))
            else:
                QMessageBox.question(self, '提示',"您的帳號已經有人使用，請重新輸入", QMessageBox.Ok)
        else: # 當取消註冊按鈕時
            reg.hide()
            log.show()
    
    def AutoCreateAlbum(self): # 當使用者第一次註冊時,系統自動幫使用者創造一個新的空白相簿
        path = "src/users/" + self.textbox1.text() + "/album_0"
        os.makedirs(path) # 產生一個相簿資料夾給使用者
        ppath = "src/users/"+self.textbox1.text()+"/album_0/0.jpg"
        shutil.copy('src/images/ex2.jpg',ppath) # 將範例圖片複製到使用者的資料夾裡
        string = "INSERT INTO pictures (account,albumid,pic0,aname) VALUES('" + self.textbox1.text() + "',0,1,'我的相簿1')"
        cursor.execute(string)
        db.commit()
        mb.SaveData() # 將使用者的資料傳送到資料庫本存
            
            

class Root_Album(QWidget): #相簿視窗
            
    def __init__(self):
        
        super().__init__()
        
        # 初始設定值
        self.labelstate = [] # 腳本內的相簿狀態,這裡銜接Member的self.album,也就是說 資料庫讀取使用者的相簿狀態 傳送到Member的album再傳送到此類別的self.labelstate
        self.select = [] # 檢測玩家是否在相片的checkbox上面打勾
        self.delcheck = False # 檢測玩家是否有使用到checkbox,如果有系統回傳True,否則點選刪除相簿不會有反應
        self.editid = -1 # 檢測最後一個被打勾的相簿,目的是為了修改相簿名稱
        for i in range(0,8): # 預設產生八個相簿的狀態為False,以及選擇的狀態為False
            self.labelstate.append(False)
            self.select.append(False)

        self.initUI()
        
    def initUI(self):               
        
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        self.setGeometry(400, 100, 1024, 768)        
        self.setWindowTitle('電子相簿管理系統 Version 1.0')
        self.setFixedSize(1024, 768)
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(230, 203, 27))
        self.setPalette(p)
        
        menubar = QMenuBar(self)
        fileMenu = menubar.addMenu('選項')
        
        data = QAction("查看個人資料",self)
        fileMenu.addAction(data)
        fileMenu.triggered[QAction].connect(self.OnClickMenu)

        self.LoadButton()
        self.LoadLabel()
        self.LoadCheckBox()
                
        self.show()
        
    def OnClickMenu(self): # 當按下"查看個人資料"的表單時
        
        sums = [0,0]
        for i in range(0,8):
            if mb.album[i] == 1: # 當使用者的相簿狀態為1時增加總數
                sums[0] +=1 
                for j in range(0,15):
                    if mb.picture[i][j] == 1: # 當使用者的相片狀態為1時增加總數
                        sums[1] += 1

        string = "個人暱稱:%s\t\n\n帳號:%s\t\n\n相簿數量:%d\t\n\n相片數量:%d" % (mb.nickname,mb.account,sums[0],sums[1])
        QMessageBox.question(self, '個人資料',string, QMessageBox.Ok)
                                
    def LoadButton(self): # 程式第一次啟動時,系統會寫入button進行初始化
        
        self.btn1 = QPushButton('新增相簿', self)
        self.btn1.setToolTip('點選此選項新增相簿,您最多可以新增8個相簿')
        self.btn1.resize(80,80)
        self.btn1.move(925,40) 
        self.btn1.clicked.connect(lambda:self.OnClickButton(0))
        self.btn1.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.btn2 = QPushButton('刪除相簿', self)
        self.btn2.setToolTip('點選此選項刪除您不想要留住的相簿')
        self.btn2.resize(80,80)
        self.btn2.move(925,140) 
        self.btn2.clicked.connect(lambda:self.OnClickButton(1))
        self.btn2.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.btn3 = QPushButton('修改名稱', self)
        self.btn3.setToolTip('點選此選項修改您欲想修改的相簿名稱')
        self.btn3.resize(80,80)
        self.btn3.move(925,240) 
        self.btn3.clicked.connect(lambda:self.OnClickButton(2))
        self.btn3.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
    def LoadLabel(self): # 程式第一次啟動時,系統會寫入label進行初始化
        
        # 歡迎回來的label
        self.labeltitle = QLabel(self)
        self.labeltitle.resize(300,30)
        self.labeltitle.move(390,730)
        self.labeltitle.setFont(QFont("微軟正黑體",20,QFont.Bold))
        self.labeltitle.setStyleSheet('color: blue')
        
        #圖片label初始化
        self.label = []
        for i in range(0,8):
            self.label.append(i)           
            self.label[i] = QLabel(self)

            if self.labelstate[i] == True:
                pixmap = QPixmap('src/images/ex2.jpg')
            else:
                 pixmap = QPixmap('src/images/ex1.jpg')
            
            pixmap_s = pixmap.scaled(200, 320)
            self.label[i].setPixmap(pixmap_s)
            self.label[i].resize(200,320)
            self.label[i].mousePressEvent = functools.partial(self.OnClickLabel,source_object=self.label[i],ev=0,id=i)
            if i < 4:
                self.label[i].move(20+225*i,20)
            else:
                j = i-4
                self.label[i].move(20+225*j,380)  
                
        #圖片名稱label初始化
        self.textlabel = []
        self.textstr = []
        for i in range(0,8):
            self.textlabel.append(i)
            self.textstr.append("我的相簿" + str(i+1))
            self.textlabel[i] = QLabel(self)
            self.textlabel[i].resize(105,16)
            self.textlabel[i].setText(self.textstr[i])
            if i < 4: #每四個相簿換位置
                self.textlabel[i].move(110+225*i,350)
            else:
                j = i-4
                self.textlabel[i].move(110+225*j,710)  
            if self.labelstate[i] == False: # 當相簿被啟動時才會顯示圖片
                self.textlabel[i].setVisible(False)
                    
    def LoadCheckBox(self): # 程式第一次啟動時,系統會寫入checkbox進行初始化
        
        self.checkbox = []
        for i in range(0,8):
            self.checkbox.append(i)
            self.checkbox[i] = QCheckBox("",self)
            self.checkbox[i].setChecked(False) # 預先設定每個checkbox為無打勾狀態
            self.checkbox[i].toggled.connect(self.OnCheckboxToggled) # 綁定函數來檢測checkbox是否被打勾
            if i < 4:
                self.checkbox[i].move(90+225*i,350)
            else:
                j = i-4
                self.checkbox[i].move(90+225*j,710)  
                
            if self.labelstate[i] == False: # 當相簿狀態為False時就不會顯示checkbox
                self.checkbox[i].setVisible(False)
                
    def UpdateLabel(self): # 更新label,用來即時更新使用者的照片設定,也就是當程式啟動時會先讓程式進行Loadlabel然後才依據使用者登入進行UpdateLabel
        
        self.labeltitle.setText("歡迎回來,"+mb.nickname) # 更新"歡迎回來"的使用者暱稱
        
        for i in range(0,8):            
            if self.labelstate[i] == True: # 當相簿被啟動時,顯示使用者圖片,若沒有則保守顯示範例圖片(不過已經先被隱藏處理)
                j = 0
                while j < 15: # 用來更新相簿的最首張照片,當相片發生異動時,系統會將相簿內的最首張照片當作相簿封面
                    if mb.picture[i][j] == 1:
                        break
                    j+=1
                ppath ='src/users/'+mb.account+'/album_'+str(i)+'/'+str(j)+'.jpg'
                pixmap = QPixmap(ppath)
            else: # 若相簿狀態為False則發送範例圖片當封面,不過已經被隱藏處理
                pixmap = QPixmap('src/images/ex1.jpg')
                
            pixmap_s = pixmap.scaled(200, 320)
            self.label[i].setPixmap(pixmap_s)
            self.textlabel[i].setText(self.textstr[i])
            if i < 4:
                self.label[i].move(20+225*i,20)
            else:
                j = i-4
                self.label[i].move(20+225*j,380)  
            
        for i in range(0,8): # 當相簿狀態為True的時候才會顯示相簿名稱label跟checkbox項目
            if self.labelstate[i] == True:
                self.textlabel[i].setVisible(True)
                self.checkbox[i].setVisible(True)
            else:
                self.textlabel[i].setVisible(False)
                self.checkbox[i].setVisible(False)
        
    def OnClickButton(self, event): # 當按下按鈕時
        
        if event == 0: # 當按下"新增相簿"按鈕時
            i = 0
            while i < 8: # 透過相簿類別的狀態由while逐格檢視相簿狀態,如果False就新增相簿,最多八個
                if self.labelstate[i] == False:
                    mb.album[i] = 1 # 設置使用者(Member)類別的相簿狀態為1
                    mb.picture[i][0] = 1 # 設置使用者(Member)類別的相片狀態為1
                    self.labelstate[i] = True # 設置本相簿(Roor_Album)類別的相簿狀態為1
                    self.textstr[i] = "我的相簿" + str(i+1)
                    path = "src/users/" + mb.account + "/album_" + str(i) # 路徑為users裡的album相簿編號
                    if os.path.isdir(path): # 防錯機制,如果路徑相簿有資料夾先處刪除處理
                        shutil.rmtree(path)                   
                    os.makedirs(path) # 新增資料夾 相簿命名法為 album_(i)
                    ppath = "src/users/"+mb.account+"/album_"+ str(i) +"/0.jpg"
                    shutil.copy('src/images/ex2.jpg',ppath) # 將範例圖片複製到該新增的相簿資料夾,使其美觀
                    self.UpdateLabel() #即時更新相簿Label
                    QMessageBox.question(self, '提示',"您新增了一個相簿", QMessageBox.Ok)
                    # ↓ SQL語法,新增一筆使用者相簿欄位,順便將預設的圖片狀態寫為1代表啟用中
                    string = "INSERT INTO pictures (account,albumid,pic0,aname) VALUES('" + mb.account + "','" + str(i) + "',1,'"+self.textstr[i]+"')"
                    cursor.execute(string)
                    db.commit()
                    mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 新增了一個相簿編號:{:} 日期:{:}".format(mb.nickname,mb.account,i,date))
                    break
                i+=1
        elif event == 1: # 當按下"刪除相簿"按鈕時
            if self.delcheck == True:
                reply = QMessageBox.question(self, '警告',"您確定要刪除勾選的相簿嗎?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    for i in range(0,8):
                        if self.select[i] == True:
                            mb.album[i] = 0
                            
                            for j in range(0,15):
                                mb.picture[i][j] = 0
                                pic.labelstate[j] = False
                            
                            self.labelstate[i] = False
                            self.UpdateLabel()
                            self.delcheck = False
                            self.checkbox[i].setChecked(False)
                            path = "src/users/" + mb.account + "/album_" + str(i)
                            shutil.rmtree(path)
                            # ↓ SQL語法,刪除資料庫中的相簿欄位為使用者指定的相簿,並由使用者的帳號與相簿ID作為檢測條件
                            string = "DELETE FROM pictures WHERE account='" + mb.account + "' AND albumid = '" + str(i) + "'"
                            cursor.execute(string)
                            db.commit()
                            mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 刪除了一個相簿編號:{:} 日期:{:}".format(mb.nickname,mb.account,i,date))
                        
        elif event == 2: # 當按下"修改相簿"按鈕時
            
            # 利用count檢測使用者是否勾選唯一的相簿,如果選太多或沒選擇無法修改相簿名稱
            count = 0
            for i in range(0,8):
                if(self.select[i] == True):
                    count+=1
            if count != 1:
                QMessageBox.question(self, '提示',"請唯一勾選您欲修改名稱的相簿", QMessageBox.Ok)
            else:
                ean.show() # 啟動修改相簿名稱的視窗
                
    def OnClickLabel(self, event, source_object=None, ev=-1, id=-1): # 當按下label也就是按下圖片時,進入"瀏覽相簿內相片"的視窗
        
        if self.labelstate[id] == True:
            pic.albumid = id # 將點選相簿的編號指向到root_picture類別裡面,使它可以知道使用者點選哪一本相簿
            for j in range(0,15): # 檢測若使用者(Member)類別的狀態為1時,將root_picture的相片狀態設定為True
                if mb.picture[id][j] == 1:
                    pic.labelstate[j] = True
            rt.hide()
            pic.show()
            pic.UpdateLabel()
                
    def OnCheckboxToggled(self): # 當checkbox被打勾時會傳到此涵數
        
        self.delcheck = True
        for i in range(0,8):
            if self.checkbox[i].isChecked():
                self.select[i] = True
                self.editid = i # 最後被點選到的相簿編號,用來修改相簿名稱
            else:
                self.select[i] = False
                
    def EditAlbumName(self,name): # 參考由ean視窗傳送過來的文字進行相簿名稱的修改
        
        self.textstr[self.editid] = name # 將Loadlabel初始化的textstr修改成使用者輸入的新名稱
        self.UpdateLabel() # 即時更新label
        self.checkbox[self.editid].setChecked(False) # 將使用者所有勾選的checkbox初始化為無勾選狀態
        mb.SaveDataForAName(self.editid) # 單獨資料庫裡的picture,不使用mb.savedata()是因為增加儲存效率
        self.editid = -1 # 初始化需傳給修改視窗的id
        
        ean.hide()
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, '警告',"您確定要登出並離開嗎?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            mb.SaveData() # 確保將使用者的資料全部儲存一遍
            mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 登出並保存了所有資料 日期:{:}".format(mb.nickname,mb.account,date))
            event.accept()
        else:
            event.ignore() 
        
        
             
class Root_Picture(QWidget): #相片視窗
            
    def __init__(self):
        
        super().__init__()
        
        # 初始設定值
        self.albumid = -1
        self.labelstate = []
        self.select = []
        self.delcheck = False
        for i in range(0,16):
            self.labelstate.append(False)
            self.select.append(False)
        self.initUI()
        
        
    def initUI(self):               
        
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        self.setGeometry(400, 100, 1024, 768)        
        self.setWindowTitle('電子相簿管理系統 Version 1.0')
        self.setFixedSize(1024, 768)
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(230, 203, 27))
        self.setPalette(p)
                
        self.LoadButton()
        self.LoadLabel()
        self.LoadCheckBox()
        
        self.show()
        
    def LoadButton(self):
        
        self.btn1 = QPushButton('新增照片', self)
        self.btn1.setToolTip('點選此選項新增照片,您最多可以新增15張相片')
        self.btn1.resize(80,80)
        self.btn1.move(925,40) 
        self.btn1.clicked.connect(lambda:self.OnClickButton(0))
        self.btn1.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.btn2 = QPushButton('刪除相片', self)
        self.btn2.setToolTip('點選此選項刪除您不想要留住的相片')
        self.btn2.resize(80,80)
        self.btn2.move(925,140) 
        self.btn2.clicked.connect(lambda:self.OnClickButton(1))
        self.btn2.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
        self.btn3 = QPushButton('返回相簿', self)
        self.btn3.resize(80,40)
        self.btn3.move(440,725) 
        self.btn3.clicked.connect(lambda:self.OnClickButton(2))
        self.btn3.setFont(QFont("微軟正黑體",10,QFont.Bold))  
        
    def LoadLabel(self):
        
        self.labeltitle = QLabel(self)
        self.labeltitle.resize(300,30)
        self.labeltitle.move(30,730)
        self.labeltitle.setFont(QFont("微軟正黑體",15,QFont.Bold))
        self.labeltitle.setStyleSheet('color: gray')
        
        self.label = []
        for i in range(0,15):
            self.label.append(i)
            self.label[i] = QLabel(self)

            if self.labelstate[i] == True:
                pixmap = QPixmap('src/images/ex2.jpg')
            else:
                 pixmap = QPixmap('src/images/ex3.jpg')
            
            pixmap_s = pixmap.scaled(130, 190)
            self.label[i].setPixmap(pixmap_s)
            self.label[i].resize(130,190)
            self.label[i].mousePressEvent = functools.partial(self.OnClickLabel,source_object=self.label[i],ev=0,id=i)
            if i < 5:
                self.label[i].move(20+190*i,20)
            elif i >= 5 and i <= 9:
                j = i-5
                self.label[i].move(20+190*j,260)  
            else:
                j = i-10
                self.label[i].move(20+190*j,500)  
                
        self.textlabel = []
        self.textstr = []
        for i in range(0,15):
            self.textlabel.append(i)
            self.textstr.append("我的相片" + str(i+1))
            self.textlabel[i] = QLabel(self)
            self.textlabel[i].setText(self.textstr[i])
            if i < 5:
                self.textlabel[i].move(60+190*i,220)
            elif i >= 5 and i <= 9:
                j = i-5
                self.textlabel[i].move(60+190*j,460)  
            else:
                j = i-10
                self.textlabel[i].move(60+190*j,700)  
            if self.labelstate[i] == False:
                self.textlabel[i].setVisible(False)
                
    def LoadCheckBox(self):
        
        self.checkbox = []
        for i in range(0,15):
            self.checkbox.append(i)
            self.checkbox[i] = QCheckBox("",self)
            self.checkbox[i].setChecked(False)
            self.checkbox[i].toggled.connect(self.OnCheckboxToggled)
            if i < 5:
                self.checkbox[i].move(25+190*i,25)
            elif i >= 5 and i <= 9:
                j = i-5
                self.checkbox[i].move(25+190*j,265)  
            else:
                j = i-10
                self.checkbox[i].move(25+190*j,505)  
                
            if self.labelstate[i] == False:
                self.checkbox[i].setVisible(False)
                
    def UpdateLabel(self):
        
        self.labeltitle.setText(mb.nickname+"/"+rt.textstr[self.albumid])
        
        for i in range(0,15):            
            if self.labelstate[i] == True:
                ppath ='src/users/'+mb.account+'/album_'+str(self.albumid)+'/'+str(i)+'.jpg'
                pixmap = QPixmap(ppath)
            else:
                pixmap = QPixmap('src/images/ex3.jpg')
                
            pixmap_s = pixmap.scaled(130, 190)
            self.label[i].setPixmap(pixmap_s)
            self.textlabel[i].setText(self.textstr[i])
            if i < 5:
                self.label[i].move(25+190*i,25)
            elif i >= 5 and i <= 9:
                j = i-5
                self.label[i].move(25+190*j,265)  
            else:
                j = i-10
                self.label[i].move(25+190*j,505)  
            
        for i in range(0,15):
            if self.labelstate[i] == True:
                self.textlabel[i].setVisible(True)
                self.checkbox[i].setVisible(True)
            else:
                self.textlabel[i].setVisible(False)
                self.checkbox[i].setVisible(False)
                
    def OnClickButton(self, event):
        
        if event == 0: # 當使用者按下"新增照片"時
            i = 0
            while i < 15:
                if self.labelstate[i] == False:  
                    files,ftype= QFileDialog.getOpenFileName(self,  "選取圖片", "", "(*.jpg);;(*.png);;(*.bmp);;(*.gif)")  #提供選取圖片視窗,只能選擇jpg.png.bmp.gif
                    if files: # 當圖片確定被選擇後
                        if ftype == "(*.jpg)":
                            path = "src/users/"+mb.account+"/album_"+str(self.albumid)+"/"+str(i)+".jpg"
                            shutil.copy(files,path)
                        else: #當副檔名不為jpg時,特別將圖片轉檔為jpg,使整個系統架構較為統一與完整
                            tstr = ""
                            if ftype == "(*.png)": tstr = ".png"
                            elif ftype == "(*.bmp)": tstr = ".bmp"
                            elif ftype == "(*.gif)": tstr = ".gif"
                            path = "src/users/"+mb.account+"/album_"+str(self.albumid)+"/"+str(i)+tstr # 先將未轉為png圖片的檔案複製到使用者相簿裡面,最後由os.remove刪除
                            jpath = "src/users/"+mb.account+"/album_"+str(self.albumid)+"/"+str(i)+".jpg" 
                            shutil.copy(files,path)
                            Image.open(path).convert('RGB').save(jpath)
                            os.remove(path)
                            
                        mb.picture[self.albumid][i] = 1 # 將使用者(Member)類別的照片狀態設為1,代表啟用
                        self.labelstate[i] = True # 將pic的labelstate狀態設定為True,代表照片被啟用
                        self.textstr[i] = "我的相片" + str(i+1)
                        self.UpdateLabel()
                        QMessageBox.question(self, '提示',"您新增了一個相片", QMessageBox.Ok)
                        mb.SaveDataForPicutre(self.albumid,i)
                        mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 新增了一個相片編號:{:}至{:} 日期:{:}".format(mb.nickname,mb.account,i,rt.textstr[self.albumid],date))
                    break
                i+=1
        elif event == 1: # 當使用者按下"刪除照片"時
            if self.delcheck == True:
                reply = QMessageBox.question(self, '警告',"您確定要刪除勾選的相片嗎?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    count , count2 , j = 0 , 0 , 0
                    while j < 15:
                        if self.labelstate[j] == True:
                            count+=1
                        if self.select[j] == True:
                            count2+=1
                        j+=1
                    if count-count2 < 1:
                        QMessageBox.question(self, '提示',"您必須至少留住一張照片在這個相簿裡！", QMessageBox.Ok)
                        return 
                    
                    for i in range(0,15):
                        if self.select[i] == True:
                            mb.picture[self.albumid][i] = 0
                            self.labelstate[i] = False
                            self.UpdateLabel()
                            self.delcheck = False
                            self.checkbox[i].setChecked(False)
                            path = "src/users/"+mb.account+"/album_"+str(self.albumid)+"/"+str(i)+".jpg"
                            os.remove(path)
                            mb.SaveDataForPicutre(self.albumid,i)
                            mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 從{:}刪除了相片編號{:} 日期:{:}".format(mb.nickname,mb.account,rt.textstr[self.albumid],i,date))
        elif event == 2: # 當使用者按下"返回相簿"時
            pic.hide()
            for i in range(0,15):
                self.labelstate[i] = False # 因為使用者回到相簿裡,所以離開前將寫在此類別所有相片狀態設定回False,避免下一個相簿出錯
            rt.UpdateLabel()
            rt.show()
            
    def OnClickLabel(self, event, source_object=None, ev=-1, id=-1): # 當使用者按下圖片時,進入"編輯圖片"視窗
        
        if self.labelstate[id] == True: 
            rb.albumid = self.albumid
            rb.pictureid = id
            rb.UpdateLabel()
            pic.hide()
            rb.show()
            
    def OnCheckboxToggled(self):
        
        self.delcheck = True
        for i in range(0,15):
            if self.checkbox[i].isChecked():
                self.select[i] = True
            else:
                self.select[i] = False
                
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, '警告',"您確定要登出並離開嗎?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            mb.SaveData()
            mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 登出並保存了所有資料 日期:{:}".format(mb.nickname,mb.account,date))
            event.accept()
        else:
            event.ignore() 
            

                 
class Root_Browse(QWidget): # 編輯相片視窗
    
    def __init__(self):
        
        super().__init__()
        self.initUI()
        
        self.albumid = -1 # 初始化選中的相簿為-1,代表目前未選擇任何相簿
        self.pictureid = -1 # 初始化選中的相片為-1,代表目前未選擇任何相簿
        self.temping = False # 當啟動相片效果時為True,預設為False
        
    def initUI(self):  
        
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        self.setGeometry(400, 100, 1024, 768)        
        self.setWindowTitle('電子相簿管理系統 Version 1.0')
        self.setFixedSize(1024, 768)
        
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(230, 203, 27))
        self.setPalette(p)
        
        self.label = QLabel(self)
        pixmap = QPixmap('src/images/ex3.jpg')
        pixmap_s = pixmap.scaled(800, 600)
        self.label.setPixmap(pixmap_s)
        self.label.resize(800,600)
        self.label.move(112,20)
        
        self.label1 = QLabel(self) # 上一張的圖片label
        pixmap = QPixmap('src/images/label1.jpg') # 圖片為"上一張"
        pixmap_s = pixmap.scaled(50,158)
        self.label1.setPixmap(pixmap_s)
        self.label1.resize(50,158)
        self.label1.mousePressEvent = functools.partial(self.OnClickLabel,source_object=self.label1,ev=0)
        self.label1.move(30,280)  
        
        self.label2 = QLabel(self) # 下一張的圖片label
        pixmap = QPixmap('src/images/label2.jpg') # 圖片為"下一張"
        pixmap_s = pixmap.scaled(50,158)
        self.label2.setPixmap(pixmap_s)
        self.label2.resize(50,158)
        self.label2.mousePressEvent = functools.partial(self.OnClickLabel,source_object=self.label2,ev=1)
        self.label2.move(941,280)  
        
        self.label3 = QLabel(self) # 解析度的label
        self.label3.resize(300,30)
        self.label3.move(120,620)
        self.label3.setFont(QFont("微軟正黑體",10,QFont.Bold))
        self.label3.setStyleSheet('color: black')
        
        self.label4 = QLabel(self) # QRCODE的label
        pixmap = QPixmap("src/images/url.svg")
        self.label4.setPixmap(pixmap)
        self.label4.resize(130,130)
        self.label4.move(800,620)  
        self.label4.hide()
        
        self.LoadButton()
                
        self.show()
        
    def LoadButton(self):
        
        btn_name = []
        btn_name.append("旋轉效果")
        btn_name.append("模糊效果")
        btn_name.append("退出照片")
        btn_name.append("輪廓效果")
        btn_name.append("細強效果")
        btn_name.append("真實效果")
        btn_name.append("浮雕效果")
        btn_name.append("焦黑效果")
        btn_name.append("產生網址")
        btn_name.append("新增文字")
        
        self.btn = []
        for i in range(0,10):
            self.btn.append(i)
            self.btn[i] = QPushButton(btn_name[i], self)
            self.btn[i].resize(80,40)
            self.btn[i].setFont(QFont("微軟正黑體",10,QFont.Bold))  
            if i < 5:
                self.btn[i].move(280+i*100,650)
            else:
                j = i-5
                self.btn[i].move(280+j*100,700)  
                
        # 將button設置獨立函數,不將其寫入迴圈是因為經測試它們在create時寫在共同的記憶體,所以會被最後的i取代
        self.btn[0].clicked.connect(lambda:self.OnClickButton(0))
        self.btn[1].clicked.connect(lambda:self.OnClickButton(1))
        self.btn[2].clicked.connect(lambda:self.OnClickButton(2))
        self.btn[2].setStyleSheet('QPushButton {color: red;}')
        self.btn[3].clicked.connect(lambda:self.OnClickButton(3))
        self.btn[4].clicked.connect(lambda:self.OnClickButton(4))
        self.btn[5].clicked.connect(lambda:self.OnClickButton(5))
        self.btn[6].clicked.connect(lambda:self.OnClickButton(6))
        self.btn[7].clicked.connect(lambda:self.OnClickButton(7))
        self.btn[8].clicked.connect(lambda:self.OnClickButton(8))
        self.btn[9].clicked.connect(lambda:self.OnClickButton(9))
        
        self.ebtn = QPushButton('寄發email', self)
        self.ebtn.setToolTip('點選此選項將您的圖片寄發出去,並且可以填寫一些訊息.')
        self.ebtn.resize(80,40)
        self.ebtn.move(925,30) 
        self.ebtn.clicked.connect(lambda:self.OnClickButton(10))
        self.ebtn.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.ebtn.setStyleSheet('QPushButton {color: green;}') # 將按鈕的顏色設置為綠色
        
    def UpdateLabel(self): # 即時更新圖片
        
        self.path = "src/users/"+mb.account+"/album_"+str(self.albumid)+"/"+str(self.pictureid)+".jpg"
        pixmap = QPixmap(self.path)
        pixmap_s = pixmap.scaled(800, 600) # 統一將解析度設置為800x600
        self.label.setPixmap(pixmap_s)
        shutil.copy(self.path,'src/images/temp.jpg') # 為了讓使用者體驗編輯效果,特地將使用者選的圖片複製出來,等使用者確定保存後才會回寫到原圖片檔案
        
        image = Image.open('src/images/temp.jpg') # 打開圖片讀取解析度
        self.width, self.height = image.size
        self.label3.setText(pic.textstr[self.pictureid]+" , "+str(self.width)+"x"+str(self.height)) # 讀取解析度的label
        image.close()
        
    def OnClickButton(self,btnid):
        
        if btnid == 0: #旋轉處理
            im = Image.open('src/images/temp.jpg') # 先打開由剛剛複製的temp圖片
            im = im.rotate(45, Image.BILINEAR) # 效果涵數
            im.save('src/images/temp.jpg') # 保存temp圖片使其不影響原圖檔
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
        elif btnid == 1: #模糊處理
            im = Image.open('src/images/temp.jpg')
            QMessageBox.question(self, '提示',"影像處理中．．．", QMessageBox.Ok)
            for i in range(1): im = im.filter( ImageFilter.BLUR )
            im.save('src/images/temp.jpg')
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
            QMessageBox.question(self, '提示',"影像處理完畢", QMessageBox.Ok)
        elif btnid == 2: # 儲存
            reply = QMessageBox.question(self, '警告',"您確定要保存這張照片嗎\n保存後將會覆蓋原圖片！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes: # 當確定保存後,系統將修改過後的temp回寫到原圖檔
                shutil.copy('src/images/temp.jpg',self.path)
                rb.hide()
                pic.UpdateLabel()
                pic.show()
            else:
                rb.hide()
                pic.UpdateLabel()
                pic.show()
            self.label1.setDisabled(False) 
            self.label2.setDisabled(False) 
            self.label4.hide()
                
        elif btnid == 3: # 輪廓處理
            im = Image.open('src/images/temp.jpg')
            im.filter(ImageFilter.CONTOUR)
            im02= im.filter(ImageFilter.CONTOUR)
            im02.save('src/images/temp.jpg')
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
        elif btnid == 4: # 細節增強
            im = Image.open('src/images/temp.jpg')
            im.filter(ImageFilter.CONTOUR)
            im02= im.filter(ImageFilter.DETAIL)
            im02.save('src/images/temp.jpg')
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
        elif btnid == 5: # 邊界增強
            im = Image.open('src/images/temp.jpg')
            im.filter(ImageFilter.CONTOUR)
            im02= im.filter(ImageFilter.MinFilter)
            im02.save('src/images/temp.jpg')
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
        elif btnid == 6: # 浮雕處理
            im = Image.open('src/images/temp.jpg')
            im.filter(ImageFilter.CONTOUR)
            im02= im.filter(ImageFilter.EMBOSS)
            im02.save('src/images/temp.jpg')
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
        elif btnid == 7: # 焦黑處理
            im = Image.open('src/images/temp.jpg')
            im.filter(ImageFilter.CONTOUR)
            im02= im.filter(ImageFilter.FIND_EDGES)
            im02.save('src/images/temp.jpg')
            pixmap = QPixmap('src/images/temp.jpg')
            pixmap_s = pixmap.scaled(800, 600)
            self.label.setPixmap(pixmap_s)
            self.temping = True
        elif btnid == 8: # 產生網址
            reply = QMessageBox.question(self, '提示',"您即將把圖片轉成永久的專屬網址\n按下確認後我們就會提供您一個QRCODE\n產生網址前請確保您的照片已經保存\n請注意,您的網址請記得自行抄下\n您現在要轉換嗎?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
            #原理: 先由系統決定亂碼為圖片名稱,進而透過FTP上傳到FTP伺服器,然後將伺服器的網址轉成QRCODE
    
            if reply == QMessageBox.Yes:
                rand = random.randint(1000000000,9999999999)
                ftp = ftplib.FTP('106.105.25.121','admin','admin')
                file = open(self.path,'rb') # rb代表以二進位的方式打開
                ftp.storbinary('STOR '+ str(rand) +'.jpg', file)
                file.close()
                string = "http://106.105.25.121/oitmis/" + str(rand) + ".jpg"
                url = pyqrcode.create(string)
                url.svg('src/images/url.svg', scale=3)
                pixmap = QPixmap("src/images/url.svg")
                self.label4.setPixmap(pixmap)
                self.label4.show()
                mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 成功產生一組獨立網址,編號為:{:} 日期:{:}".format(mb.nickname,mb.account,rand,date))
                
            
        elif btnid == 9: # 新增文字
            ebn.show()
            
        elif btnid == 10: # 寄發email
            se.picid = self.pictureid
            se.show()
         
    def OnClickLabel(self, event, source_object=None, ev=-1):
        
        if ev == 0: # 當按下"上一張時",系統由最後一張開始選
            j = 15
            while j >= 0:
                if mb.picture[self.albumid][j] == 1:
                    if j < self.pictureid: # 而當小於目前圖片的編號時,系統找到你此圖片的上一張圖片進行跳離
                        break
                j-=1
            if j == -1: # 當按到最首張時,意味著已經沒有圖片 j 會直接跳到-1, 開始鎖定label提醒使用者沒有圖片可以進行上一張了
                self.label1.setDisabled(True) 
                return
            self.label2.setDisabled(False) # 初始化下一張的按鈕,避免造成同時被鎖定狀態
            self.pictureid = j # 編輯圖片的視窗編號也順勢更新到剛剛跳離的j了
            self.UpdateLabel() # 即時更新圖片label
            self.label4.hide() # QRCODE隨之取消,因為圖片被改變
        
        elif ev == 1: # 當按下"下一張時",系統由首一張開始選
            j = 0
            while j < 15:
                if mb.picture[self.albumid][j] == 1:
                    if j > self.pictureid:
                        break
                j+=1
            if j == 15: 
                self.label2.setDisabled(True) 
                return
            self.label1.setDisabled(False) 
            self.pictureid = j
            self.UpdateLabel()
            self.label4.hide()
        
    def EditBrowseText(self,text,cindex,tindex,lindex):
        
        cstr = "white" # 預設顏色為白色
        tsize = 20 # 預設文字大小為20
        
        # 抓取圖片的寬與高
        width = self.width
        height = self.height
        
        location = [ width*0.05 , height*0.05 ] # 預設位置為左上角
        
        if cindex == 1: cstr = "black"
        elif cindex == 2: cstr = "red"
        elif cindex == 3: cstr = "orange"
        elif cindex == 4: cstr = "yellow"
        elif cindex == 5: cstr = "green"
        elif cindex == 6: cstr = "blue"
        elif cindex == 7: cstr = "purple"
        else: cstr = "white"
        
        if tindex == 1: tsize = 32
        elif tindex == 2: tsize = 44
        elif tindex == 3: tsize = 56
        elif tindex == 4: tsize = 68
        elif tindex == 5: tsize = 80
        elif tindex == 6: tsize = 92
        elif tindex == 7: tsize = 104
        else: tsize = 20
        
        if lindex == 1: location = [ width/2.3 , height*0.05 ] # 正上
        elif lindex == 2: location = [ width/1.3 , height*0.05 ] # 右上
        elif lindex == 3: location = [ width*0.05 , height/2.3 ] # 正左
        elif lindex == 4: location = [ width/2.3 , height/2.3 ] # 正中央
        elif lindex == 5: location = [ width/1.3 , height/2.3 ] # 正右
        elif lindex == 6: location = [ width*0.05 , height/1.3 ] # 左下
        elif lindex == 7: location = [ width/2.3 , height/1.3 ] # 正下
        elif lindex == 8: location = [ width/1.3 , height/1.3 ] # 右下
        else: location = [ width*0.05 , height*0.05 ] # 左上
        
        
        image = Image.open('src/images/temp.jpg')
        font = ImageFont.truetype("msjh.ttc", tsize, encoding="微軟正黑體")   # 設置文字字體及字形
        draw = ImageDraw.Draw(image) # 設定local draw 參考到ImageDraw的instance
        draw.text((location[0],location[1]), text, font=font,fill = cstr) # 設定文字座標以及字體
        image.save('src/images/temp.jpg')
        pixmap = QPixmap('src/images/temp.jpg')
        pixmap_s = pixmap.scaled(800, 600)
        self.label.setPixmap(pixmap_s)
        self.temping = True
        ebn.hide()
        
    def sendtoemail(self,address,subject,text):
        se.picid = -1
        se.hide()

        strFrom = 'clock77392@gmail.com' # 我們創建的官方email
        strTo = address # 欲寄出的email

        # 多用途網際網路郵件擴展
        msgRoot = MIMEMultipart('related') # 使msgRoot參考到MIMEMultipart中的instance為related的形式
        msgRoot['Subject'] = subject # 信箱主旨
        msgRoot['From'] = strFrom # 信箱寄信者
        msgRoot['To'] = strTo # 信箱被寄者
        msgRoot.preamble = text #信箱前言,當信箱被寄送到某用戶時,未被打開時可直覺查看的訊息
        
        #當信箱為純文本模式時的機制的信央內容,一般不會被看到
        msgAlternative = MIMEMultipart('alternative')# 將信箱內容的模式設置為純文本與超文本
        msgRoot.attach(msgAlternative) # 將此模式的機制裝載到msgRoot
        
        #信箱內容
        msgText = MIMEText(text) # 將信箱內容轉乘MIME格式
        msgAlternative.attach(msgText) # 將轉為MIEM格式的訊息裝載到msgRoot

        tstr = '<b>' + text + '</b><br><img src="cid:image1"><br>'
        msgText = MIMEText(tstr, 'html') # 將tstr套用為html的函數格式
        msgAlternative.attach(msgText)

        fp = open(self.path, 'rb') # self.path為已選定的圖片路徑
        msgImage = MIMEImage(fp.read()) # 將路徑套用MIME函數
        fp.close()

        msgImage.add_header('Content-ID', '<image1>') # 新增 html 標籤至msgImage
        msgRoot.attach(msgImage)
        
        msg = msgRoot.as_string() # 將msgRoot所有的訊息裝載到msg
     
        smtpObj = smtplib.SMTP('smtp.gmail.com',587) # SMTP主機為google
        smtpObj.starttls() # 是通訊協定的擴充功能加密連線
        smtpObj.login('clock77392@gmail.com','dd123456') # gmail帳戶與密碼
        smtpObj.sendmail('clock77392@gmail.com', address, msg.encode("utf8")) # 以UTF8的格式正式寄出信箱
        smtpObj.quit() # 結束SMTP連線
        mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 寄出了一封圖片信箱,目標地址為:{:} 日期:{:}".format(mb.nickname,mb.account,address,date))
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, '警告',"您確定要登出並離開嗎??", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            mb.SaveData()
            mb.WriteLog("[伺服器訊息]: 使用者暱稱:{:},帳號:{:} 登出並保存了所有資料 日期:{:}".format(mb.nickname,mb.account,date))
            event.accept()
        else:
            event.ignore() 



class Edit_Album_Name(QWidget): # 編輯相簿名稱視窗
    
    def __init__(self):
        
        super().__init__()
        self.initUI()
        
    def initUI(self):  
        
        self.setGeometry(700, 400, 200, 100)   
        self.setWindowTitle(" ")
        self.setFixedSize(200, 100)
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        
        self.textlabel = QLabel(self)
        self.textlabel.setText('輸入您欲改的相簿名稱')
        self.textlabel.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel.move(20,12)
        self.textlabel.resize(150,16)
                
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 30)
        self.textbox.resize(150,20)
        
        self.btn1 = QPushButton('確定', self)
        self.btn1.move(55,53) 
        self.btn1.clicked.connect(self.OnClickButton)

        self.show()
        
    def OnClickButton(self):
        
        if rt.editid == -1:
            QMessageBox.question(self, '警告',"您尚未選擇欲修改名稱的相簿", QMessageBox.Ok)
        else:
            rt.EditAlbumName(self.textbox.text()) # 將已輸入的新名字回傳到root_album的相簿
            
            
                
class Edit_Browse_Name(QWidget): # 新增文字視窗
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        self.ColorIndex = 0
        self.TextSizeIndex = 0
        self.LocationIndex = 0
        
    def initUI(self):  
        
        self.setGeometry(700, 400, 200, 250)   
        self.setWindowTitle(" ")
        self.setFixedSize(200, 250)
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        
        self.textlabel = QLabel(self)
        self.textlabel.setText('輸入您欲加文字')
        self.textlabel.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel.move(12,12)
        self.textlabel.resize(120,16)
        
        self.textlabel2 = QLabel(self)
        self.textlabel2.setText('字體顏色:')
        self.textlabel2.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel2.move(20,70)
        self.textlabel2.resize(120,16)
        
        self.textlabel3 = QLabel(self)
        self.textlabel3.setText('字體大小:')
        self.textlabel3.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel3.move(20,110)
        self.textlabel.resize(120,16)
        
        self.textlabel4 = QLabel(self)
        self.textlabel4.setText('字體位置:')
        self.textlabel4.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel4.move(20,150)
        self.textlabel4.resize(120,16)
        
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 30)
        self.textbox.resize(150,20)
        
        self.btn = QPushButton('確定', self)
        self.btn.move(55,200) 
        self.btn.clicked.connect(self.OnClickButton)
        
        self.cb = QComboBox(self)
        self.cb.resize(80,20)
        self.cb.move(90,70)
        self.cb.addItems(["白色", "黑色", "紅色", "橘色", "黃色", "綠色", "藍色", "紫色"])
        self.cb.activated.connect(self.OnColorSelect)
        
        self.cb2 = QComboBox(self)
        self.cb2.resize(80,20)
        self.cb2.move(90,110)
        self.cb2.addItems(["10px", "16px", "22px", "28px", "34px", "40px", "46px", "52px"])
        self.cb2.activated.connect(self.OnTextsizeSelect)
        
        self.cb3 = QComboBox(self)
        self.cb3.resize(80,20)
        self.cb3.move(90,150)
        self.cb3.addItems(["左上", "正上", "右上", "正左", "正中央", "正右", "左下", "正下", "右下"])
        self.cb3.activated.connect(self.OnLocationSelect)

        self.show()
        
    def OnClickButton(self):
        rb.EditBrowseText(self.textbox.text(),self.ColorIndex,self.TextSizeIndex,self.LocationIndex)  # 將以上三樣設定回傳到"編輯相片"的視窗
        
    def OnColorSelect(self,index):
        self.ColorIndex = index # 設定顏色編號
        
    def OnTextsizeSelect(self,index):
        self.TextSizeIndex = index # 設定文字編號
        
    def OnLocationSelect(self,index):
        self.LocationIndex = index # 設定位置編號
        
        
        
class Send_Email(QWidget): # 寄信視窗
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):  
        
        self.setGeometry(700, 400, 200, 250)   
        self.setWindowTitle(" ")
        self.setFixedSize(200, 220)
        self.setWindowIcon(QIcon('src/images/logo.ico'))
        
        self.textlabel = QLabel(self)
        self.textlabel.setText('輸入您欲寄出的信箱:')
        self.textlabel.setFont(QFont("微軟正黑體",9,QFont.Bold)) 
        self.textlabel.resize(200,16)
        self.textlabel.move(12,12)
        
        self.textlabel2 = QLabel(self)
        self.textlabel2.setText('輸入您的信箱主旨:')
        self.textlabel2.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel2.resize(200,16)
        self.textlabel2.move(12,58)
        
        self.textlabel3 = QLabel(self)
        self.textlabel3.setText('輸入您的信箱內容:')
        self.textlabel3.setFont(QFont("微軟正黑體",9,QFont.Bold))  
        self.textlabel3.resize(200,16)
        self.textlabel3.move(12,104)
        
        self.textlabel4 = QLabel(self)
        self.textlabel4.setText('P.S.寄發之前圖片請務必先保存!')
        self.textlabel4.setFont(QFont("微軟正黑體",7,QFont.Bold))  
        self.textlabel4.resize(200,16)
        self.textlabel4.move(20,144)
        self.textlabel4.setStyleSheet('QLabel {color: red;}')
                
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 28)
        self.textbox.resize(150,20)
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20, 74)
        self.textbox2.resize(150,20)
        
        self.textbox3 = QLineEdit(self)
        self.textbox3.move(20, 120)
        self.textbox3.resize(150,20)
        
        self.btn = QPushButton('確定', self)
        self.btn.move(55,170) 
        self.btn.clicked.connect(self.OnClickButton)
        
        self.show()
        
    def OnClickButton(self):
        rb.sendtoemail(self.textbox.text(),self.textbox2.text(),self.textbox3.text())  # 將以上住址、主旨、信箱內容回傳到"編輯相片"的視窗
        
        
           
if __name__ == '__main__':
    
    app = QApplication(sys.argv) # 使app 參考到 QApplication 中並載入系統的sys.argv，使pyqt可以使用系統的指令 
    log = Login() # 登入視窗物件
    reg = Register() # 註冊視窗物件
    rt = Root_Album() # 相簿視窗物件
    pic = Root_Picture() # 照片視窗物件
    rb = Root_Browse() # 編輯相片視窗物件
    ean = Edit_Album_Name() # 編輯相簿名稱視窗物件
    ebn = Edit_Browse_Name() # 編輯相片文字視窗物件
    se = Send_Email() # 寄信物件
    mb = Member() # 使用者資料物件
    
    reg.hide()
    rt.hide()
    pic.hide()
    rb.hide()
    ean.hide()
    ebn.hide()
    se.hide()
    
    sys.exit(app.exec_())
