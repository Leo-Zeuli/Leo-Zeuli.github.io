#Delete "Previous Narrative Markdown.txt" to clear the data upon opening the program

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

window=Tk()
window.title("Story Markdown")
window["bg"] = "white"

variables_dict = {"title":"", "structure_title":"", "story_type":"",
                  "story_type_specification":"", "synopsis_image_source":"",
                  "synopsis_image_path":"", "synopsis_text":"", "wide_synopsis_text":""}

def update_variables_dict():
    global variables_dict
    variables_dict["title"] = title.get()
    variables_dict["structure_title"] = structure_title.get().strip()
    variables_dict["story_type"] = ["Screenplay","Prose"][story_type.get()]
    variables_dict["story_type_specification"] = story_type_specification.get().strip()
    
    variables_dict["synopsis_image_source"] = synopsis_image_source.get().strip()
    variables_dict["synopsis_image_path"] = synopsis_image_path.get().strip()

    variables_dict["synopsis_text"] = synopsis_text.get("1.0","end-1c").strip()
    variables_dict["wide_synopsis_text"] = wide_synopsis_text.get("1.0","end-1c").strip()
    
    if story_type_specification.get().strip() == "":
        variables_dict["story_type_specification"] = variables_dict["story_type"]

def select_synopsis_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Synopsis Image",
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    synopsis_image_path.set(file_path)

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
    full_folder_path = folder_path+"/Narratives/"+variables_dict["structure_title"]
    if not os.path.exists(full_folder_path):
        os.mkdir(full_folder_path)
    #Make Folder

    #Moving Photo
    synopsis_image_path_tuple = os.path.splitext(synopsis_image_path.get())
    variables_dict["synopsis_image_path_extension"] = synopsis_image_path_tuple[1]
    if not os.path.exists(folder_path+"/Photos/Narratives/"+variables_dict["structure_title"]):
        os.mkdir(folder_path+"/Photos/Narratives/"+variables_dict["structure_title"])
    try:
        os.replace("".join(synopsis_image_path_tuple), folder_path+"/Photos/Narratives/"+variables_dict["structure_title"]+"/"+variables_dict["structure_title"]+synopsis_image_path_tuple[1])
    except: pass
    #Moving Photo

    variables_dict_keys = list(variables_dict.keys())
    variables_dict_keys.sort(reverse = True, key = (lambda dict_key: len(dict_key)))
    
    #Synopsis Compact
    synopsis_compact_template = open(folder_path+"/Narratives/Template/Synopsis Compact Template.html","r")
    synopsis_compact_text = synopsis_compact_template.read()
    synopsis_compact_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "synopsis_image_source":
            if variables_dict["synopsis_image_source"]:
                synopsis_compact_text = synopsis_compact_text.replace("synopsis_image_source", "Image: "+variables_dict["synopsis_image_source"])
            else:
                synopsis_compact_text = synopsis_compact_text.replace("synopsis_image_source", "")
        else:
            synopsis_compact_text = synopsis_compact_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis_compact = open(full_folder_path+"/Synopsis Compact.html","w")
    synopsis_compact.write(synopsis_compact_text)
    synopsis_compact.close()
    #Synopsis Compact

    #Synopsis
    synopsis_template = open(folder_path+"/Narratives/Template/Synopsis Template.html","r")
    synopsis_text = synopsis_template.read()
    synopsis_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "synopsis_image_source":
            if variables_dict["synopsis_image_source"]:
                synopsis_text = synopsis_text.replace("synopsis_image_source", "Image: "+variables_dict["synopsis_image_source"])
            else:
                synopsis_text = synopsis_text.replace("synopsis_image_source", "")
        else:
            synopsis_text = synopsis_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis = open(full_folder_path+"/Synopsis.html","w")
    synopsis.write(synopsis_text)
    synopsis.close()
    #Synopsis

    #Synopsis Wide
    synopsis_wide_template = open(folder_path+"/Narratives/Template/Synopsis Wide Template.html","r")
    synopsis_wide_text = synopsis_wide_template.read()
    synopsis_wide_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "synopsis_image_source":
            if variables_dict["synopsis_image_source"]:
                synopsis_wide_text = synopsis_wide_text.replace("synopsis_image_source", "Image: "+variables_dict["synopsis_image_source"])
            else:
                synopsis_wide_text = synopsis_wide_text.replace("synopsis_image_source", "")
        else:
            synopsis_wide_text = synopsis_wide_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis_wide = open(full_folder_path+"/Synopsis Wide.html","w")
    synopsis_wide.write(synopsis_wide_text)
    synopsis_wide.close()
    #Synopsis Wide

    #Story Loader
    feature_loader = open(folder_path+"/Loader.js")
    lines = feature_loader.readlines()
    lines[0] = lines[0][:16] + '["'+variables_dict["structure_title"]+'","'+{"Screenplay":"s","Prose":"p"}[variables_dict["story_type"]]+'"],' + lines[0][16:]
    feature_loader.close()
    feature_loader = open(folder_path+"/Loader.js","w")
    feature_loader.writelines(lines)
    feature_loader.close()
    #Story Loader

    #Sitemap
    sitemap = open("sitemap.txt","a")
    sitemap.write("\nhttps://leo-zeuli.github.io/Narratives/"+variables_dict["structure_title"]+".html")
    sitemap.close()
    #Sitemap

    #Remainder
    remainder_frame = Frame(window)
    remainder_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
    Label(remainder_frame, text="→", bg="white", fg="red").pack(side="left")
    Label(remainder_frame, text="→", bg="white", fg="orange").pack(side="left")
    Label(remainder_frame, text="→", bg="white", fg="yellow").pack(side="left")
    Label(remainder_frame, text="→", bg="white", fg="lawn green").pack(side="left")
    Label(remainder_frame, text="→", bg="white", fg="cyan").pack(side="left")
    Label(remainder_frame, text="→", bg="white", fg="blue").pack(side="left")
    Label(remainder_frame, text="→", bg="white", fg="purple").pack(side="left")
    Label(remainder_frame, text ='Move "'+variables_dict["structure_title"]+'.html" to /Narratives/').pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="purple").pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="blue").pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="cyan").pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="lawn green").pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="yellow").pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="orange").pack(side="left")
    Label(remainder_frame, text="←", bg="white", fg="red").pack(side="left")
    #Remainder

def load_markdown():
    global variables_dict
    previous_markdown = open("Previous Narrative Markdown.txt","r")
    variables_dict = eval(previous_markdown.read().strip())
    
    title.set(variables_dict["title"])
    structure_title.set(variables_dict["structure_title"])
    story_type.set({"Screenplay":0,"Prose":1}[variables_dict["story_type"]])
    story_type_specification.set(variables_dict["story_type_specification"])
    
    synopsis_image_source.set(variables_dict["synopsis_image_source"])
    synopsis_image_path.set(variables_dict["synopsis_image_path"])

    synopsis_text.delete("1.0","end-1c")
    synopsis_text.insert("end-1c", variables_dict["synopsis_text"])
    wide_synopsis_text.delete("1.0","end-1c")
    wide_synopsis_text.insert("end-1c", variables_dict["wide_synopsis_text"])

def save_markdown():
    update_variables_dict()
    previous_markdown = open("Previous Narrative Markdown.txt","w")
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
#testing.set(1) #Not Testing Defult
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

story_type_frame = Frame(window)
story_type_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
story_type = IntVar()
Radiobutton(story_type_frame, text="Screenplay", variable=story_type, value=0).pack(side="left")
Radiobutton(story_type_frame, text="Prose", variable=story_type, value=1).pack(side="left")
Label(story_type_frame, text="Specification : ", bg="white").pack(side="left")
story_type_specification = StringVar()
Entry(story_type_frame, textvariable=story_type_specification, bg="white", highlightbackground="yellow", width="18").pack(side="left")

image_frame = Frame(window)
image_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(image_frame, text="Image Source", bg="white").grid(row=0,column=2)
Label(image_frame, text="File Path /", bg="white").grid(row=0,column=1)
Label(image_frame, text="Synopsis Image", bg="white").grid(row=1,column=0)
synopsis_image_path = StringVar()
Entry(image_frame, textvariable=synopsis_image_path, bg="white", width="25", highlightbackground="lawn green").grid(row=1,column=1)
synopsis_image_source = StringVar()
Entry(image_frame, textvariable=synopsis_image_source, bg="white", width="10", highlightbackground="lawn green").grid(row=1,column=2)
Button(image_frame, text ="Directory Select", command = select_synopsis_image).grid(row=1,column=3,padx=(3,0))

synopsis_frame = Frame(window)
synopsis_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(synopsis_frame, text="Synopsis", bg="white").grid(row=0,column=0)
synopsis_text = Text(synopsis_frame, bg="white", highlightbackground="cyan", height="10")
synopsis_text.grid(row=1,column=0)

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
