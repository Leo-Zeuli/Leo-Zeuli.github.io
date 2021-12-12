#Delete "Previous Collection Markdown.txt" to clear the data upon opening the program

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import datetime
time_raw = datetime.datetime.now()
time = time_raw.strftime("%B")+" "+str(int(time_raw.strftime("%d")))+", "+time_raw.strftime("%Y")

window=Tk()
window.title("Collection Markdown")
window["bg"] = "white"

variables_dict = {"title":"", "structure_title":"", "compact_image_path":"",
                  "wide_image_path":"", "specification":"", "art_pieces_true_false":"",
                  "wide_synopsis_text":""}

def update_variables_dict():
    global variables_dict
    variables_dict["title"] = title.get()
    variables_dict["structure_title"] = structure_title.get().strip()
    variables_dict["specification"] = specification.get().strip()

    art_pieces_true_false_bool = []
    for piece in range(len(art_pieces_true_false)):
        art_pieces_true_false_bool.append(art_pieces_true_false[piece].get())
    variables_dict["art_pieces_true_false"] = art_pieces_true_false_bool

    variables_dict["wide_image_path"] = wide_image_path.get().strip()

    variables_dict["wide_synopsis_text"] = wide_synopsis_text.get("1.0","end-1c").strip()
    
    if specification.get().strip() == "":
        variables_dict["specification"] = "Collection"

def select_compact_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Compact Image",
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    compact_image_path.set(file_path)
def select_wide_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Wide Image",  
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    wide_image_path.set(file_path)

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
    compact_image_path_tuple = os.path.splitext(compact_image_path.get())
    variables_dict["compact_image_path_extension"] = compact_image_path_tuple[1]
    wide_image_path_tuple = os.path.splitext(wide_image_path.get())
    variables_dict["wide_image_path_extension"] = wide_image_path_tuple[1]

    if not os.path.exists(folder_path+"/Photos/Art/"+variables_dict["structure_title"]):
        os.mkdir(folder_path+"/Photos/Art/"+variables_dict["structure_title"])
        
    try:
        os.replace("".join(compact_image_path_tuple), folder_path+"/Photos/Art/"+variables_dict["structure_title"]+"/"+variables_dict["structure_title"]+compact_image_path_tuple[1])
    except: pass
    try:
        os.replace("".join(wide_image_path_tuple), folder_path+"/Photos/Art/"+variables_dict["structure_title"]+"/"+variables_dict["structure_title"]+" Wide"+wide_image_path_tuple[1])
    except: pass  
    #Moving Photos

    variables_dict_keys = list(variables_dict.keys())
    variables_dict_keys.sort(reverse = True, key = (lambda dict_key: len(dict_key)))
    
    #Synopsis Compact
    synopsis_compact_template = open(folder_path+"/Art/Template/Synopsis Compact Template.html","r")
    synopsis_compact_text = synopsis_compact_template.read()
    synopsis_compact_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            synopsis_compact_text = synopsis_compact_text.replace("_title_", str(variables_dict[variable_name]))
        elif ((variable_name == "compact_image_path_extension") and (variables_dict["compact_image_path_extension"] == "")):
            synopsis_compact_text = synopsis_compact_text.replace("compact_image_path_extension", " Wide"+str(variables_dict["wide_image_path_extension"]))
        else:
            synopsis_compact_text = synopsis_compact_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis_compact = open(full_folder_path+"/Synopsis Compact.html","w")
    synopsis_compact.write(synopsis_compact_text)
    synopsis_compact.close()
    #Synopsis Compact

    #Synopsis Wide
    synopsis_wide_template = open(folder_path+"/Art/Template/Synopsis Wide Template.html","r")
    synopsis_wide_text = synopsis_wide_template.read()
    synopsis_wide_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            synopsis_wide_text = synopsis_wide_text.replace("_title_", str(variables_dict[variable_name]))
        elif ((variable_name == "wide_image_path_extension") and (variables_dict["wide_image_path_extension"] == "")):
            synopsis_compact_text = synopsis_compact_text.replace("wide_image_path_extension",str(variables_dict["compact_image_path_extension"]))
        elif (variable_name == "wide_image_path_extension"):
            synopsis_compact_text = synopsis_compact_text.replace("wide_image_path_extension"," Wide"+str(variables_dict["wide_image_path_extension"]))
        else:
            synopsis_wide_text = synopsis_wide_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis_wide = open(full_folder_path+"/Synopsis Wide.html","w")
    synopsis_wide.write(synopsis_wide_text)
    synopsis_wide.close()
    #Synopsis Wide

    #Collection
    collection_template = open(folder_path+"/Art/Template/Collection Template.html","r")
    collection_html = collection_template.read()
    collection_template.close()
    pieces_list = [art_pieces[piece] for piece in range(len(art_pieces_true_false)) if art_pieces_true_false[piece].get()]
    collection_html = collection_html.replace("pieces_list",str(pieces_list))
    collection_html = collection_html.replace("_title_", str(variables_dict["title"]))
    collection = open(full_folder_path+".html","w")
    collection.write(collection_html)
    collection.close()

    for piece in pieces_list:
        piece_file = open(folder_path+"/Art/"+piece+".html")
        piece_html = piece_file.read()
        piece_file.close()
        split_index = piece_html.rfind("</p>")
        add_to_piece = "</p><p class='general'>Part of <a class='feature-link' href='/Art/"+variables_dict["structure_title"]+"'>"+variables_dict["title"]+" Collection</a>."
        piece_file = open(folder_path+"/Art/"+piece+".html","w")
        piece_file.write(piece_html[:split_index]+add_to_piece+piece_html[split_index:])
        piece_file.close()
    #Collection

    #Collection Loader
    feature_loader = open(folder_path+"/Loader.js")
    lines = feature_loader.readlines()
    lines[0] = lines[0][:16] + '["'+variables_dict["structure_title"]+'","c"],' + lines[0][16:]
    feature_loader.close()
    feature_loader = open(folder_path+"/Loader.js","w")
    feature_loader.writelines(lines)
    feature_loader.close()
    #Collection Loader

    #Sitemap
    sitemap = open("sitemap.txt","a")
    sitemap.write("\nhttps://leo-zeuli.github.io/Art/"+variables_dict["structure_title"]+".html")
    sitemap.close()
    #Sitemap

def load_markdown():
    global variables_dict
    previous_markdown = open("Previous Collection Markdown.txt","r")
    variables_dict = eval(previous_markdown.read().strip())
    
    title.set(variables_dict["title"])
    structure_title.set(variables_dict["structure_title"])
    specification.set(variables_dict["specification"])
    
    for piece in range(1,len(variables_dict["art_pieces_true_false"])+1):
        art_pieces_true_false[-piece].set(variables_dict["art_pieces_true_false"][-piece])

    compact_image_path.set(variables_dict["compact_image_path"])
    wide_image_path.set(variables_dict["wide_image_path"])

    wide_synopsis_text.delete("1.0","end-1c")
    wide_synopsis_text.insert("end-1c", variables_dict["wide_synopsis_text"])

def save_markdown():
    update_variables_dict()
    previous_markdown = open("Previous Collection Markdown.txt","w")
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

image_frame = Frame(window)
image_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(image_frame, text="File Path /", bg="white").grid(row=0,column=1)
Label(image_frame, text="Compact Image", bg="white").grid(row=1,column=0)
compact_image_path = StringVar()
Entry(image_frame, textvariable=compact_image_path, bg="white", width="35", highlightbackground="lawn green").grid(row=1,column=1)
Button(image_frame, text ="Directory Select", command = select_compact_image).grid(row=1,column=3,padx=(3,0))
Label(image_frame, text="Wide Image", bg="white").grid(row=2,column=0)
wide_image_path = StringVar()
Entry(image_frame, textvariable=wide_image_path, bg="white", width="35", highlightbackground="lawn green").grid(row=2,column=1)
Button(image_frame, text ="Directory Select", command = select_wide_image).grid(row=2,column=3,padx=(3,0))

select_pieces_frame = Frame(window)
select_pieces_frame.pack(padx=(10, 10), pady=(2,2))
Label(select_pieces_frame, text="Select Pieces", bg="white").grid(row=0,column=0)
feature_links = open(os.path.abspath(os.getcwd())+"/Loader.js")
lines = feature_links.readlines()
feature_links.close()
exec(lines[0][4:-2])
art_pieces = []
for feature in features:
    if feature[1] == "ar":
        art_pieces.append(feature[0])
art_pieces_true_false = []
for piece in range(len(art_pieces)):
    art_pieces_true_false.append(IntVar())
    Checkbutton(select_pieces_frame, text=art_pieces[piece],variable=art_pieces_true_false[piece], onvalue=True, offvalue=False).grid(row=piece+1,column=0)

wide_synopsis_frame = Frame(window)
wide_synopsis_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(wide_synopsis_frame, text="Wide Synopsis", bg="white").grid(row=0,column=0)
wide_synopsis_text = Text(wide_synopsis_frame, bg="white", highlightbackground="blue", height="10")
wide_synopsis_text.grid(row=1,column=0)

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
