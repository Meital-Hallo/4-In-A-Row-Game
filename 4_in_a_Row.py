import tkinter as tk
from tkinter import font
import numpy as np
from PIL import Image,ImageTk
global cnt, BoardSize,app, Turn_button

# Initializa Vars
BoardSize=[6,7];
Board=np.zeros(BoardSize);
button_dict = {} # Stores button references here
cnt=1;


def init_Players(photos):
    Player1={"Id": 1, "Photo": photos[2], "Photo_turn": photos[4]};
    Player2={"Id": 2, "Photo": photos[1], "Photo_turn": photos[3]};
    Players=[Player1, Player2]
    return Players


def GetPlayerID(Players):
    global cnt
    if (cnt % 2) == 0:
        CurPlayer=Players[1]
    else:
        CurPlayer=Players[0]
    return CurPlayer
    
def Restart(photos,button_dict):
    global cnt, BoardSize, Board, Turn_button
    cnt=1;
    Cols=np.where(Board!=0)[1]
    Rows=np.where(Board!=0)[0]
    Board=np.zeros(BoardSize);
    for i in range(0,len(Cols)):
        button_dict[Rows[i],Cols[i]]["image"]=photos[0]
        button_dict[Rows[i],Cols[i]]["bg"]="#00A2E8"
    for Btn in button_dict:
        button_dict[Btn]["state"] = 'normal'
        
    # Change the Cur_player Color to yellow.
    cur_player=GetPlayerID(Players)
    Turn_button["image"]=cur_player["Photo_turn"]

        
def Retry(photos,button_dict):
    global cnt, BoardSize, Board, Row, column
    cnt=cnt-1;
    Board[Row,column]=0;
    button_dict[Row,column]["image"]=photos[0]
    button_dict[Row,column]["bg"]="#00A2E8"
    for Btn in button_dict:
        button_dict[Btn]["state"] = 'normal'
        button_dict[Btn]["bg"]="#00A2E8"


def play(btn,button_dict,photo):
    global cnt, BoardSize, Board, Row, app, column
    column = btn.grid_info()['column'] # grid_info will return dictionary with all grid elements (row, column, ipadx, ipday, sticky, rowspan and columnspan)
    try:
        Row=list(np.where(Board[:,column]==0))[0][-1];
    except: #if Row>BoardSize[0]-1: 
        return()
    
    
    cur_player=GetPlayerID(Players)
    for irow in range(Row):
        button_dict[(irow,column)]["image"]=cur_player["Photo"]
        app.after(50)
        app.update()
        button_dict[(irow,column)]["image"]=photo[0]

    button_dict[(Row,column)]["image"]=cur_player["Photo"]
    Board[Row, column]=cur_player['Id'];
      
    CheckVictory(Players, Row, column, button_dict) 
    
    # Change the "Turn Button" 
    cnt=cnt+1
    cur_player=GetPlayerID(Players)
    Turn_button["image"]=cur_player["Photo_turn"]


def DisplayWin(button_dict, Lst):
    print(Lst)
    for i in range(len(Lst[0])):
        button_dict[(Lst[0][i],Lst[1][i])]["bg"]='lightgreen'
    
    for Btn in button_dict:
        button_dict[Btn]["state"] = 'disabled'
        

def CheckVictory(Players, Row, column, button_dict):
    global Board
    cur_player=GetPlayerID(Players)

    # Down
    Lst=[[Row], [column]];
    for i in range(Row+1, BoardSize[0]):  
        if Board[i,column]==Board[Row,column]:
            Lst[0].append(i)
            Lst[1].append(column)
        else:
            break
    if len(Lst[0])>3: DisplayWin(button_dict, Lst)
    
    
    # Right Side & Left Side
    Lst=[[Row], [column]];
    for i in range(column+1, BoardSize[1]):
        if Board[Row,column]==Board[Row,i]:
            Lst[0].append(Row)
            Lst[1].append(i)
        else:
            break 
    for i in range(column, 0,-1):  
        if Board[Row,column]==Board[Row,i-1]:
            Lst[0].append(Row)
            Lst[1].append(i-1)
        else:
            break
    if len(Lst[0])>3: DisplayWin(button_dict, Lst)
 

    # Diagonal Negative Slope
    Lst=[[Row], [column]];
    for i in range(1, min(BoardSize[0]-Row, BoardSize[1]-column)):
        if Board[Row,column]==Board[Row+i,column+i]:
                Lst[0].append(Row+i)
                Lst[1].append(column+i)
        else:
            break
    for i in range(1,min([Row,column])):  
            if Board[Row,column]==Board[Row-i,column-i]:
                Lst[0].append(Row-i)
                Lst[1].append(column-i)
            else:
                break   
    if len(Lst[0])>3: DisplayWin(button_dict, Lst)

    # Diagonal Positive Slope
    Lst=[[Row], [column]];
    for i in range(1, min(Row, BoardSize[1]-column)):
        if Board[Row,column]==Board[Row-i,column+i]:
                Lst[0].append(Row-i)
                Lst[1].append(column+i)
        else:
            break
    for i in range(1,min([BoardSize[0]-Row,column])):  
            if Board[Row,column]==Board[Row+i,column-i]:
                Lst[0].append(Row+i)
                Lst[1].append(column-i)
            else:
                break   
    if len(Lst[0])>3: DisplayWin(button_dict, Lst)


# Create the app
app = tk.Tk()
display_frame = tk.Frame(master=app)
display_frame.pack(fill=tk.X)
display = tk.Label(master=display_frame,text="4 In A Row", font=font.Font(size=10, weight="bold"))
display.pack()

# Create Images
photo_white = ImageTk.PhotoImage( Image.open(r'ButtonImages/white.png').resize((60,60)), Image.ANTIALIAS )
photo_red = ImageTk.PhotoImage( Image.open(r'ButtonImages/red.png').resize((50,50)))
photo_yellow = ImageTk.PhotoImage( Image.open(r'ButtonImages/yellow.png').resize((50,50)))
photo_red_turn=ImageTk.PhotoImage( Image.open(r'ButtonImages/red.png').resize((30,30)))
photo_yellow_turn=ImageTk.PhotoImage( Image.open(r'ButtonImages/yellow.png').resize((30,30)))
photos=[photo_white,photo_red, photo_yellow,photo_red_turn,photo_yellow_turn]
Players=init_Players(photos)


grid_frame_button = tk.Frame(master=app,bg='#00A2E8')
# Button for closing 
exit_button = tk.Button(grid_frame_button, text="X", bg='#F79787', height= 1, width=5, activeforeground='grey', font=font.Font(size=10, weight="bold"),fg="white", command=app.destroy) 
exit_button.grid(row=0,column=0, padx=2, pady=5)

# Button for restart 
photo_Restart = ImageTk.PhotoImage( Image.open(r'ButtonImages/restart.png').resize((20,20)), Image.ANTIALIAS )
restart_button = tk.Button(grid_frame_button, image=photo_Restart, command=lambda button_dict=button_dict, photo=photos:Restart(photos,button_dict)) 
restart_button.grid(row=0,column=1, padx=2, pady=5) 

# Button for retry 
photo_retry = ImageTk.PhotoImage( Image.open(r'ButtonImages/retry.png').resize((20,20)), Image.ANTIALIAS )
retry_button = tk.Button(grid_frame_button,image=photo_retry, command=lambda button_dict=button_dict, photo=photos:Retry(photos,button_dict)) 
retry_button.grid(row=0,column=2, padx=2, pady=5) 

# Turn Button
Turn_button = tk.Button(grid_frame_button, image=photos[4],bd=0,bg="#00A2E8", text='Turn') 
Turn_button.grid(row=0,column=9, padx=50, pady=5) 
grid_frame_button.pack(fill=tk.X)

grid_frame = tk.Frame(master=app,bg='#00A2E8')
grid_frame.pack(fill=tk.X)
for row in range(BoardSize[0]):
        grid_frame.rowconfigure(row, weight=1, minsize=50)
        for col in range(BoardSize[1]):
            grid_frame.columnconfigure(col, weight=1, minsize=50)
            button = tk.Button(master=grid_frame,text="",font=font.Font(size=10, weight="bold"),bg="#00A2E8", width=2,height=2,bd=0)
            button.config(command=lambda button=button, button_dict=button_dict, photo=photos: play(button,button_dict,photo))
            if row==0:
                button['text']=str(col+1)
            button.grid(row=row,column=col,padx=0,pady=0,sticky="nsew")
            button["image"]=photos[0]
            button_dict[(row,col)] = button # Add reference to your button dictionary
            

app.mainloop()  
    