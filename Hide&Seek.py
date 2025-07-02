import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class PrivacyProtectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hide&Seek")
        
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        
        self.cap = cv2.VideoCapture(0)
        self.width, self.height = 640, 480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        
        self.create_widgets()
        
        
        self.update()
        
    def create_widgets(self):
        
        self.video_frame = ttk.Label(self.root)
        self.video_frame.pack(pady=10)
        
        
        self.warning_label = ttk.Label(
            self.root,
            text="Status: Ready",
            font=('Helvetica', 12),
            foreground='black'
        )
        self.warning_label.pack(pady=5)
        
        
        self.toggle_btn = ttk.Button(
            self.root,
            text="Enable Protection",
            command=self.toggle_protection
        )
        self.toggle_btn.pack(pady=5)
        
        
        exit_btn = ttk.Button(
            self.root,
            text="Exit",
            command=self.on_close
        )
        exit_btn.pack(pady=5)
        
        
        self.protection_enabled = False
        
    def toggle_protection(self):
        self.protection_enabled = not self.protection_enabled
        btn_text = "Disable Protection" if self.protection_enabled else "Enable Protection"
        self.toggle_btn.config(text=btn_text)
        
    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces
        
    def apply_mask(self, frame, faces):
        masked_frame = frame.copy()
        warning_active = False
        
        for (x, y, w, h) in faces:
            
            center = (x + w//2, y + h//2)
            radius = max(w, h) // 2
            cv2.circle(masked_frame, center, radius, (0, 0, 255), -1)
            
            
            if radius * 2 < min(w, h):
                warning_active = True
                cv2.putText(
                    masked_frame, 
                    "PRIVACY WARNING!", 
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (0, 0, 255), 
                    2
                )
                
        return masked_frame, warning_active
        
    def update(self):
        ret, frame = self.cap.read()
        
        if ret:
            if self.protection_enabled:
                faces = self.detect_faces(frame)
                processed_frame, warning = self.apply_mask(frame, faces)
                
                if warning:
                    self.warning_label.config(
                        text="WARNING: Face detected!", 
                        foreground='red'
                    )
                else:
                    self.warning_label.config(
                        text="Status: Protection Active", 
                        foreground='green'
                    )
            else:
                processed_frame = frame
                self.warning_label.config(
                    text="Status: Protection Disabled", 
                    foreground='black'
                )
                
            
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(processed_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.video_frame.imgtk = imgtk
            self.video_frame.config(image=imgtk)
            
        self.root.after(10, self.update)
        
    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.cap.release()
            self.root.destroy()
            
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = PrivacyProtectorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
