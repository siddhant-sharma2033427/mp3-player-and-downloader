import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import os
from os import path
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image  
import PIL
from pygame import mixer
from time import sleep
from threading import Thread
from mutagen.mp3 import MP3
import shutil
from youtubesearchpython import VideosSearch
import urllib.request, io
import youtube_dl
from pytube import YouTube
root = tk.Tk()
root.title("RHYTHM")
photo = tk.PhotoImage(file = "image/mp3_logo.png")
root.iconphoto(False, photo)
root.geometry("550x450")
root.resizable(False, False)
class go_live:
    def __init__(self,root,st):
        self.root = root
        self.st = st
        self.image_track = []
        self.image_label_track = []
        self.label_dict = {}
        self.cur_search_val = []
        self.temp_pb = ""
        self.temp_pb_label = ""
        self.toplevel = Toplevel(self.root)
        self.toplevel.geometry("550x600")
        self.toplevel.grab_set()
        
        self.yscroll = ttk.Scrollbar(self.toplevel,orient = VERTICAL)
        self.yscroll.pack(side = "right",fill = "y",expand = True)
        
        self.my_canvas = Canvas(self.toplevel,yscrollcommand = self.yscroll.set,width = 580,height = 600)
        self.my_canvas.pack(side = "left",fill = "both",expand = True)
        self.my_canvas.configure(scrollregion=(0,0,2100,2100))
        self.yscroll.config(command = self.my_canvas.yview)
        
        self.widget_frame = Frame(self.my_canvas)
        self.widget_frame_id = self.my_canvas.create_window(0,0,window = self.widget_frame,anchor = "nw")
        
        self.thread_obj = Thread(target = self.search)
        self.thread_obj.deamon = True
        self.thread_obj.start()
        self.thread_obj2 = Thread(target = self.link_search)
        self.thread_obj2.deamon = True
        self.thread_obj2.start()
        
        self.search_frame = Frame(self.widget_frame)
        self.search_frame.pack(side = "top",fill = "x",expand = True)
        self.entry_box = Entry(self.search_frame,width = 580)
        self.entry_box.pack(side = "top",fill = "x",expand = True)
        self.entry_box.focus()
        self.search_btn = ttk.Button(self.search_frame,text = "Search",command = self.main_fun_call)
        self.search_btn.pack(side = "left",anchor = "s")
        
        self.result_frame = Frame(self.widget_frame)
        self.result_frame.pack(side = "left",anchor = "ne")
        
        self.result = Label(self.result_frame,text = "Result are")
        self.result.pack()
        
        self.toplevel.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.toplevel.mainloop()
    def main_fun_call(self):
        self.refresh()
        if self.cur_search_val != [] and 'https://youtu.be' == self.cur_search_val[0][:16]:
            self.progressbar()
            self.cur_search_val.append(self.entry_box.get())
        else:
            self.cur_search_val.append(self.entry_box.get())
    def progressbar(self):
                temp_search = Toplevel()
                temp_search.geometry("300x300")
                self.temp_pb_label = Label(temp_search,text = "downloading....  please wait")
                self.temp_pb_label.pack()
                self.temp_pb = ttk.Progressbar(temp_search,orient=HORIZONTAL,mode = "indeterminate",length = 250)
                self.temp_pb.pack()
                self.temp_pb.start()
                temp_search.mainloop()
    def link_search(self):
        
        os.chdir(self.st + "songs")
        while(1):
            if self.cur_search_val != [] and 'https://youtu.be' == self.cur_search_val[0][:16]:
                self.progressbar()
                try:
                    options = {
                            'format':'bestaudio/best',
                            'extractaudio':True,
                            'audioformat':'mp3',
                            'outtmpl': u'%(id)s.%(ext)s',     #name the file the ID of the video
                            'noplaylist':True,
                            'nocheckcertificate':True,
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                                            }]
                                }

                    with youtube_dl.YoutubeDL(options) as ydl:
                        ydl.download([self.entry_box.get()])
                    self.temp_pb_label.config(text = "downloaded")
                    self.temp_pb.stop()
                except:
                        showinfo("Error", "Something went wrong check your connection")
                        self.temp_pb_label.config(text = "Error occured")
                        self.temp_pb.stop()
                self.cur_search_val = []
        
    def search(self):
        os.chdir(self.st + "songs")
        while True:
            if self.cur_search_val !=[]:
                #for_search = self.entry_box.get()
                #print(for_search)
                for_search = self.cur_search_val[0]
                video_search = VideosSearch(for_search,limit = 20)
                result = video_search.result()
                #print(result)
                self.label_dict = {}
                try:
                    for i in range(20):
                        def create_lambda(event , i ,x):
                            try:
                                options = {
                                    'format':'bestaudio/best',
                                    'extractaudio':True,
                                    'audioformat':'mp3',
                                    'outtmpl': u'%(id)s.%(ext)s',     #name the file the ID of the video
                                    'noplaylist':True,
                                    'nocheckcertificate':True,
                                    'postprocessors': [{
                                        'key': 'FFmpegExtractAudio',
                                        'preferredcodec': 'mp3',
                                        'preferredquality': '192',
                                                    }]
                                        }
                                with youtube_dl.YoutubeDL(options) as ydl:
                                    ydl.download([x])
                            except:
                                showinfo("Error", "Some thing went wrong check your connection")
                            
                        im = self.thumb(url = result['result'][i]['link'])
                        self.image_track.append(im)
                        temp2 = Label(self.result_frame,image = im)
                        temp2.pack()
                        
                        temp = Label(self.result_frame,text = result['result'][i]['title'])
                        temp.pack()
                        self.label_dict['frame'+str(i)] = temp
                        self.label_dict['frame'+str(i)].bind("<ButtonRelease-1>",lambda eve ,i = i:  create_lambda(eve,i,result['result'][i]['link']))
                        
                        #print(result["result"][i]["title"])
                    
                except:
                    pass
                self.cur_search_val = []
            
            
    def thumb(self,url):
        yt = YouTube(url)
        raw_data = urllib.request.urlopen(yt.thumbnail_url).read()
        im = Image.open(io.BytesIO(raw_data)).resize((100, 100))
        image = ImageTk.PhotoImage(im)
        return image
    def refresh(self):
        for child in self.result_frame.winfo_children():
            child.destroy()
    def on_closing(self):
        self.toplevel.grab_release()
        self.toplevel.destroy()
        
        

class main_window():
    def __init__(self,root):
        self.root = root
        mixer.init()
        
        self.ispause = False
        self.cur = 0
        self.is_exit = False
        self.cur_song_length = 0
        self.cur_song_time = 0
        self.is_loop = 0
        #list for storing all file in list box
        self.lis = {}
        #string for cwd
        self.st = os.getcwd() + r"\ ".replace(" ","")
        #variable for checking wether player is mute or not
        self.is_mute = False
        
        #creating image variable for adding image to buttons
        open_folderImage = tk.PhotoImage(file = self.st + r"image\open_folder2.png")
        open_fileImage = tk.PhotoImage(file =self.st +  r"image\open-file2.png")
        go_onlineImage = tk.PhotoImage(file = self.st + r"image\go_online.png")
        rename_image = self.resize(self.st + r"image\rename_icon.png",20,20)
        delete_image = self.resize(self.st + r"image\delete_icon.png",20,20)
        
        
        
        
        #creating label frame for buttons
        self.label_frame1 = ttk.Frame(self.root)
        self.label_frame1.grid(row = 0,column = 0)
        
        self.music_box= ttk.LabelFrame(self.root,text = "Music box")
        self.music_box.grid(row = 1,column = 1,sticky = "ne")
        Grid.rowconfigure(self.root,1,weight = 1)
        Grid.columnconfigure(self.root,1,weight = 1)
        
        self.list_box_frame = ttk.LabelFrame(self.root,text = "list box",width = 20)
        self.list_box_frame.grid(row = 1,column = 0,sticky = "nsw")
        Grid.rowconfigure(self.root,1,weight = 2)
        Grid.columnconfigure(self.root,0,weight = 2)
        
        #buttons
        self.open_file = ttk.Button(self.label_frame1,image=open_fileImage,command=lambda :self.openfile(self.list_box))
        self.open_folder = ttk.Button(self.label_frame1,image=open_folderImage,command = lambda :self.openfolder(self.list_box))
        self.go_online = ttk.Button(self.label_frame1,image = go_onlineImage,command = lambda : go_live(self.root,self.st))
        self.rename_btn = ttk.Button(self.label_frame1,image = rename_image,command = self.rename)
        self.delete_btn = ttk.Button(self.label_frame1,image = delete_image,command = self.delete)
        
        #button pack
        self.open_file.pack(side = "left",padx = "10")
        self.open_folder.pack(side = "left",padx = "10")
        self.go_online.pack(side = "left",padx = "10")
        self.rename_btn.pack(side = "left",padx = "10")     
        self.delete_btn.pack(side = "left",padx = "10")
        
        #list box in first frame
        self.scroll_bar1 = ttk.Scrollbar(self.list_box_frame,orient = VERTICAL)
        self.scroll_bar1.grid(column = 1,sticky = "nsew")
        self.scroll_bar2 = ttk.Scrollbar(self.list_box_frame,orient = HORIZONTAL)
        self.scroll_bar2.grid(row = 1,sticky = "nsew")
        
        self.list_box = tk.Listbox(self.list_box_frame,yscrollcommand=self.scroll_bar1.set,xscrollcommand=self.scroll_bar2.set,width = 20)
        self.list_box.grid(row = 0,column = 0,sticky = "nsw")
        Grid.rowconfigure(self.list_box_frame,0,weight = 1)
        Grid.columnconfigure(self.list_box_frame,0,weight = 1)
        
        self.scroll_bar1.config(command = self.list_box.yview)
        self.scroll_bar2.config(command = self.list_box.xview)
        
        
        #music buttons
        os.chdir(self.st)
        
        self.thumbnail_bg = self.resize(self.st + r"image\no_thumb.png",300,200)
        self.thumb_label = Label(self.music_box,image = self.thumbnail_bg).grid(row = 0,column = 0,sticky = "w")
        
        self.cur_song = ttk.Label(self.music_box,text = "")
        self.cur_song.grid(row = 1,column = 0)
        
        self.scale = ttk.Scale(self.music_box,from_ = 0,to = 100,value = 0,length = 300,command = self.myslider)
        self.scale.grid(row = 2,column = 0,sticky = "w")
        
        self.btn_frame = ttk.LabelFrame(self.music_box)
        self.btn_frame.grid(row = 3,column = 0,sticky = "w")
        
        self.loop_img = self.resize(self.st + r"image\player_loop.png",30,30)
        self.loop_btn = ttk.Button(self.btn_frame,image = self.loop_img,command = self.player_loop)
        self.loop_btn.grid(row = 0,column = 0,sticky = "w")
        
        self.vol_img = self.resize(self.st + r"image\player_unmute_volume.png",30,30)
        self.vol_btn = ttk.Button(self.btn_frame,image = self.vol_img,command = self.vol_btn_com)
        self.vol_btn.grid(row = 0,column = 1,sticky = "w",padx = 5)
        
        self.vol_scale = ttk.Scale(self.btn_frame,from_ = 0.0,to = 1.0,length = 100,value = 1,command = self.vol_controll)
        self.vol_scale.grid(row = 0,column = 2,sticky = "w")
        
        self.btn_frame2 = ttk.LabelFrame(self.music_box)
        self.btn_frame2.grid(row = 4,column = 0,sticky = "w")
        
        
        self.backword_img = self.resize(self.st + r"image\player_backword.png",30,30)
        self.backword_btn = ttk.Button(self.btn_frame2,image = self.backword_img,command = lambda : self.player_backword())
        self.backword_btn.grid(row = 0,column = 0,sticky = "w",padx = 10)
        
        self.play_img = self.resize(self.st + r"image\player_play.png",30,30)
        self.play_btn = ttk.Button(self.btn_frame2,image = self.play_img,command = lambda : self.pause_unpause())
        self.play_btn.grid(row = 0,column = 1,sticky = "w",padx = 10)
        
        self.forward_img = self.resize(self.st + r"image\player_forward.png",30,30)
        self.forward_btn = ttk.Button(self.btn_frame2,image = self.forward_img,command = lambda : self.player_forward())
        self.forward_btn.grid(row = 0,column = 2,sticky = "nw",padx = 10)
        
        self.stop_img = self.resize(self.st + r"image\player_stop.png",30,30)
        self.stop_btn = ttk.Button(self.btn_frame2,image = self.stop_img,command = lambda:self.player_stop())
        self.stop_btn.grid(row = 0,column = 3,sticky = "nw",padx = 10)
        
        
        self.list_box.bind('<ButtonRelease-1>',self.def_play)
        
        self.first_run()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    def pr(self):
        print(self.lis)
    def first_run(self):
        if path.exists(self.st+r'songs'):
            paths = os.listdir(self.st+r'songs')
            for path1 in paths:
                self.list_box.insert("end",path1)
                self.lis.update({path1 : self.st+r'songs\ '.replace(" ","")+path1})
                
                
        else:
            os.mkdir(self.st+r'songs')
    def resize(self,img,new_width,new_height):
        im = Image.open(img) # image extension *.png,*.jpg
        im = im.resize((new_width, new_height), Image.ANTIALIAS)
        #im = im.thumbnail((new_width, new_height), Image.ANTIALIAS)
        im = PIL.ImageTk.PhotoImage(im)
        #im = PhotoImage(img)
        return im
    def openfolder(self,root):
        
        file_path = filedialog.askdirectory(title = "select folder")#asking user to select directory
        file_path = file_path + r"/"#adding / for after use
        file_path2 = os.listdir(file_path)#listing all files in user input directory
        for i in file_path2:
            
            if i.endswith((".mp3",".ogg",".mod")):#if file extention is supported extension then insert to list box and in dictonary
                if path.exists(self.st + r'songs\ '.replace(" ","")+i) == False and i not in self.lis:#check if file is already exist in songs forlder or not
                    shutil.copy(file_path+i, self.st + r'songs')#copy frile from user dir to song dir
                    self.lis.update({i : self.st + r"songs\ ".replace(" ","")+i})#update dictonary
                    print(i , file_path,file_path+i)
                    root.insert("end",i)#insert all file in list box
                
        
    def openfile(self,root):
        file_path = filedialog.askopenfilenames(title="select file",filetype=(("MP3",".mp3"),("OGG",".ogg"),("MOD",".mod")))#asking user to select file with specifi extention
        for i in file_path:#looping incase user select multiple files
            if path.exists(self.st + r'songs\ '.replace(" ","")+path.basename(i)) == False and path.basename(i) not in self.lis:#checking if file already exist in song folder or not
                self.lis[path.basename(i)] = self.st + r"songs\ ".replace(" ","") + path.basename(i)#updating dictonary
                root.insert("end",path.basename(i))#insering file name in list box
                shutil.copy(i,self.st + r'songs')#copying file fron user dir to song dir
            else:
                showinfo("Already exist", "song you are trying to add is already present")
    def rename(self):
        file_name = self.list_box.curselection()[0]
        def save():
            
            #print(self.st + "songs\ ".replace(" ","")+rename_entry.get())
            ext = os.path.splitext(self.list_box.get(file_name))[1]#extracting extention
            new_name = rename_entry.get()#extracting user entered name
            new_path = self.st+"songs\ ".replace(" ","") + new_name + ext #new path for new File
            print(new_path)
            if path.basename(new_path) not in self.lis:
                mixer.music.unload()#unloading mixer so that file can be renamed
                os.rename(self.st + "songs\ ".replace(" ","")+self.list_box.get(file_name),new_path)#renaming using os
                del self.lis[self.list_box.get(file_name)] # deleting old key value pair
                self.lis[path.basename(new_path)] = new_path #inserting new path and name
                self.list_box.delete(file_name) #deleting current selection from list
                self.list_box.insert("end",path.basename(new_path)) #inserting new name at the end of list box
                print(self.lis)
            temp.destroy()#destroying root window
        temp = Toplevel(self.root)
        temp.geometry("200x100")
        temp.title("Rename Window")
        temp.resizable(False, False)
        rename = Label(temp,text = "Enter New Name Without extention")
        rename.pack(side = "top")
        rename_entry = Entry(temp,width = 30)
        rename_entry.pack(side = "top",anchor = "w")
        rename_entry.focus()
        save_btn = ttk.Button(temp,text = "Save",command = save)
        save_btn.pack(side = "left",anchor = "w")
        
        temp.mainloop()
        #os.rename()
    def delete(self):
        mixer.music.unload()
        file_name = self.list_box.curselection()[0]
        del self.lis[self.list_box.get(file_name)]
        os.remove(self.st + "songs\ ".replace(" ","")+self.list_box.get(file_name))
        self.list_box.delete(file_name)
        
    def play(self):
        if self.cur!=len(self.lis):
            
            self.cur_song_time = 0
            mus = self.list_box.get(self.cur)
            mixer.music.load(self.lis[mus])
            print("is_loop = ",self.is_loop)
            mixer.music.play(loops = self.is_loop)
            self.cur_song.config(text = f'currently playing {mus}')
            try:
                self.cur_song_length = MP3(self.lis[mus])
                self.cur_song_length = self.cur_song_length.info.length
            except:
                self.cur_song_length = mixer.Sound(self.lis[mus])
                self.cur_song_length = self.cur_song_length.get_length()
                #getting current volume
            #self.vol_scale.set(value = float(mixer.Sound.get_volume))
            self.scale.config(value = 0,to = self.cur_song_length)
            self.curr_time()
    def player_backword(self):
        try:
            self.is_loop = 0
            self.cur = self.list_box.curselection()[0]
            if self.cur != 0:
                self.cur -= 1
                mus = self.list_box.get(self.cur)
                self.list_box.selection_clear(0,END)
                self.list_box.activate(self.cur)
                self.list_box.selection_set(self.cur,last = None)
                self.is_exit = True
                #mixer.music.load(self.lis[mus])
                #`mixer.music.play()
                thread_obj2 = Thread(target = self.play())
                thread_obj2.daemon = True
                thread_obj2.start()
        except:
            print("error")
    def player_forward(self):
        try:
            self.is_loop = 0
            self.cur = self.list_box.curselection()[0]
            print(self.list_box.curselection()[0])
            if self.cur != len(self.lis)-1:
                self.cur += 1
                mus = self.list_box.get(self.cur)
                self.list_box.selection_clear(0,END)
                self.list_box.activate(self.cur)
                self.list_box.selection_set(self.cur,last = None)
                #self.cur_song.config(text = f'currently playing {mus}')
                #mixer.music.load(self.lis[mus])
                #mixer.music.play()
                self.thread_obj = Thread(target = lambda : self.play())
                self.thread_obj.daemon = True
                self.thread_obj.start()
        except :
            print("error")
    def pause_unpause(self):
        if self.ispause == False:
            self.ispause = True
            mixer.music.pause()
            self.play_img= self.resize(r"image/player_pause.png",30,30)
            self.play_btn.config(image = self.play_img)
        else:
            self.ispause = False
            self.play_img = self.resize(r"image/player_play.png",30,30)
            self.play_btn.config(image = self.play_img)
            mixer.music.unpause()
    def player_stop(self):
        mixer.music.stop()
        mixer.music.unload()
        self.list_box.selection_clear(0,END )
    def player_loop(self):
        print(self.is_loop)
        mus = self.list_box.get(self.cur)
        mixer.music.load(self.lis[mus])
        if self.is_loop == 0:
            self.is_loop = -1
            print(self.is_loop)
            mixer.music.play(loops = self.is_loop)
        else:
            self.is_loop = 0
            print(self.is_loop)
            mixer.music.play(loops = self.is_loop)
            
    def def_play(self,event):
        mus = self.list_box.curselection()[0]
        self.cur = mus
        self.is_loop = 0
        self.play()
        print(mus,type(mus))
    def myslider(self,event):
        mus = self.list_box.get(self.cur)
        mixer.music.load(self.lis[mus])
        mixer.music.play(loops = self.is_loop,start = int(self.scale.get()))
    def curr_time(self):
        self.cur_song_time = mixer.music.get_pos()//1000
        
        #self.scale.config(value=self.cur_song_time+1)
        
        if int(self.scale.get()) == int(self.cur_song_length):
            self.scale.config(value = 0)
        elif int(self.scale.get()) == self.cur_song_time+1:
            self.scale.config(value=self.cur_song_time+1)
        elif mixer.music.get_busy() == False:
            self.scale.config(value = 0)
        elif mixer.music.get_busy() == False:
            self.player_forward()
        else:
            self.scale.config(value = int(self.scale.get()))
            new_time = int(self.scale.get())
            self.scale.config(value = new_time+1)
        
        self.cur_song.config(text = f'currently playing {int(self.scale.get())}:{int(self.cur_song_time)}')
        
        self.root.after(1000,self.curr_time)
    def vol_controll(self,event):
        mixer.music.set_volume(self.vol_scale.get())
    def vol_btn_com(self):
        if self.is_mute == False:
            self.vol_img = self.resize(self.st + r"image\player_mute_volume.png",30,30)
            self.vol_btn.config(image = self.vol_img)
            mixer.music.set_volume(0)
            self.is_mute = True
        else:
            self.vol_img = self.resize(self.st + r"image\player_unmute_volume.png",30,30)
            self.vol_btn.config(image = self.vol_img)
            mixer.music.set_volume(self.vol_scale.get())
            self.is_mute = False
    def on_closing(self):
        mixer.quit()
        self.root.destroy()
obj = main_window(root)
