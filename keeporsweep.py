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

root = tk.Tk()
element_list = []
path = os.getcwd()

# Ensure window fits screen
# Preview canvas to half screen height and margin/padding relatively
screen_height = root.winfo_screenheight()
canvas_width = int(screen_height/2)
canvas_height = int(screen_height/2)
margin = int(screen_height/20)
padding = int(margin/2)



class Application(tk.Frame):


  def __init__(self, master=None):
    super().__init__(master, bg="white")
    self.pack()
    self.random_files(path)
    self.create_widgets()


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


  # Create all interface elements
  def create_widgets(self):
    # Preview container
    self.canvas = Canvas(self, width=canvas_width, height=canvas_height, bg="white")
    self.canvas.pack(side="top", expand=1, padx=margin, pady=margin)

    element_current = element_list[0]

    # Handle previews for images
    if element_current.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
      self.image_raw = Image.open(element_list[0])
      # Fit image to canvas, https://stackoverflow.com/a/19450866
      wpercent = (canvas_width / float(self.image_raw.size[0]))
      hsize = int((float(self.image_raw.size[1]) * float(wpercent)))
      self.image_raw = self.image_raw.resize((canvas_width, hsize), PIL.Image.BICUBIC)
      self.image = ImageTk.PhotoImage(self.image_raw)
      self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)

    # Split up the file path, remove current directory
    element_relativepath = element_current[len(path):]
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


  # Display preview of current element
  def element_preview(self):
    self.canvas.delete("all")
    element_current = element_list[0]
    # Image handling
    if element_current.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
      # Update preview
      self.image_raw = Image.open(element_list[0])
      wpercent = (canvas_width / float(self.image_raw.size[0]))
      hsize = int((float(self.image_raw.size[1]) * float(wpercent)))
      self.image_raw = self.image_raw.resize((canvas_width, hsize), PIL.Image.BICUBIC)
      self.image = ImageTk.PhotoImage(self.image_raw)
      self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)


  # Display title and details of current element
  def element_text(self):
    element_current = element_list[0]
    # Splitting up the file path, removing current directory
    element_relativepath = element_current[len(path):]
    element_details, element_title = element_current.rsplit('/',1)
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
    # Delete current element
    print("Sweep!")
    # Then go to next element
    self.next_element()



app = Application(master=root)
app.master.title("Keep or Sweep")
app.master.configure(background="white")

app.mainloop()
