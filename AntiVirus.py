import os
import requests
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import time

current_frame_index = 0
animation_id = None # To store the after() ID for cancellation

virus_total_api_scan_url= "https://www.virustotal.com/vtapi/v2/file/scan"
virus_total_api_key= "befd17eea2f0ed97c57094fbae211132382901b890b3deaed7f9b88fe921be85"
virus_total_get_report_url= "https://www.virustotal.com/vtapi/v2/file/report"


def scan_file(file_path):
    scan_id= upload_file(file_path)
    time.sleep(15)
    is_virus=get_report(scan_id)
    if is_virus:
        print("VIRUS IS DETECTED!!! filepath: ",file_path)
    else:
        print("{} is not virus".format(file_path))
    return is_virus

def get_report(scan_id,retries=5, delay=10):
    params = {'apikey': virus_total_api_key, 'resource': scan_id}

    for attempt in range(retries):
        response = requests.get(virus_total_get_report_url, params=params)
        
        if not response or response.status_code != 200:
            print(f"[Attempt {attempt+1}] Failed to get report. Status code: {response.status_code}")
            time.sleep(delay)
            continue
        
        result = response.json()
        
        # Optional: print result to debug
        # print("DEBUG result:", result)

        # Wait if scan is not finished yet
        if result.get("response_code") == 1:
            # Report is ready
            return result.get("positives", 0) > 0
        elif result.get("response_code") == -2:
            print("Scan still in progress. Waiting...")
            time.sleep(delay)
        else:
            print("Unexpected response from VirusTotal:", result)
            break
    
    raise Exception("Failed to get a valid report from VirusTotal after several retries.")

def upload_file(file_path):
    params = {'apikey': virus_total_api_key}
    files = {'file': (file_path, open(file_path, 'rb'))}
    response = requests.post(virus_total_api_scan_url, files=files, params=params)
    response = response.json()
    return response['scan_id']

def scan_folder_files(folder_path):
    for item in os.listdir(folder_path): #iterate list folder items
        full_item_path=os.path.join(folder_path,item)#create full item path
        if os.path.isdir(full_item_path):
            scan_folder_files(full_item_path)
        else:
            scan_file(full_item_path)


def UploadActionFile(event=None):
    file_pathg = filedialog.askopenfilename()
    if file_pathg:
        if scan_file(file_pathg):
            label = tk.Label(root, width=20, height=2,text=str("VIRUS IS DETECTED!!! filepath: "+os.path.basename(file_pathg)))
            label.place(x=550, y=450)
        else:
            label = tk.Label(root, width=20, height=2,text=str("{} is not virus".format(os.path.basename(file_pathg))))
            label.place(x=550, y=450)
    else:
        label = tk.Label(root, width=20, height=2,text="No file selected.")
        label.place(x=550, y=450)


def UploadActionFolder(event=None):
    """Opens a folder selection dialog and returns the selected path."""
    folder_pathg = filedialog.askdirectory()
    if folder_pathg:  # Check if a folder was actually selected
        if scan_folder_files(folder_pathg):
            label = tk.Label(root, width=20, height=2,text=str("VIRUS IS DETECTED!!! filepath: "+os.path.basename(folder_pathg)))
            label.place(x=550, y=450)
        else:
            label = tk.Label(root,width=20, height=2, text=str("{} is not virus".format(os.path.basename(folder_pathg))))
            label.place(x=550, y=450)
        # You can now use 'folder_path' for further operations,
        # like displaying it in a label or processing its contents.
    else:
        label = tk.Label(root,width=20, height=2, text="No folder selected.")
        label.place(x=550, y=450)




def animate_gif():
    global current_frame_index, animation_id
    image = photoimage_objects[current_frame_index]
    gif_label.configure(image=image)

    current_frame_index = (current_frame_index + 1) % len(photoimage_objects)
    
    # Adjust delay as needed (e.g., 50 milliseconds)
    animation_id = root.after(100, animate_gif) 




root=tk.Tk()
root.title("Anti virus check")
root["bg"] = "black"


gif_path = "R.gif" 
info = Image.open(gif_path)
frames = info.n_frames 
photoimage_objects = []
for i in range(frames):
    # Create a PhotoImage for each frame
    obj = ImageTk.PhotoImage(info.copy()) # Create a copy to avoid modifying original
    photoimage_objects.append(obj)
    try:
        info.seek(i + 1) # Move to the next frame
    except EOFError:
        break # Break if no more frames

gif_label = tk.Label(root, bg="black") 
gif_label.pack()

animate_gif()

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(anchor=tk.CENTER, expand=True) # Center the frame and allow it to expand


button_scan_file = tk.Button(button_frame,width=20, height=2,text='scan file', command=UploadActionFile,bg='white')
button_scan_folder = tk.Button(button_frame, width=20, height=2,text='scan folder', command=UploadActionFolder,bg='white')

button_scan_file.pack(side='left',padx=100)
button_scan_folder.pack(side='left',padx=100)

root.mainloop()