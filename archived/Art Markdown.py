#Delete "Previous Art Markdown.txt" to clear the data upon opening the program

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import datetime
time_raw = datetime.datetime.now()
time = time_raw.strftime("%B")+" "+str(int(time_raw.strftime("%d")))+", "+time_raw.strftime("%Y")

window=Tk()
window.title("Art Markdown")
window["bg"] = "white"

variables_dict = {"title":"", "structure_title":"", "blurb_text":"",
                  "specification":"","image_paths":""}

def update_variables_dict():
    global variables_dict
    variables_dict["title"] = title.get()
    variables_dict["structure_title"] = structure_title.get().strip()
    variables_dict["specification"] = specification.get().strip()
    
    variables_dict["image_paths"] = [image_path.get().strip() for image_path in image_paths]

    variables_dict["blurb_text"] = blurb_text.get("1.0","end-1c").strip()
    
    if specification.get().strip() == "":
        variables_dict["specification"] = "Art"

def select_image(string_var):
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Image",
                                           filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"),
                                                      ("png files", "*.png"), ("svg files", "*.svg")))
    string_var.set(file_path)

def process_router():
    istesting = bool(testing.get())
    if istesting:
        print("testing mode")
    else:
        process()
def process():
    update_variables_dict()

    #Make Folder
    folder_path = os.path.abspath(os.getcwd())
    full_folder_path = folder_path+"/Art/"+variables_dict["structure_title"]
    if not os.path.exists(full_folder_path):
        os.mkdir(full_folder_path)
    #Make Folder

    #Moving Photos
    for img in range(len(image_paths)):
        image_path_tuple = os.path.splitext(image_paths[img].get())
        if img == 0:
            variables_dict["image_path_extension"] = [image_path_tuple[1]]
        else:
            variables_dict["image_path_extension"].append(image_path_tuple[1])
        try:
            if img == 0:
                os.replace("".join(image_path_tuple), folder_path+"/Photos/Art/"+variables_dict["structure_title"]+image_path_tuple[1])
            else:
                os.replace("".join(image_path_tuple), folder_path+"/Photos/Art/"+variables_dict["structure_title"]+" "+str(img)+image_path_tuple[1])
        except: pass
        
    #Moving Photos

    variables_dict_keys = list(variables_dict.keys())
    variables_dict_keys.sort(reverse = True, key = (lambda dict_key: len(dict_key)))

    #Linked Piece
    linked_piece_template = open(folder_path+"/Art/Template/Linked Piece Template.html","r")
    linked_piece_text = linked_piece_template.read()
    linked_piece_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            linked_piece_text = linked_piece_text.replace("_title_", str(variables_dict[variable_name]))
        elif variable_name == "image_path_extension":
            linked_piece_text = linked_piece_text.replace(variable_name, str(variables_dict[variable_name][0]))
        else:
            linked_piece_text = linked_piece_text.replace(variable_name, str(variables_dict[variable_name]))
    linked_piece = open(full_folder_path+"/Linked Piece.html","w")
    linked_piece.write(linked_piece_text)
    linked_piece.close()
    #Linked Piece

    #Art
    art_template = open(folder_path+"/Art/Template/Art Template.html","r")
    art_html = art_template.read()
    art_template.close()
    art_html = art_html.replace("time",time)
    for variable_name in variables_dict_keys:
        if variable_name == "blurb_text":
            formated_blurb_text = ""
            for paragraph in variables_dict[variable_name].splitlines():
                if paragraph:
                    formated_blurb_text += ('<p class="general">'+paragraph+"</p>")
            art_html = art_html.replace('<p class="general"></p>',formated_blurb_text)
        elif variable_name == "title":
            art_html = art_html.replace("_title_", str(variables_dict[variable_name]))
        else:
            art_html = art_html.replace(variable_name, str(variables_dict[variable_name]))
    art = open(full_folder_path+".html","w")
    art.write(art_html)
    art.close()
    #Art

    #Art Loader
    feature_loader = open(folder_path+"/Loader.js")
    lines = feature_loader.readlines()
    lines[0] = lines[0][:16] + '["'+variables_dict["structure_title"]+'","ar"],' + lines[0][16:]
    feature_loader.close()
    feature_loader = open(folder_path+"/Loader.js","w")
    feature_loader.writelines(lines)
    feature_loader.close()
    #Art Loader

    #Sitemap
    sitemap = open("sitemap.txt","a")
    sitemap.write("\nhttps://leo-zeuli.github.io/Art/"+variables_dict["structure_title"]+".html")
    sitemap.close()
    #Sitemap

def load_markdown():
    global variables_dict
    previous_markdown = open("Previous Art Markdown.txt","r")
    variables_dict = eval(previous_markdown.read().strip())
    
    title.set(variables_dict["title"])
    structure_title.set(variables_dict["structure_title"])
    specification.set(variables_dict["specification"])
    
    for row in range(len(variables_dict["image_paths"])):
        if row != 0:
            add_image()
        image_paths[row].set(variables_dict["image_paths"][row])

    blurb_text.delete("1.0","end-1c")
    blurb_text.insert("end-1c", variables_dict["blurb_text"])

def save_markdown():
    update_variables_dict()
    previous_markdown = open("Previous Art Markdown.txt","w")
    previous_markdown.truncate(0)
    previous_markdown.write(str(variables_dict))
    previous_markdown.close()

testing_frame = Frame(window)
testing_frame.pack(pady=(5,2), anchor="center")
Label(testing_frame, text="→", bg="white", fg="red").pack(side="left")
Label(testing_frame, text="→", bg="white", fg="orange").pack(side="left")
Label(testing_frame, text="→", bg="white", fg="yellow").pack(side="left")
Label(testing_frame, text="→", bg="white", fg="lawn green").pack(side="left")
Label(testing_frame, text="→", bg="white", fg="cyan").pack(side="left")
Label(testing_frame, text="→", bg="white", fg="blue").pack(side="left")
Label(testing_frame, text="→", bg="white", fg="purple").pack(side="left")
testing = IntVar()
#testing.set(0) #Not Testing Defult
testing.set(1) #Testing Defult
Checkbutton(testing_frame, text="Testing?", variable=testing, onvalue=1, offvalue=0).pack(side="left")
Label(testing_frame, text="←", bg="white", fg="purple").pack(side="left")
Label(testing_frame, text="←", bg="white", fg="blue").pack(side="left")
Label(testing_frame, text="←", bg="white", fg="cyan").pack(side="left")
Label(testing_frame, text="←", bg="white", fg="lawn green").pack(side="left")
Label(testing_frame, text="←", bg="white", fg="yellow").pack(side="left")
Label(testing_frame, text="←", bg="white", fg="orange").pack(side="left")
Label(testing_frame, text="←", bg="white", fg="red").pack(side="left")

title_frame = Frame(window)
title_frame.pack(padx=(10, 10), pady=(0,2), anchor="w")
Label(title_frame, text="Title : ", bg="white", justify="left").grid(row=0,column=0)
title = StringVar()
Entry(title_frame, textvariable=title, bg="white", width="40", highlightbackground="red").grid(row=0,column=1)
Label(title_frame, text="Structure Title : ", bg="white", justify="left").grid(row=1,column=0)
structure_title = StringVar()
Entry(title_frame, textvariable=structure_title, bg="white", width="40", highlightbackground="orange").grid(row=1,column=1)

specification_frame = Frame(window)
specification_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
Label(specification_frame, text="Specification : ", bg="white").pack(side="left")
specification = StringVar()
Entry(specification_frame, textvariable=specification, bg="white", highlightbackground="yellow", width="18").pack(side="left")

row = 0
image_paths = []
def add_image():
    global row
    row += 1
    Label(image_frame, text="Piece Image", bg="white").grid(row=(row+1),column=0)
    image_paths.append(StringVar())
    Entry(image_frame, textvariable=image_paths[row], bg="white", width="35", highlightbackground="lawn green").grid(row=(row+1),column=1)
    Button(image_frame, text ="Directory Select", command = lambda : select_image(image_paths[row])).grid(row=(row+1),column=2,padx=(3,0))
image_frame = Frame(window)
image_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(image_frame, text="File Path /", bg="white").grid(row=0,column=1)
Button(image_frame, text ="Add Image", command = add_image).grid(row=0,column=2)
Label(image_frame, text="Piece Image", bg="white").grid(row=(row+1),column=0)
image_paths.append(StringVar())
Entry(image_frame, textvariable=image_paths[row], bg="white", width="35", highlightbackground="lawn green").grid(row=(row+1),column=1)
Button(image_frame, text ="Directory Select", command = lambda : select_image(image_paths[0])).grid(row=(1),column=2,padx=(3,0))

blurb_frame = Frame(window)
blurb_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(blurb_frame, text="Art Blurb", bg="white").grid(row=0,column=0)
blurb_text = Text(blurb_frame, bg="white", highlightbackground="cyan", height="10")
blurb_text.grid(row=1,column=0)

markdown_processes_frame = Frame(window)
markdown_processes_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
Label(markdown_processes_frame, text="→", bg="white", fg="red").pack(side="left")
Label(markdown_processes_frame, text="→", bg="white", fg="orange").pack(side="left")
Label(markdown_processes_frame, text="→", bg="white", fg="yellow").pack(side="left")
Label(markdown_processes_frame, text="→", bg="white", fg="lawn green").pack(side="left")
Label(markdown_processes_frame, text="→", bg="white", fg="cyan").pack(side="left")
Label(markdown_processes_frame, text="→", bg="white", fg="blue").pack(side="left")
Label(markdown_processes_frame, text="→", bg="white", fg="purple").pack(side="left")
Button(markdown_processes_frame, text ="Save Markdown", command=save_markdown).pack(side="left")
Button(markdown_processes_frame, text ="Load Markdown", command=load_markdown).pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="purple").pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="blue").pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="cyan").pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="lawn green").pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="yellow").pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="orange").pack(side="left")
Label(markdown_processes_frame, text="←", bg="white", fg="red").pack(side="left")

process_frame = Frame(window)
process_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
Label(process_frame, text="→", bg="white", fg="red").pack(side="left")
Label(process_frame, text="→", bg="white", fg="orange").pack(side="left")
Label(process_frame, text="→", bg="white", fg="yellow").pack(side="left")
Label(process_frame, text="→", bg="white", fg="lawn green").pack(side="left")
Label(process_frame, text="→", bg="white", fg="cyan").pack(side="left")
Label(process_frame, text="→", bg="white", fg="blue").pack(side="left")
Label(process_frame, text="→", bg="white", fg="purple").pack(side="left")
Button(process_frame, text ="Process", command=process_router).pack(side="left")
Label(process_frame, text="←", bg="white", fg="purple").pack(side="left")
Label(process_frame, text="←", bg="white", fg="blue").pack(side="left")
Label(process_frame, text="←", bg="white", fg="cyan").pack(side="left")
Label(process_frame, text="←", bg="white", fg="lawn green").pack(side="left")
Label(process_frame, text="←", bg="white", fg="yellow").pack(side="left")
Label(process_frame, text="←", bg="white", fg="orange").pack(side="left")
Label(process_frame, text="←", bg="white", fg="red").pack(side="left")
