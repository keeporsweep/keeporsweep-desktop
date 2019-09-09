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
import subprocess
import cv2
import mimetypes
from PIL import Image, ImageDraw
try:
  import sys
except:
  pass
import logging
logging.basicConfig(level=logging.WARNING)

root = tk.Tk()
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


  def __init__(self, master=None):
    super().__init__(master, bg="white")
    self.pack()

    # Set up basic layout
    self.create_widgets()

    # Get the randomized file list
    self.random_files(path)

    # Load first element
    self.element_preview()
    self.element_text()




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

    self.counter = tk.Label(self, text='0', foreground="white", activeforeground="white", background="#32a846", activebackground="#e51d18", compound="top", relief="flat", font=font_size_weight)
    self.counter.pack(side="bottom", ipadx=padding//2, ipady=padding//2, padx=margin//2, pady=(margin//8,margin))

    self.counter_label = tk.Label(self, text='Sweep Counter', foreground="white", activeforeground="white", background="#32a846", activebackground="#e51d18", compound="top", relief="flat", font=font_size_weight)
    self.counter_label.pack(side="bottom", ipadx=padding//2, ipady=padding//2, padx=margin//2, pady=0)

  # Display preview of current element
  def element_preview(self):
    self.canvas.delete("all")

    if len(element_list)>0:
      logging.warning(element_list)
      logging.warning(len(element_list))
      element_current = element_list[0]

      # Image handling
      # if element_current.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):

      if element_current.lower().endswith(('.mp4','.avi','.mkv')):
        self.image_raw = self.create_thumb(element_current)
      elif 'text/plain' == mimetypes.guess_type(element_current)[0]:
        logging.warning(element_current)
        self.image_raw = self.create_thumb_from_text(element_current)
        self.image = ImageTk.PhotoImage(self.image_raw)
        self.canvas.bind("<Button-1>",self.show_file)
        self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)
      else:
        try:
          self.image_raw = Image.open(element_list[0])
          # Make image fill canvas
          if self.image_raw.size[0] > self.image_raw.size[1]:
            # Wider than tall
            self.image_raw.thumbnail((self.image_raw.size[0], canvas_height+1), PIL.Image.BICUBIC)
          else:
            # Taller than wide
            self.image_raw.thumbnail((canvas_width+1, self.image_raw.size[1]), PIL.Image.BICUBIC)

          self.image = ImageTk.PhotoImage(self.image_raw)
          self.canvas.bind("<Button-1>",self.show_file)
          self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)
        except:
          return
    else:
      self.image_raw = Image.open('images/clean.png')
      self.image = ImageTk.PhotoImage(self.image_raw)
      self.canvas.create_image(canvas_width/2, canvas_height/2, anchor="center", image=self.image)

  # Display title and details of current element
  def element_text(self, empty=False):

    if not empty:
      element_current = element_list[0]
      # Splitting up the file path, removing current directory
      element_relativepath = element_current[len(path):]
      element_details, element_title = os.path.split(element_relativepath)
      # Element title
      self.title.config(text=element_title)
      self.title.bind("<Button-1>",self.show_file)
      # Element details
      self.details.config(text=element_details)
      self.details.bind("<Button-1>", self.show_folder)
    else:
      self.title.config(text='')
      self.details.config(text='')

  #Open folder on clicking path
  def show_folder(self, null_arg):

    pathToFolder = os.path.dirname(os.path.abspath(element_list[0]))
    self.open_file(os.path.realpath(pathToFolder))

  # Open file on click file path
  def show_file(self, null_arg):

    pathToFolder = os.path.abspath(element_list[0])
    self.open_file(pathToFolder)

  #Open the file according to the OS platform
  def open_file(self, filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])



  # Move to next element
  def next_element(self):
    self.delete_thumbs()
    # Remove element from list
    if len(element_list)>1:
      element_list.pop(0)
      # Display next element
      self.element_preview()
      self.element_text()
    elif len(element_list)==1:
      element_list.pop(0)
      self.element_preview()
      self.element_text(empty=True)
      os.rmdir('.thumbnails')
    

  # Pressing "Keep" button
  def keep_element(self):
    # Simply go to next element
    self.next_element()


  # Pressing "Sweep" button
  def sweep_element(self):
    # Flash on deletion for extra excitement
    self.sweep.flash()
    if element_list:
      element_current = element_list[0]
      # Delete current element
      if os.path.isfile(element_current):
        send2trash(element_current)
      # Update the sweep counter
      self.counter['text']=str(int(self.counter['text'])+1)
      # Then go to next element
      self.next_element()



  # Creating thumbnail for video
  def create_thumb(self, filename):
    vcap = cv2.VideoCapture(filename)
    res, im_ar = vcap.read()
    while im_ar.mean() < 50 and res:
          res, im_ar = vcap.read()
    im_ar = cv2.resize(im_ar, (500, 500), 0, 0, cv2.INTER_LINEAR)

    cv2.imwrite(os.path.join('.thumbnails',f'{filename[:-4]}.jpg'), im_ar)
    logging.warning('.thumbnails',f'{filename[:-4]}.jpg')
    return os.path.join('.thumbnails',f'{filename[:-4]}.jpg')


  def create_thumb_from_text(self, file):
    # Read first few lines from the file
    text=''
    with open(file, encoding='utf8') as fp:
      for index, line in enumerate(fp):
        if index<20:
          text+=line
    logging.warning(text)

    # Create new image
    img = Image.new('RGB', (canvas_height, canvas_width),color='white')
    d=ImageDraw.Draw(img)
    # Write text on the image
    text = text.encode('ascii','ignore')
    d.text((10,10),text,0)
    filename = os.path.basename(file).split('.')[0]
    thumb_path = os.path.join('.thumbnails',f'{filename}.png')
    logging.warning(thumb_path)
    img.save(thumb_path)
    return Image.open(thumb_path)

  def delete_thumbs(self):
    for file in os.listdir('.thumbnails'):
      try:
        os.remove(os.path.join('.thumbnails', file))
      except Exception as e:
        logging.warning(f'Not deleted {e}' )

def create_thumb_folder():
  if '.thumbnails' in os.listdir():
    return
  try:
    os.mkdir('.thumbnails')
  except:
    logging.warning('Could not create folder')


create_thumb_folder()
app = Application(master=root)
app.master.title("Keep or Sweep")
app.master.configure(background="white")
# Center window on the screen
# https://stackoverflow.com/a/28224382
if sys.platform != "win32":
  root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
root.iconbitmap('images/icon.ico')
app.mainloop()
