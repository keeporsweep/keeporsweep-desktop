#!/usr/bin/env python3
# 💻🔀🗑️ Keep or Sweep, v0.1.0 for desktop
# Show a random file so you can clean your stuff
# Simply make executable and click (or run as python3 keeporsweep.py)
# http://keeporsweep.net

import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk,Image
import os
from random import shuffle
from send2trash import send2trash

root = Tk()
element_list = []
path = os.path.dirname(os.path.abspath(__file__))

# Ensure window fits screen
# Preview canvas to half screen height and margin/padding relatively
screen_height = root.winfo_screenheight()
canvas_width = int(screen_height/2)
canvas_height = int(screen_height/2)
margin = int(screen_height/40)
padding = margin
font_size = "-size 12"
font_size_weight = "-size 12 -weight bold"



class Application(tk.Frame):


  def __init__(self, master):
    self.master = master
    super().__init__(master, bg="white")
    self.pack()

    # Set up basic layout
    self.create_widgets()

    # Get the randomized file list
    self.random_files(path)

    # Load first element
    self.element_preview()
    self.element_text()

    root.bind('<Control-n>', self.keep_element())
    root.bind('<space>', self.keep_element())
    root.bind('<n>', self.someotherfunction())

  def someotherfunction(e=None):
    print('It works !')

  # Return random list of all files
  def random_files(self, path):
    global element_list
    # Get list of all files
    for root, dirs, files in os.walk(path):
      # Ignore hidden folders
      dirs[:] = [d for d in dirs if not d.startswith('.')]
      for file in files:
        element_list.append(os.path.join(root, file))
    # Return it in random order
    shuffle(element_list)


  # Initial set up of all interface elements
  def create_widgets(self):
    # Preview container
    self.canvas = Canvas(self, width=canvas_width, height=canvas_height, bg="white")
    self.canvas.pack(side="top", expand=1, padx=margin, pady=margin)

    # Element title & detail text
    self.title = Label(self, font=font_size_weight, bg="white", width="40")
    self.title.pack()
    self.details = Label(self, font=font_size, fg="#aaa", bg="white", width="40")
    self.details.pack()

    # Keep button
    self.keep = tk.Button(self, text="Keep", foreground="white", activeforeground="white", background="#0082c9", activebackground="#0072b0", command=self.keep_element, cursor="heart", bitmap="warning", compound="top", relief="flat", font=font_size_weight, default="active")
    self.keep.pack(side="right", ipadx=padding, ipady=padding, padx=margin, pady=margin)

    # Sweep button
    self.sweep = tk.Button(self, text="Sweep", foreground="white", activeforeground="white", background="#e9322d", activebackground="#e51d18", command=self.sweep_element, cursor="pirate", bitmap="error", compound="top", relief="flat", font=font_size_weight)
    self.sweep.pack(side="left", ipadx=padding, ipady=padding, padx=margin, pady=margin)


  # Display preview of current element
  def element_preview(self):
    self.canvas.delete("all")
    element_current = element_list[0]

    # Image handling
    if element_current.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
      self.image_raw = Image.open(element_list[0])
      # Make image fill canvas
      if self.image_raw.size[0] > self.image_raw.size[1]:
        # Wider than tall
        self.image_raw.thumbnail((self.image_raw.size[0], canvas_height+1), PIL.Image.BICUBIC)
      else:
        # Taller than wide
        self.image_raw.thumbnail((canvas_width+1, self.image_raw.size[1]), PIL.Image.BICUBIC)
      self.image = ImageTk.PhotoImage(self.image_raw)
      self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)


  # Display title and details of current element
  def element_text(self):
    element_current = element_list[0]
    # Splitting up the file path, removing current directory
    element_relativepath = element_current[len(path):]
    element_details, element_title = os.path.split(element_relativepath)
    # Element title
    self.title.config(text=element_title)
    # Element details
    self.details.config(text=element_details)


  # Move to next element
  def next_element(self):
    # Remove element from list
    element_list.pop(0)
    # Display next element
    self.element_preview()
    self.element_text()


  # Pressing "Keep" button
  def keep_element(self):
    # Simply go to next element
    self.next_element()


  # Pressing "Sweep" button
  def sweep_element(self):
    # Flash on deletion for extra excitement
    self.sweep.flash()
    element_current = element_list[0]
    # Delete current element
    if os.path.isfile(element_current):
      send2trash(element_current)
    # Then go to next element
    self.next_element()



app = Application(master=root)
app.master.title("Keep or Sweep")
app.master.configure(background="white")
# Center window on the screen
# https://stackoverflow.com/a/28224382
root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))


root.mainloop()


# Keyboard shortcuts (not working yet)
#frame = Frame(root, width=600, height=600)
#frame.bind("<space>", app.keep)
#frame.bind("<Right>", app.keep)
#frame.bind("k", app.keep)
#frame.bind("<BackSpace>", app.sweep)
#frame.bind("<Left>", app.sweep)
#frame.bind("s", app.sweep)
