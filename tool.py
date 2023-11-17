import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter.ttk import Treeview
from threading import *
import target
import scanner
import platform
import subprocess
import os
def add_tab():
   tab_name = 'terminal'
   if tab_name:
      tab = ttk.Frame(topControl)
      topControl.add(tab, text=tab_name)
      # entry.delete(0, 'end')


def delete_tab():
   selected_tab = topControl.select()
   if selected_tab:
      topControl.forget(selected_tab)

win = Tk()
style = ttk.Style()
style.theme_use('classic')
menubar = Menu(win)
# Adding File Menu and commands
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New File', command=None)
file.add_command(label='Open...', command=None)
file.add_command(label='Save', command=None)
file.add_separator()
file.add_command(label='Exit', command=win.destroy)

# Adding Edit Menu and commands
edit = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='Cut', command=None)
edit.add_command(label='Copy', command=None)
edit.add_command(label='Paste', command=None)
edit.add_command(label='Select All', command=None)
edit.add_separator()
edit.add_command(label='Find...', command=None)
edit.add_command(label='Find again', command=None)

view = Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=view)
view.add_command(label='Terminal', command=add_tab)
view.add_command(label='delete', command=delete_tab)

# Adding Help Menu
help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='Tk Help', command=None)
help_.add_command(label='Demo', command=None)
help_.add_separator()
help_.add_command(label='About Tk', command=None)
# display Menu
win.config(menu = menubar)


pw = tk.PanedWindow(orient=tk.VERTICAL)
pw.pack(side=TOP, fill=tk.BOTH, expand=True)

tabControl = ttk.Notebook(pw)
tabControl.pack(expand=True, fill='both')
pw.add(tabControl)

recontab = ttk.Frame(tabControl)
tabControl.add(recontab, text='Reconnaissance')

recontabControl = ttk.Notebook(recontab)

targettab = ttk.Frame(recontabControl)
recontabControl.add(targettab, text='Target')


def add_node():
   node_text = entry.get()
   try:
      ip=target.get_ip_address(node_text)
      treeview.insert('', 'end', text=node_text, values=node_text +' '+ip)
   except:
      treeview.insert('', 'end', text=node_text, values=node_text +' FAIL')

def add_new_line():
   node_text = entry.get()
   try:
      treeviewcustom.insert('', 'end', text=node_text, values=node_text.replace(" ", "\ "))
   except:
      pass
def add_view_scanner(text):
   node_text = text
   try:
      ip=target.get_ip_address(node_text)
      tree2.insert('', 'end', text=node_text, values=node_text +' '+ip)
   except:
      tree2.insert('', 'end', text=node_text, values=node_text +' FAIL')

def add_scanner():
   item = treeview.selection()
   node_text = treeview.item(item)['values']
   try:
      tree2.insert('', 'end', text=node_text, values=node_text)
   except:
      tree2.insert('', 'end', text=node_text, values=node_text)

def dic_command():
   item = treeviewcustom.selection()
   for re in item:
      result = treeviewcustom.item(re)['values']
      print(result)
      for command in result:
         # Get the operating system name
         os_name = platform.system()

         # Check if running on Linux
         if os_name == 'Linux':
            text_area.insert(tk.END, command + "\n")
            # Use bash shell to execute the command
            subprocess.run(['bash', '-c', command])

         # Check if running on Windows
         elif os_name == 'Windows':
            text_area.insert(tk.END, command + "\n")
            # Use powershell to execute the command
            printshell = subprocess.run(
               ['powershell', '-Command', command])
            print(printshell)
         else:
            print(f"Unsupported operating system: {os_name}")



def show_popup():
   messagebox.showinfo("Popup", "plese check your subdomain file")

def add_node_scanner():
   item = treeview.selection()
   lists = tree3.selection()
   file_path = tree3.item(lists)['text']

   def read_file(file_path):
      try:
         with open(file_path, 'r') as file:
            content = file.read()
            dom = content.splitlines()
            return dom
      except FileNotFoundError:
         print(f"File not found: {file_path}")
         return None
      except IOError as e:
         print(f"Error reading the file: {e}")
         return None

   file_content = read_file(file_path)
   node_text = treeview.item(item)['values']
   try:
     results = scanner.domain_scanner(node_text[0], file_content)
     for result in results:
        text_area.insert(tk.END, result + "\n")
        add_view_scanner(result)
   except:
      show_popup()
def add_dir_scanner():
   item = tree2.selection()
   lists = tree3.selection()
   file_path = tree3.item(lists)['text']

   def read_file(file_path):
      try:
         with open(file_path, 'r') as file:
            content = file.read()
            dom = content.splitlines()
            return dom
      except FileNotFoundError:
         print(f"File not found: {file_path}")
         return None
      except IOError as e:
         print(f"Error reading the file: {e}")
         return None

   file_content = read_file(file_path)
   node_text = tree2.item(item)['values']
   try:
     results = scanner.dir_scanner(node_text[0], file_content)
     for result in results:
        text_area.insert(tk.END, result + "\n")
   except:
      show_popup()
def delete_node():
   selected_item = treeview.selection()
   for item in selected_item:
      print(item)
      treeview.delete(item)
def delete_scan():
   selected_item = treeview.selection()
   for item in selected_item:
      print(item)
      tree2.delete(item)
def delete_dir():
   selected_item = treeview.selection()
   for item in selected_item:
      print(item)
      tree3.delete(item)
def update_node():
   selected_item = treeview.selection()
   for item in selected_item:
      print(item)
      new_text = entry.get()
      treeview.item(item, text=new_text, values=new_text)

def delete_line():
   selected_item = treeviewcustom.selection()
   for item in selected_item:
      print(item)
      treeviewcustom.delete(item)
def update_line():
   selected_item = treeviewcustom.selection()
   for item in selected_item:
      print(item)
      new_text = entry.get()
      treeviewcustom.item(item, text=new_text, values=new_text)

def UploadAction():
   file_path = filedialog.askopenfilename()

   def read_file(file_path):
      try:
         with open(file_path, 'r') as file:
            content = file.read()
            dom = content.splitlines()
            return dom
      except FileNotFoundError:
         print(f"File not found: {file_path}")
         return None
      except IOError as e:
         print(f"Error reading the file: {e}")
         return None
   file_content = read_file(file_path)
   if file_content:
      for node_text in file_content:
         try:
            ip=target.get_ip_address(node_text)
            treeview.insert('', 'end', text=node_text, values=node_text +' '+ip)
         except:
            treeview.insert('', 'end', text=node_text, values=node_text +' FAIL')

def UploadAction2():
   file_path = filedialog.askopenfilename()

   def read_file(file_path):
      try:
         with open(file_path, 'r') as file:
            content = file.read()
            dom = content.splitlines()
            return dom
      except FileNotFoundError:
         print(f"File not found: {file_path}")
         return None
      except IOError as e:
         print(f"Error reading the file: {e}")
         return None
   file_content = read_file(file_path)
   if file_content:
      for node_text in file_content:
         try:
            treeviewcustom.insert('', 'end', text=node_text, values=node_text.replace(" ", "\ "))
         except:
            treeviewcustom.insert('', 'end', text=node_text, values=node_text.replace(" ", "\ "))
def LinkAction():
   file_path = filedialog.askopenfilename()

   def read_file(file_path):
      try:
         with open(file_path, 'r') as file:
            content = file.read()
            dom = content.splitlines()
            return dom
      except FileNotFoundError:
         print(f"File not found: {file_path}")
         return None
      except IOError as e:
         print(f"Error reading the file: {e}")
         return None
   file_content = read_file(file_path)
   if file_content:
      # for node_text in file_content:
      try:
         treeviewcustom.insert('', 'end', text=file_path, values=file_path)
      except:
         treeviewcustom.insert('', 'end', text=file_path, values='Fail File Path')

# def add_new_line_threading():
#    # Call work function
#    t1 = Thread(target=add_new_line)
#    t1.start()
def scanner_threading():
   # Call work function
   t1 = Thread(target=add_node_scanner)
   t1.start()

def UploadAction_threading():
   # Call work function
   t1 = Thread(target=UploadAction)
   t1.start()

def UploadAction_threading2():
   # Call work function
   t1 = Thread(target=UploadAction2)
   t1.start()
def dic_scanner_threading():
   # Call work function
   t1 = Thread(target=add_dir_scanner)
   t1.start()

def dic_threading():
   # Call work function
   t1 = Thread(target=dic_command)
   t1.start()
# Create a Treeview widget
treeview = ttk.Treeview(targettab, column=("c1", "c2"), show='headings', height=8)

treeview.column("#1", anchor=CENTER, stretch=NO, width=600)
treeview.heading("#1", text="Domain")
treeview.column("#2", anchor=CENTER)
treeview.heading("#2", text="IP Address")
treeview.grid(row=1, column=0,sticky="nsew" , columnspan=4, padx=5, pady=5)
targettab.columnconfigure(0, weight=1)
targettab.rowconfigure(1, weight=1)

m1 = Menu(treeview, tearoff=0)
m1.add_command(label="Add Scan List", command=add_scanner)
m1.add_command(label="Delete", command=delete_node)

def do_popup(event):
   try:
      m1.tk_popup(event.x_root, event.y_root)
   finally:
      m1.grab_release()


treeview.bind("<Button-3>", do_popup)

# Create a TextField widget
l1 = Label(targettab, text = "Domain:")
l1.grid(row = 0, column = 0, sticky = W, pady = 2)
entry = ttk.Entry(targettab)
entry.grid(row=0, column=0, sticky = W, padx = 50)

# Create buttons for treeview operations
add_button = ttk.Button(targettab, text='Add', command=add_node)
add_button.grid(row=0, column=0, sticky = W, padx = 160)

delete_button = ttk.Button(targettab, text='Delete', command=delete_node)
delete_button.grid(row=0, column=0, sticky = W, padx = 220)

update_button = ttk.Button(targettab, text='Update', command=update_node)
update_button.grid(row=0, column=0, sticky = W, padx = 290)

update_button = ttk.Button(targettab, text='File', command=UploadAction_threading)
update_button.grid(row=0, column=0, sticky = W, padx = 365)

select_button = ttk.Button(targettab, text='target>>', command=add_scanner)
select_button.grid(row=0, column=0, padx=400)


dicscantab = ttk.Frame(recontabControl)
recontabControl.add(dicscantab, text='Scanner')
recontabControl.pack(fill='both', expand=True)
# Create a Treeview widget
tree2 = Treeview = ttk.Treeview(dicscantab, column=("c1", "c2", "c3"), show='headings', height=8)
tree2.column("#1", anchor=CENTER, stretch=NO)
tree2.heading("#1", text="Domain")
tree2.column("#2", anchor=CENTER)
tree2.heading("#2", text="IP Address")
tree2.column("#3", anchor=CENTER)
tree2.heading("#3", text="Status")
tree2.grid(row=0, column=0, sticky="nsew" , columnspan=1, padx=5, pady=5)

# Create a Treeview widget
tree3 = Treeview = ttk.Treeview(dicscantab, column=("c1"), show='headings', height=8)
tree3.column("#1", anchor=CENTER, stretch=NO, width=350)
tree3.heading("#1", text="Directory")
tree3.grid(row=0, column=1, sticky="nsew" , columnspan=4, padx=5, pady=5)
dicscantab.columnconfigure(1, weight=1)
dicscantab.rowconfigure(0, weight=1)


m2 = Menu(tree2, tearoff=0)
m2.add_command(label="Subdomain Scan", command=scanner_threading)
m2.add_command(label="Subdirectory Scan", command=dic_scanner_threading)
m2.add_command(label="delete", command=delete_scan)

def do_popup(event):
   try:
      m2.tk_popup(event.x_root, event.y_root)
   finally:
      m2.grab_release()


tree2.bind("<Button-3>", do_popup)

m3 = Menu(tree3, tearoff=0)
m3.add_command(label="Upload", command=LinkAction)
m3.add_command(label="delete", command=delete_dir)

def do_popup(event):
   try:
      m3.tk_popup(event.x_root, event.y_root)
   finally:
      m3.grab_release()


tree3.bind("<Button-3>", do_popup)

customscantab = ttk.Frame(recontabControl)
recontabControl.add(customscantab, text='Custom')
recontabControl.pack(fill='both', expand=True)

# Create a Treeview widget
treeviewcustom = ttk.Treeview(customscantab, column=("c1"), show='headings', height=8)

treeviewcustom.column("#1", anchor=CENTER)
treeviewcustom.heading("#1", text="command")
treeviewcustom.grid(row=1, column=0,sticky="nsew" , columnspan=4, padx=5, pady=5)
customscantab.columnconfigure(0, weight=1)
customscantab.rowconfigure(1, weight=1)

# Create a TextField widget
l1 = Label(customscantab, text = "Shell:")
l1.grid(row = 0, column = 0, sticky = W, pady = 2)
entry = ttk.Entry(customscantab, width=130)
entry.grid(row=0, column=0, sticky = W, padx = 50)

# Create buttons for treeview operations
add_button = ttk.Button(customscantab, text='Add', command=add_new_line)
add_button.grid(row=0, column=0, sticky = E)

# delete_button = ttk.Button(customscantab, text='Delete', command=delete_line)
# delete_button.grid(row=0, column=0, sticky = E, padx = 320)
#
# update_button = ttk.Button(customscantab, text='Update', command=update_line)
# update_button.grid(row=0, column=0, sticky = E, padx = 390)

# upload_button = ttk.Button(customscantab, text='File', command=UploadAction_threading)
# upload_button.grid(row=0, column=0, sticky = E, padx = 465)

# # select_button = ttk.Button(customscantab, text='run>>', command=dic_threading)
# select_button.grid(row=0, column=0, sticky = E)

mc = Menu(treeviewcustom, tearoff=0)
mc.add_command(label="Add", command=add_new_line)
mc.add_command(label="Delete", command=delete_line)
mc.add_command(label="Update", command=update_line)
mc.add_command(label="File", command=UploadAction_threading2)
mc.add_command(label="run>>", command=dic_threading)


def do_popup(event):
   try:
      mc.tk_popup(event.x_root, event.y_root)
   finally:
      mc.grab_release()


treeviewcustom.bind("<Button-3>", do_popup)

tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
tab7 = ttk.Frame(tabControl)
Weapontab = tabControl.add(tab2, text='Weaponization')
Exploittab = tabControl.add(tab3, text='Exploitation')
privatetab = tabControl.add(tab4, text='Privilege escalation')
Lateraltab = tabControl.add(tab5, text='Lateral movement')
C2tab = tabControl.add(tab6, text='Command and control')
Exfiltab = tabControl.add(tab7, text='Exfiltrate')
# tabControl.pack(side = TOP)

# Button widget
top = ttk.Frame(pw)
top.pack(side=BOTTOM, expand = 1, fill =BOTH)

# This will add button widget to the panedwindow
pw.add(top)
topControl = ttk.Notebook(top)

m = Menu(topControl, tearoff=0)
m.add_command(label="New terminal", command=add_tab)
m.add_command(label="Delete", command=delete_tab)

def do_popup(event):
   try:
      m.tk_popup(event.x_root, event.y_root)
   finally:
      m.grab_release()


topControl.bind("<Button-3>", do_popup)

terminal = ttk.Frame(topControl)
topControl.add(terminal, text='terminal')
topControl.pack(expand=1, fill="both")
text_area = tk.Text(terminal)
text_area.place(width= 800, height= 280)
text_area.grid(row=1, column=0, padx=5, pady=5)
# text_area.columnconfigure(0, weight=1)
# text_area.rowconfigure(1, weight=1)
text_area.pack(expand=True, fill=BOTH)

pw.add(tabControl)

win.geometry("1000x600")
win.title("pentest")
win.mainloop()
# aovresearcher0@gmail.com
