#!/usr/bin/env python3
# 💻🔀🗑️ Keep or Sweep
# Show a random file so you can clean your stuff
# Simply make executable and click (or run as python3 keeporsweep.py)
# http://keeporsweep.net

import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk,Image
import os
from random import shuffle

element_list = []
path = os.path.dirname(os.path.realpath(__file__))
canvas_width = 500
canvas_height = 500
margin = 50
padding = 25



class Application(tk.Frame):


  def __init__(self, master=None):
    super().__init__(master, bg="white")
    self.pack()
    self.random_files(path)
    self.create_widgets()


  def random_files(self, path):
    global element_list
    for root, dirs, files in os.walk(path):
      dirs[:] = [d for d in dirs if not d.startswith('.')]
      for file in files:
        element_list.append(os.path.join(root, file))
    shuffle(element_list)
    print(element_list[0])


  def create_widgets(self):
    # Show preview
    self.canvas = Canvas(self, width=canvas_width, height=canvas_height, bg="white")
    self.canvas.pack(side="top", expand=1, padx=margin, pady=margin)
    self.image_raw = Image.open(element_list[0])

    # Fit image to canvas, https://stackoverflow.com/a/19450866
    wpercent = (canvas_width / float(self.image_raw.size[0]))
    hsize = int((float(self.image_raw.size[1]) * float(wpercent)))
    self.image_raw = self.image_raw.resize((canvas_width, hsize), PIL.Image.ANTIALIAS)
    self.image = ImageTk.PhotoImage(self.image_raw)

    self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)
    self.canvas.pack(expand=1, fill="both")

    # Splitting up the file path, removing current directory
    element_current = element_list[0][len(path):]
    element_details, element_title = element_current.rsplit('/',1)

    # Element title
    self.title = Label(self, text=element_title, font="-weight bold", bg="white")
    self.title.pack()

    # Element details
    self.details = Label(self, text=element_details, fg="grey", bg="white")
    self.details.pack()

    # Keep button
    self.keep = tk.Button(self, text="Keep", fg="white", bg="#0082c9", command=self.keep_element, cursor="heart", relief="flat", font="-weight bold")
    self.keep.pack(side="right", ipadx=padding, ipady=padding, padx=margin, pady=margin)

    # Sweep button
    self.sweep = tk.Button(self, text="Sweep", fg="white", bg="red", command=self.sweep_element, cursor="pirate", relief="flat", font="-weight bold")
    self.sweep.pack(side="left", ipadx=padding, ipady=padding, padx=margin, pady=margin)


  def element_preview(self):
    # Update preview
    self.image_raw = Image.open(element_list[0])
    wpercent = (canvas_width / float(self.image_raw.size[0]))
    hsize = int((float(self.image_raw.size[1]) * float(wpercent)))
    self.image_raw = self.image_raw.resize((canvas_width, hsize), PIL.Image.ANTIALIAS)
    self.image = ImageTk.PhotoImage(self.image_raw)
    self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)


  def element_text(self):
    # Splitting up the file path, removing current directory
    element_current = element_list[0][len(path):]
    element_details, element_title = element_current.rsplit('/',1)
    # Element title
    self.title.config(text=element_title)
    # Element details
    self.details.config(text=element_details)

  # Pressing "Keep" button
  def keep_element(self):
    print("Keep!")
    element_list.pop(0)
    self.element_preview()
    self.element_text()

  # Pressing "Sweep" button
  def sweep_element(self):
    print("Sweep!")



root = tk.Tk()
app = Application(master=root)
app.master.title("Keep or Sweep")
app.master.configure(background="white")
app.master.minsize(600, 750)

app.mainloop()
