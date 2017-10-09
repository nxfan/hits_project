import tkinter
from tkinter import *
from tkinter import constants
from tkinter import filedialog
import psycopg2
import traceback
import csv
#import text_editor
import os



#cur = conn.cursor()

listfile=[]

class simpleapp_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):

        button = tkinter.Button(self,text=u"Game Data",command=self.OnButtonClick)
        button2 = tkinter.Button(self,text=u"Match Concussion",command=self.OnButtonCLick3)
        #here is the third button to run the script, the command isn't right
        button3 = tkinter.Button(self,text=u"Submit Game Data",command=self.OnButtonClick2)
        l = Label(self, text="Hello! If you would like to upload game data please click the 'Game Data' to select your txt file, then 'Submit Game' Data to submit.")
        l2 = Label(self, text="If you would like to match a concussion please click 'Match Concussion'.")

        button2.pack(side='bottom',padx=15,pady=15)
        button3.pack(side='bottom',padx=15,pady=15)
        button.pack(side='bottom',padx=15,pady=15)
        
        l.pack(side='top',padx=15,pady=5) 
        l2.pack(side='top',padx=15,pady=5)
        
         

    def OnButtonClick(self):
        x = filedialog.askopenfilename(title='Please select data directory')
        listfile.append(x)

    def OnButtonClick2(self):
        try:
            conn = psycopg2.connect("dbname='nxfan' user='nxfan' password='961024650615'")
            print("connected to database")
        except psycopg2.Error as e:
            print ("I am unable to connect to the database")
            print (e)
            print (e.pgcode)
            print (e.pgerror)
            print (traceback.format_exc())
        print(listfile)
        cur = conn.cursor() 
        for txtfile in listfile: 
            with open(txtfile) as csvfile:
                spamreader=csv.reader(csvfile, delimiter='\t')
                for i, row in enumerate(spamreader):
                    if i>5:
                        eventid=row[0]
                        playerid=row[3]
                        primaryposition=row[6]
                        eventdate=row[8]
                        eventtime=row[9]
                        lolpython=list(eventtime)
                        lolpython[5]=':'
                        eventtime="".join(lolpython)
                        lolpython=list(eventdate)
                        lolpython[2]=lolpython[5]='-'
                        eventdate="".join(lolpython)
                        timestamp=eventdate+' '+eventtime
                        linear=row[14]
                        rotation=row[25]
                        cur.execute("INSERT INTO hits (Eventid, playerid, primaryposition, impacttime, linearforce, rotationalforce) SELECT %s,%s,%s,%s,%s,%s WHERE NOT EXISTS (SELECT 1 FROM hits WHERE Eventid= %s);",(eventid,playerid,primaryposition,timestamp,linear,rotation,eventid))
                        cur.execute("INSERT INTO players (playerid) SELECT %s WHERE NOT EXISTS (SELECT 1 FROM players WHERE playerid = %s);", (playerid, playerid))
                        cur.execute("SELECT COUNT(*) FROM hits WHERE Eventid = 513643")
                        x=cur.fetchall()
                        conn.commit()
                        print(x)
    def OnButtonCLick3(self):
        #self.counter += 1
        def EventIdMatch():
            try:
                conn = psycopg2.connect("dbname='nxfan' user='nxfan' password='961024650615'")
                print("connected to database")
            except psycopg2.Error as e:
                print ("I am unable to connect to the database")
                print (e)
                print (e.pgcode)
                print (e.pgerror)
                print (traceback.format_exc())
            print(listfile)
            cur = conn.cursor()
            print("hello")
        
        def OnButtonClick5():
            def PlayerIdMatch():
                try:
                    conn = psycopg2.connect("dbname='nxfan' user='nxfan' password='961024650615'")
                    print("connected to database")
                except psycopg2.Error as e:
                    print ("I am unable to connect to the database")
                    print (e)
                    print (e.pgcode)
                    print (e.pgerror)
                    print (traceback.format_exc())
                    print(listfile)
                cur = conn.cursor()

                temp_id = eventidentry.get()
                month_time = month.get()
                date_time = date.get()
                year_time = year.get()
                if(month_time == "" or date_time == "" or year_time == ""):
                    error = Toplevel(self)
                    errormessage = Label(error, text="Error: No Date was entered.")
                    errormessage.pack(side='top',padx=20,pady=20)

                time = str(month_time)+'/'+str(date_time)+'/'+str(year_time)
                cur.execute("select extract (doy from timestamp %s)",[time])
                doy = cur.fetchall()[0][0]
                print(doy)
                if(temp_id== ""):
                    error = Toplevel(self)
                    errormessage = Label(error, text="Error: No ID was entered.")
                    errormessage.pack(side='top',padx=20,pady=20)
                cur.execute("select * from hits where (linearforce + rotationalforce) = (select MAX(linearforce + rotationalforce) from hits where extract(doy from impacttime) = %s) and  playerid = %s",[doy,temp_id])
                event = cur.fetchall()
                eventid = event[0][0]
                print(temp_id)
                print(eventid)
                playerid = event[0][1]
                linearforce = event[0][4]

                cur.execute("select count from numhits where playerid = %s", [playerid])
                data= cur.fetchall()
                playernum_hit = data[0][0]
                print(playernum_hit)

                cur.execute("select * from numhits where playerid != %s ORDER BY abs((select count from numhits where playerid = %s)-count) limit 5",[playerid,playerid])
                numhits_data=cur.fetchall()
                hits_data = []
                for player_id, count in numhits_data:
                    cur.execute("select * from hits where extract(doy from impacttime) = (select extract(doy from impacttime) from hits where eventid = %s) and playerid = %s order by abs(%s - linearforce) limit 1", (eventid,player_id, linearforce))
                    hits_data.append(cur.fetchall())   

                cur.execute("select *  from players where playerid = %s", [playerid])
                player_data = cur.fetchall()
                output = Toplevel(self)
                entered_data = Label(output, text = "Here is the data on the entered EventID:")
                playerdataout = 'Player Name: ' + str(player_data[0][1]) + '    Player ID: ' + str(player_data[0][0])  + '    Weight: ' + str(player_data[0][2]) + '    Height: ' + str(player_data[0][3]) + '    Age: ' + str(player_data[0][4])
                entered_data2 = Label(output, text = playerdataout)
                entered_data.grid(row = 0, column=5,padx = 5, pady = 5)
                entered_data2.grid(row = 1,column=5, padx=5,pady=5)
                

                match_string = [['Match', 'EventID', 'PlayerID', 'Primary Position', 'Impact Time', 'Linear Force', 'Rotational Force', 'Number of Impacts', 'Diff Linear Force', 'Diff Number of Impacts']]
                count = 1
                for i in hits_data:
                    # cur.execute("select count from numhits where playerid = %s", [i[1]])
                    # num_impact=cur.fetchall()
                    for one,two,three,four,five,six in i:
                        cur.execute("select count from numhits where playerid = %s", [two])
                        num_impact=cur.fetchall()
                        print(num_impact[0])
                        match_row = [str(count), str(one), str(two), str(three), str(four), str(five), str(six), str(num_impact[0][0]), str(float(linearforce)-float(five)), str(int(playernum_hit) - int(num_impact[0][0]))]
                        match_string.append(match_row)
                    count +=1

                i = 3
                for row in match_string:
                    j = 0
                    print(row)
                    for item in row:
                        out = Label(output, text = item)
                        out.grid(row=i,column=j,padx=5,pady=5)
                        j+=1
                    i+=1
                
            t.destroy()
            e=Toplevel(self)
            l = Label(e,text = "Please enter the PlayerID")
            m = Label(e,text = "Month")
            d = Label(e,text = "Date")
            y = Label(e,text = "Year")
            l.pack(side="top", fill="both",expand=True,padx = 15, pady=15)
            eventidentry = Entry(e)
            month = Entry(e,text="Month")
            date = Entry(e, text="Date")
            year = Entry(e,text="Year")
            eventid_match = tkinter.Button(e,text=u"Match",command=PlayerIdMatch)
            eventid_match.pack(side='bottom',padx=15,pady=15)
            year.pack(side='bottom',padx=15,pady=15)
            y.pack(side="bottom", fill="both",expand=True,padx = 15, pady=15)
            date.pack(side='bottom',padx=15,pady=15)
            d.pack(side="bottom", fill="both",expand=True,padx = 15, pady=15)
            month.pack(side='bottom',padx=15,pady=15)
            m.pack(side="bottom", fill="both",expand=True,padx = 15, pady=15)
            eventidentry.pack(side='bottom',padx=15,pady=15)
        def OnButtonClick4():
            def EventIdMatch():
                try:
                    conn = psycopg2.connect("dbname='nxfan' user='nxfan' password='961024650615'")
                    print("connected to database")
                except psycopg2.Error as e:
                    print ("I am unable to connect to the database")
                    print (e)
                    print (e.pgcode)
                    print (e.pgerror)
                    print (traceback.format_exc())
                    print(listfile)
                cur = conn.cursor()

                eventid = eventidentry.get()
                #print(eventid)
                if(eventid == ""):
                    error = Toplevel(self)
                    errormessage = Label(error, text="Error: No ID was entered.")
                    errormessage.pack(side='top',padx=20,pady=20)
                cur.execute("select * from hits where Eventid = %s", [eventid])
                data = cur.fetchall()
                playerid = data[0][1]
                linearforce = data[0][4]
                cur.execute("select count from numhits where playerid = %s", [playerid])
                data= cur.fetchall()
                playernum_hit = data[0]
                print(playernum_hit)

                cur.execute("select * from numhits where playerid != %s ORDER BY abs((select count from numhits where playerid = %s)-count) limit 5",[playerid,playerid])
                numhits_data=cur.fetchall()
                hits_data = []
                for player_id, count in numhits_data:
                    cur.execute("select * from hits where extract(doy from impacttime) = (select extract(doy from impacttime) from hits where eventid = %s) and playerid = %s order by abs(%s - linearforce) limit 1", (eventid,player_id, linearforce))
                    hits_data.append(cur.fetchall())   

                cur.execute("select *  from players where playerid = %s", [playerid])
                player_data = cur.fetchall()
                output = Toplevel(self)
                entered_data = Label(output, text = "Here is the data on the entered EventID:")
                playerdataout = 'Player Name: ' + str(player_data[0][1]) + '    Player ID: ' + str(player_data[0][0])  + '    Weight: ' + str(player_data[0][2]) + '    Height: ' + str(player_data[0][3]) + '    Age: ' + str(player_data[0][4])
                entered_data2 = Label(output, text = playerdataout)
                entered_data.grid(row = 0, column=5,padx = 5, pady = 5)
                entered_data2.grid(row = 1,column=5, padx=5,pady=5)
                

                match_string = [['Match', 'EventID', 'PlayerID', 'Primary Position', 'Impact Time', 'Linear Force', 'Rotational Force', 'Number of Impacts', 'Diff Linear Force', 'Diff Number of Impacts']]
                count = 1
                for i in hits_data:
                    # cur.execute("select count from numhits where playerid = %s", [i[1]])
                    # num_impact=cur.fetchall()
                    for one,two,three,four,five,six in i:
                        cur.execute("select count from numhits where playerid = %s", [two])
                        num_impact=cur.fetchall()
                        print(num_impact[0])
                        match_row = [str(count), str(one), str(two), str(three), str(four), str(five), str(six), str(num_impact[0][0]), str(float(linearforce)-float(five)), str(int(playernum_hit[0]) - int(num_impact[0][0]))]
                        match_string.append(match_row)
                    count +=1

                i = 3
                for row in match_string:
                    j = 0
                    print(row)
                    for item in row:
                        out = Label(output, text = item)
                        out.grid(row=i,column=j,padx=5,pady=5)
                        j+=1
                    i+=1

            t.destroy()
            e=Toplevel(self)
            l = Label(e,text="Please enter the EventID")
            l.pack(side="top", fill="both",expand=True,padx = 15, pady=15)
            eventidentry = Entry(e)
            eventid_match = tkinter.Button(e,text=u"Match",command=EventIdMatch)
            eventid_match.pack(side='bottom',padx=15,pady=15)
            eventidentry.pack(side='bottom',padx=15,pady=15)
        t=Toplevel(self)
        l = Label(t, text="Do you have the EventID?")
        l.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        button4 = tkinter.Button(t,text=u"Yes",command=OnButtonClick4)
        button5 = tkinter.Button(t,text=u"No",command=OnButtonClick5)
        button5.pack(side='right',padx=15,pady=15) 
        button4.pack(side='left',padx=15,pady=15) 

def main():
    app = simpleapp_tk(None)
    app.title('HITS ANALYZER')
    app.mainloop()

if __name__ == "__main__":
    main()
