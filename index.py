''' This program works with MQTT conection of 
IOT in order to turn on light in ESP32 from 
a desktop app'''

###### IMPORT LYBRARIES ########
import ssl                          # Establish secure connection
import sys
import paho.mqtt.client as mqtt    # Connect with the MQTT Library
import time                         # Time Library  
from tkinter import *
from tkinter import ttk, font       # Import Tkinter Lybrary
from tkinter import messagebox
import getpass

class App(ttk.Frame):

    # Window Init
    def __init__(self, window):
        # Initializations 
        self.broker = StringVar()
        self.port2 = StringVar()
        self.username2 = StringVar()             # Save data for frame in window
        self.password2 = StringVar()
        self.topic2 = StringVar()
        self.wind = window
        self.colorfondo1 = "#0B3A80"              # Color fondo#0fbcf9
        self.colorfondo = "#1157C2"                # Color Frame
        self.colorfondo2 = "#1568E6"                # Color Frame
        self.colorfondo3 = "#1774FF"                # Color Frame
        self.colorboton = "#B2EBF2"                # Color Frame
        self.colorletras = "#061D40"               # Color words 1c3836
        #self.wind.geometry('400x450')              # Window Lenght
        self.wind.title("Light Control")           # Window Title
        self.wind.configure(background = self.colorfondo1)
        self.act_time = time.strftime("%Y/%m/%d  %H:%M:%S")
        self.prev_time = "None Data"

        # Creating a Frame Connect 
        self.frameconn = LabelFrame(self.wind, text = "Connection MQTT", font=("Britannic Bold", 14), bg=self.colorfondo, fg=self.colorletras, borderwidth=2, relief="raised")
        self.frameconn.grid(row = 0, column = 1, columnspan = 3, pady = 20,padx=20, sticky=(N, S, E, W))
        
        Label(self.frameconn, text = "Broker: ", font=("Impact Bold", 12), bg=self.colorfondo, fg=self.colorletras).grid(row = 1, column = 0, pady = 3,padx=20)
        self.broker1 = Entry(self.frameconn, textvariable=self.broker)
        self.broker1.grid(row = 1, column = 1, pady = 3,padx=20)
        
        Label(self.frameconn, text = "Port: ", font=("Euphemia", 12), bg=self.colorfondo, fg=self.colorletras).grid(row = 2, column = 0, pady = 3,padx=20)
        self.port1 = Entry(self.frameconn, textvariable=self.port2)
        self.port1.grid(row = 2, column = 1, pady = 3,padx=20)
        
        Label(self.frameconn, text = "Username: ", font=("Euphemia", 12), bg=self.colorfondo, fg=self.colorletras).grid(row = 3, column = 0, pady = 3,padx=20)
        self.username1 = Entry(self.frameconn, textvariable=self.username2)
        self.username1.grid(row = 3, column = 1, pady = 3,padx=20)
        
        Label(self.frameconn, text = "Password: ", font=("Euphemia", 12), bg=self.colorfondo, fg=self.colorletras).grid(row = 4, column = 0, pady = 3,padx=20)
        self.password1 = Entry(self.frameconn, textvariable=self.password2, show="*")
        self.password1.grid(row = 4, column = 1, pady = 3,padx=20)
        
        Label(self.frameconn, text = "Topic: ", font=("Arial", 12), bg=self.colorfondo, fg=self.colorletras).grid(row = 5, column = 0, pady = 3,padx=20)
        self.topic1 = Entry(self.frameconn, textvariable=self.topic2)
        self.topic1.grid(row = 5, column = 1, pady = 3,padx=20)

        self.lblcorr_conn = Label(self.frameconn, text = "", font=("Arial Bold", 12), bg=self.colorfondo, fg=self.colorletras)
        self.lblcorr_conn.grid(row = 6, column = 1, pady = 3,padx=20)

        #self.separ1 = ttk.Separator(self.frameconn, orient=HORIZONTAL)
        #self.separ1.pack(side=TOP, fill=BOTH, expand=True)

        self.btn_connect = Button(self.frameconn, text="Connect", command=self.paconectar,bg=self.colorboton)
        self.btn_connect.grid(row = 7, column = 0, sticky= W+E, pady = 3,padx=20)

        self.btn_not_connect = Button(self.frameconn, text="Disconnect", command=self.padesconectar,bg=self.colorboton)
        self.btn_not_connect.grid(row = 7, column = 1, sticky= W+E, pady = 3,padx=20)
        
        Label(self.frameconn, text = 'State: ', font=("Arial Bold", 12), bg=self.colorfondo, fg=self.colorletras).grid(row = 8, column = 0, pady = 3,padx=20)
        self.lblconnect = Label(self.frameconn, text = 'Not Connected', font=("Arial Bold", 12), bg=self.colorfondo, fg=self.colorletras)
        self.lblconnect.grid(row = 8, column = 1, pady = 3,padx=20)
               
        
        # Creating a Frame Light
        self.framelight = LabelFrame(self.wind, text = "Light State", font=("Britannic Bold", 14), bg=self.colorfondo2, fg=self.colorletras, borderwidth=2, relief="raised")
        self.framelight.grid(row = 9, column = 0, columnspan = 3, pady = 3,padx=20, sticky=(N, S, E, W))
        
        self.btn_rf1 = Button(self.framelight, text="ON", command=self.clicked, font=("Arial Bold", 14),bg=self.colorboton)#.grid(row = 5, column = 0)
        self.btn_rf1.grid(row = 10, column = 0, pady = 3,padx=20)
        self.btn_rf1.config(state = 'disable')
        
        self.lbl_rf1 = Label(self.framelight, text="  OFF ", font=("Arial Bold", 16), bg="orange")
        self.lbl_rf1.grid(row = 10, column = 2, pady = 3,padx=20)

        # Creating a Frame of state
        self.frameesp = LabelFrame(self.wind, text = "ESP32", font=("Britannic Bold", 14), bg=self.colorfondo3, fg=self.colorletras, borderwidth=2, relief="raised")
        self.frameesp.grid(row = 12, column = 0, columnspan = 3, pady = 3,padx=20, sticky=(N, S, E, W))
        
        Label(self.frameesp, text = 'State: ',font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras).grid(row = 13, column = 0, pady = 3,padx=20)
        self.lbl_light = Label(self.frameesp, text = "THE LIGHT IS OFF",font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras)
        self.lbl_light.grid(row = 13, column = 1, pady = 3,padx=20)

        Label(self.frameesp, text = 'Actual: ',font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras).grid(row = 14, column = 0, pady = 3,padx=20)
        self.lbl_act_state = Label(self.frameesp, text = "",font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras)
        self.lbl_act_state.grid(row = 14, column = 1, pady = 3,padx=20)
        self.lbl_act_date = Label(self.frameesp, text = "",font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras)
        self.lbl_act_date.grid(row = 14, column = 2, pady = 3,padx=20)

        Label(self.frameesp, text = 'Previous: ',font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras).grid(row = 15, column = 0, pady = 3,padx=20)
        
        self.lbl_prev_state = Label(self.frameesp, text = "",font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras)
        self.lbl_prev_state.grid(row = 15, column = 1, pady = 3,padx=20)
        self.lbl_prev_date = Label(self.frameesp, text = "",font=("Arial", 12), bg=self.colorfondo3, fg=self.colorletras)
        self.lbl_prev_date.grid(row = 15, column = 2, pady = 3,padx=20)

        # Quit Button
        self.btn_quit = Button(self.wind, text="Quit", command=self.quit, font=("Arial Bold", 14),bg=self.colorboton)#.grid(row = 5, column = 0)
        self.btn_quit.grid(row = 14, column = 7, pady = 3,padx=20)
        self.broker.set("broker.mqttdashboard.com")
        self.port2.set(1883)
        # Config MQTT
        #self.broker.set("broker.mqttdashboard.com")
        #self.port 1883;
        self.keepalive = 60;
        self.clientid = "Clientjazz23";
        # self.username = "jazz23";
        # self.password = "12345";
        # self.topic = "light";
        
    def paconectar(self):
        # Get information from MQTT connection 
        self.host = self.broker.get()
        self.port = self.port2.get()
        self.username = self.username2.get()
        self.password = self.password2.get()
        self.topic = self.topic2.get()

        if self.username == "" or self.password == "" or self.host == "" or self.port == "" or self.topic == "":
            messagebox.showwarning("Warning", "You must enter all the required data")
        # elif self.username == "jazz23" and self.password == "12345":
            # self.lblconnect["text"]="SOME DATA ENTERED IS NOT CORRECT \n TRY AGAIN"
        else: 
            ##### FUNCTION PRINCIPAL #####
            self.client = mqtt.Client()     # Client Identifier
            self.client.on_connect = self.on_connect      # Conecction Function 
            self.client.on_message = self.on_message      # Message Function
            self.client.connect(self.host, self.port, self.keepalive)     # Host, terminal, keep alive
            self.client.username_pw_set(self.username,self.password)    # Username and Password
            #client.loop_forever()
            self.client.loop()
            self.btn_connect.config(state = 'disable')
            self.btn_rf1.config(state = 'normal')
            self.lblconnect["text"]="Connected"
            self.broker1.config(state = 'disable')
            self.port1.config(state = 'disable')
            self.username1.config(state = 'disable')
            self.password1.config(state = 'disable')
            self.topic1.config(state = 'disable')

    def padesconectar(self):
        self.client.disconnect()
        self.btn_connect.config(state = 'normal')
        self.btn_rf1.config(state = 'disable')
        self.lblconnect["text"]="Disconnected"
        self.broker1.config(state = 'normal')
        self.port1.config(state = 'normal')
        self.username1.config(state = 'normal')
        self.password1.config(state = 'normal')
        self.topic1.config(state = 'normal')


    ####### FUNCTION ON CONNECT ######
    def on_connect(self,client, userdata, flags, rc):
        print('Connected(%s)',self.client._client_id)
        client.subscribe(self.topic, qos=0) 
        client.publish(self.topic,'Se establecio la conexion')

    ####### FUNCTION ON MESSAGE ######
    def on_message(self,client, userdata, message):
        print('----------------------')
        print('topic: %s',  message.topic)
        print('payload: %s', message.payload)
        print('qos: %d', message.qos)
        print(message.payload.decode("utf-8"))


    # Define Light Button
    def clicked(self):
        
        if self.btn_rf1["text"] == "ON":
            self.btn_rf1["text"] = "OFF"
            self.lbl_rf1["text"] = "ON" 
            self.lbl_rf1["bg"] = "green"
            self.lbl_light["text"] = "THE LIGHT IS ON"
            estado=1
            self.lbl_act_state["text"] = "ON"
            self.lbl_act_date["text"] = time.strftime("%Y/%m/%d  %H:%M:%S")
            self.lbl_prev_state["text"] = "OFF"
            self.lbl_prev_date["text"] = self.prev_time
            self.prev_time = time.strftime("%Y/%m/%d  %H:%M:%S")

        else:
            self.btn_rf1["text"] = "ON"
            self.lbl_rf1["text"] = "OFF" 
            self.lbl_rf1["bg"] = "orange"
            self.lbl_light["text"] = "THE LIGHT IS OFF"
            estado=0
            self.lbl_act_state["text"] = "OFF"
            self.lbl_act_date["text"] = time.strftime("%Y/%m/%d  %H:%M:%S")
            self.lbl_prev_state["text"] = "ON"
            self.lbl_prev_date["text"] = self.prev_time
            self.prev_time = time.strftime("%Y/%m/%d  %H:%M:%S")

        print('El estado es: ')
        print(estado)
        self.client.publish(self.topic, estado)

    def quit(self):
        sa = messagebox.askyesno("Quit", "You want to end the program?")
        if sa == True:
            quit()

# Main program
if __name__ == "__main__":                  # Especial function main
    window = Tk()                       # Define window interface
    application = App(window)             # 
    window.mainloop() 