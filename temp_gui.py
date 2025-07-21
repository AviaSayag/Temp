import tkinter as tk
from tkinter import messagebox
import os
import shutil


CLIENT_FOLDER="C:/Users/User/OneDrive/מסמכים/client_folder"
SERVER_FOLDER="C:/Users/User/OneDrive/מסמכים/server_folder"

class FileTransferApp:
    def __init__(self,root):
        self.root=root
        self.root.title("מערכת העלאה והורדה של קבצים")

        self.client_listbox=tk.Listbox(root,width=40)
        self.server_listbox=tk.Listbox(root,width=40)

        self.client_listbox.grid(row=1,column=0,padx=10,pady=10)
        self.server_listbox.grid(row=1,column=2,padx=10,pady=10)

        tk.Label(root, text="קבצים בקליינט 📁").grid(row=0,column=0)
        tk.Label(root, text="קבצים בשרת 🖥️").grid(row=0,column=2)

        self.upload_button=tk.Button(root,text="העלאה לשרת ⬆️",command=self.upload_file)
        self.upload_button.grid(row=2,column=0,pady=5)
        
        self.download_button=tk.Button(root,text="הורדה לקליינט ⬇️",command=self.download_file)
        self.download_button.grid(row=2,column=2,pady=5)

        self.refresh_lists()

        self.root.mainloop()


    def refresh_lists(self):
        self.client_listbox.delete(0, tk.END)
        self.server_listbox.delete(0, tk.END)

        for file in os.listdir(CLIENT_FOLDER):
            self.client_listbox.insert(tk.END, file)

        for file in os.listdir(SERVER_FOLDER):
            self.server_listbox.insert(tk.END, file)


    def upload_file(self):
        selected = self.client_listbox.curselection()
        if not selected:
            messagebox.showwarning("שגיאה", "בחר קובץ להעלאה מהקליינט")
            return

        filename = self.client_listbox.get(selected[0])
        src = os.path.join(CLIENT_FOLDER, filename)
        dst = os.path.join(SERVER_FOLDER, filename)
        shutil.copy(src, dst)
        self.refresh_lists()



    def download_file(self):
        selected = self.server_listbox.curselection()
        if not selected:
            messagebox.showwarning("שגיאה", "בחר קובץ להורדה מהשרת")
            return

        filename = self.server_listbox.get(selected[0])
        src = os.path.join(SERVER_FOLDER, filename)
        dst = os.path.join(CLIENT_FOLDER, filename)
        shutil.copy(src, dst)
        self.refresh_lists()



if __name__=="__main__":
    print("runing")
    root=tk.Tk()
    app=FileTransferApp(root)