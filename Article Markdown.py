#Delete "Previous Markdown.txt" to clear the data upon opening the program

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

window=Tk()
window.title("Article Markdown")
window["bg"] = "white"

variables_dict = {"title":"", "structure_title":"", "article_subject":"", "article_type":"",
                  "article_type_specification":"", "feature_image_source":"", "wide_image_source":"",
                  "synopsis_text":"", "wide_synopsis_text":"", "article_txt_path":"",
                  "feature_image_path":"", "wide_image_path":"", "star_image_path":"", "rating":""}

def update_variables_dict():
    global variables_dict
    variables_dict["title"] = title.get()
    variables_dict["structure_title"] = structure_title.get().strip()
    variables_dict["article_subject"] = article_subject.get()
    variables_dict["article_type"] = ["Review","Analysis"][article_type.get()]
    variables_dict["article_type_specification"] = article_type_specification.get().strip()
    variables_dict["feature_image_source"] = feature_image_source.get().strip()
    variables_dict["wide_image_source"] = wide_image_source.get().strip()
    variables_dict["synopsis_text"] = synopsis_text.get("1.0","end-1c").strip()
    variables_dict["wide_synopsis_text"] = wide_synopsis_text.get("1.0","end-1c").strip()

    variables_dict["article_txt_path"] = article_txt_path.get().strip()
    variables_dict["feature_image_path"] = feature_image_path.get().strip()
    variables_dict["wide_image_path"] = wide_image_path.get().strip()
    variables_dict["star_image_path"] = star_image_path.get().strip()

    variables_dict["rating"] = rating.get()
    
    if article_type_specification.get().strip() == "":
        variables_dict["article_type_specification"] = variables_dict["article_type"]

def select_article_txt():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Article.txt",
                                             filetypes=(("text files","*.txt"),))
    article_txt_path.set(file_path)
def select_feature_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Feature Image",
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    feature_image_path.set(file_path)
def select_wide_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Wide Image",  
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    wide_image_path.set(file_path)
def select_star_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Star Image",
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    star_image_path.set(file_path)

def process_router():
    istesting = bool(testing.get())
    if istesting:
        folder_path = os.path.abspath(os.getcwd())
        feature_loader = open(folder_path+"/Features/Features-Loader.js")
        lines = feature_loader.readlines()
        lines[0] = lines[0][:16] + "["+structure_title.get().strip()+","+{"Review":"r","Analysis":"a"}[["Review","Analysis"][article_type.get()]]+"]," + lines[0][16:]
        feature_loader.close()
        feature_loader = open(folder_path+"/Features/Features-Loader.js","w")
        feature_loader.writelines(lines)
        feature_loader.close()
    else:
        process()
def process():
    update_variables_dict()

    #Make Folder
    folder_path = os.path.abspath(os.getcwd())
    full_folder_path = folder_path+"/Features/"+variables_dict["structure_title"]
    if not os.path.exists(full_folder_path):
        os.mkdir(full_folder_path)
    #Make Folder

    #Moving Photos
    feature_image_path_tuple = os.path.splitext(feature_image_path.get())
    variables_dict["feature_image_path_extension"] = feature_image_path_tuple[1]
    wide_image_path_tuple = os.path.splitext(wide_image_path.get())
    variables_dict["wide_image_path_extension"] = wide_image_path_tuple[1]
    star_image_path_tuple = os.path.splitext(star_image_path.get())
    variables_dict["star_image_path_extension"] = star_image_path_tuple[1]
    if not os.path.exists(folder_path+"/Photos/Features/"+variables_dict["structure_title"]):
        os.mkdir(folder_path+"/Photos/Features/"+variables_dict["structure_title"])
    try:
        os.replace("".join(feature_image_path_tuple), folder_path+"/Photos/Features/"+variables_dict["structure_title"]+"/"+variables_dict["structure_title"]+feature_image_path_tuple[1])
    except: pass
    try:
        os.replace("".join(wide_image_path_tuple), folder_path+"/Photos/Features/"+variables_dict["structure_title"]+"/"+variables_dict["structure_title"]+" Wide"+wide_image_path_tuple[1])
    except: pass
    try:
        os.replace("".join(star_image_path_tuple), folder_path+"/Photos/Features/"+variables_dict["structure_title"]+"/"+variables_dict["structure_title"]+" Star"+star_image_path_tuple[1])
    except: pass
    #Moving Photos

    variables_dict_keys = list(variables_dict.keys())
    variables_dict_keys.sort(reverse = True, key = (lambda dict_key: len(dict_key)))
    
    #Synopsis Compact
    synopsis_compact_template = open(folder_path+"/Features/Template/Synopsis Compact Template.html","r")
    synopsis_compact_text = synopsis_compact_template.read()
    synopsis_compact_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            if not bool(variables_dict["article_subject"]):
                synopsis_compact_text = synopsis_compact_text.replace("_title_",variables_dict["title"].replace(variables_dict["structure_title"],"<i>"+variables_dict["structure_title"]+"</i>"))
            else:
                synopsis_compact_text = synopsis_compact_text.replace("_title_", str(variables_dict[variable_name]))
        else:
            synopsis_compact_text = synopsis_compact_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis_compact = open(full_folder_path+"/Synopsis Compact.html","w")
    synopsis_compact.write(synopsis_compact_text)
    synopsis_compact.close()
    #Synopsis Compact

    #Synopsis
    synopsis_template = open(folder_path+"/Features/Template/Synopsis Template.html","r")
    synopsis_text = synopsis_template.read()
    synopsis_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            if not bool(variables_dict["article_subject"]):
                synopsis_text = synopsis_text.replace("_title_",variables_dict["title"].replace(variables_dict["structure_title"],"<i>"+variables_dict["structure_title"]+"</i>"))
            else:
                synopsis_text = synopsis_text.replace("_title_", str(variables_dict[variable_name]))
        else:
            synopsis_text = synopsis_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis = open(full_folder_path+"/Synopsis.html","w")
    synopsis.write(synopsis_text)
    synopsis.close()
    #Synopsis

    #Synopsis Wide
    synopsis_wide_template = open(folder_path+"/Features/Template/Synopsis Wide Template.html","r")
    synopsis_wide_text = synopsis_wide_template.read()
    synopsis_wide_template.close()
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            if not bool(variables_dict["article_subject"]):
                synopsis_wide_text = synopsis_wide_text.replace("_title_",variables_dict["title"].replace(variables_dict["structure_title"],"<i>"+variables_dict["structure_title"]+"</i>"))
            else:
                synopsis_wide_text = synopsis_wide_text.replace("_title_", str(variables_dict[variable_name]))
        else:
            synopsis_wide_text = synopsis_wide_text.replace(variable_name, str(variables_dict[variable_name]))
    synopsis_wide = open(full_folder_path+"/Synopsis Wide.html","w")
    synopsis_wide.write(synopsis_wide_text)
    synopsis_wide.close()
    #Synopsis Wide

    #Article
    article_template = open(folder_path+"/Features/Template/Article Template.html","r")
    article_text = article_template.read()
    article_template.close()
    star_template = "<img src='/Photos/Features/structure_title/structure_title%20Starstar_image_path_extension' alt='structure_title Themed Star' class='star'>"
    half_star_template = "<div class='half' style='display: inline-block'><img src='/Photos/Features/structure_title/structure_title%20Starstar_image_path_extension' alt='structure_title Themed Half-Star' class='star'></div>"
    article_text = article_text.replace("<star></star>", int(float(variables_dict["rating"]))*star_template+int(2*(float(variables_dict["rating"])%1))*half_star_template)
    for variable_name in variables_dict_keys:
        if variable_name == "title":
            if not bool(variables_dict["article_subject"]):
                article_text = article_text.replace("_title_",variables_dict["title"].replace(variables_dict["structure_title"],"<i>"+variables_dict["structure_title"]+"</i>"))
            else:
                article_text = article_text.replace("_title_", str(variables_dict[variable_name]))
        else:
            article_text = article_text.replace(variable_name, str(variables_dict[variable_name]))
    raw_article_text = open(article_txt_path.get(),"r")
    formated_raw_article_text = ""
    for paragraph in raw_article_text.read().splitlines():
        if paragraph:
            formated_raw_article_text += ('<p class="general">'+paragraph+"</p>")
    article_text = article_text.replace('<p class="general"></p>',formated_raw_article_text)
    article = open(full_folder_path+"/"+variables_dict["structure_title"]+".html","w")
    article.write(article_text)
    article.close()
    #Article

    #Feature Loader
    feature_loader = open(folder_path+"/Features/Features-Loader.js")
    lines = feature_loader.readlines()
    lines[0] = lines[0][:16] + '["'+variables_dict["structure_title"]+'","'+{"Review":"r","Analysis":"a"}[variables_dict["article_type"]]+'"],' + lines[0][16:]
    feature_loader.close()
    feature_loader = open(folder_path+"/Features/Features-Loader.js","w")
    feature_loader.writelines(lines)
    feature_loader.close()
    #Feature Loader

def load_markdown():
    global variables_dict
    previous_markdown = open("Previous Markdown.txt","r")
    variables_dict = eval(previous_markdown.read().strip())
    
    title.set(variables_dict["title"])
    structure_title.set(variables_dict["structure_title"])
    article_subject.set(variables_dict["article_subject"])
    article_type.set({"Review":0, "Analysis":1}[variables_dict["article_type"]])
    article_type_specification.set(variables_dict["article_type_specification"])
    feature_image_source.set(variables_dict["feature_image_source"])
    wide_image_source.set(variables_dict["wide_image_source"])
    article_type_specification.set(variables_dict["article_type_specification"])

    synopsis_text.delete("1.0","end-1c")
    synopsis_text.insert("end-1c", variables_dict["synopsis_text"])
    wide_synopsis_text.delete("1.0","end-1c")
    wide_synopsis_text.insert("end-1c", variables_dict["wide_synopsis_text"])

    article_txt_path.set(variables_dict["article_txt_path"])
    feature_image_path.set(variables_dict["feature_image_path"])
    wide_image_path.set(variables_dict["wide_image_path"])
    star_image_path.set(variables_dict["star_image_path"])

    rating.set(variables_dict["rating"])

def save_markdown():
    update_variables_dict()
    previous_markdown = open("Previous Markdown.txt","w")
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
Entry(title_frame, textvariable=title, bg="white", width="35", highlightbackground="red").grid(row=0,column=1)
Label(title_frame, text="Structure Title : ", bg="white", justify="left").grid(row=1,column=0)
structure_title = StringVar()
Entry(title_frame, textvariable=structure_title, bg="white", width="35", highlightbackground="red").grid(row=1,column=1)
article_subject = IntVar()
Radiobutton(title_frame, text="General", variable=article_subject, value=1).grid(row=0,column=2,padx=(3,0),sticky="w")
Radiobutton(title_frame, text="Film(s) Specific", variable=article_subject, value=0).grid(row=1,column=2,padx=(3,0),sticky="w")

article_txt_frame = Frame(window)
article_txt_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(article_txt_frame, text="Article .txt Path /", bg="white").pack(side="left")
article_txt_path = StringVar()
Entry(article_txt_frame, textvariable=article_txt_path, bg="white", width="35", highlightbackground="orange").pack(side="left")
Button(article_txt_frame, text ="Directory Select", command = select_article_txt).pack(side="left",padx=(3,0))

article_type_frame = Frame(window)
article_type_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
article_type = IntVar()
Radiobutton(article_type_frame, text="Review", variable=article_type, value=0).pack(side="left")
Radiobutton(article_type_frame, text="Analysis", variable=article_type, value=1).pack(side="left")
Label(article_type_frame, text="Specification : ", bg="white").pack(side="left")
article_type_specification = StringVar()
Entry(article_type_frame, textvariable=article_type_specification, bg="white", highlightbackground="yellow").pack(side="left")

image_frame = Frame(window)
image_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(image_frame, text="Image Source", bg="white").grid(row=0,column=2)
Label(image_frame, text="File Path /", bg="white").grid(row=0,column=1)
Label(image_frame, text="Feature Image", bg="white").grid(row=1,column=0)
feature_image_path = StringVar()
Entry(image_frame, textvariable=feature_image_path, bg="white", width="25", highlightbackground="lawn green").grid(row=1,column=1)
feature_image_source = StringVar()
Entry(image_frame, textvariable=feature_image_source, bg="white", width="10", highlightbackground="lawn green").grid(row=1,column=2)
Button(image_frame, text ="Directory Select", command = select_feature_image).grid(row=1,column=3,padx=(3,0))
Label(image_frame, text="Wide Image", bg="white").grid(row=2,column=0)
wide_image_path = StringVar()
Entry(image_frame, textvariable=wide_image_path, bg="white", width="25", highlightbackground="lawn green").grid(row=2,column=1)
wide_image_source = StringVar()
Entry(image_frame, textvariable=wide_image_source, bg="white", width="10", highlightbackground="lawn green").grid(row=2,column=2)
Button(image_frame, text ="Directory Select", command = select_wide_image).grid(row=2,column=3,padx=(3,0))

synopsis_frame = Frame(window)
synopsis_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(synopsis_frame, text="Synopsis", bg="white").grid(row=0,column=0)
synopsis_text = Text(synopsis_frame, bg="white", highlightbackground="cyan", highlightcolor="cyan", height="10")
synopsis_text.grid(row=1,column=0)

wide_synopsis_frame = Frame(window)
wide_synopsis_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(wide_synopsis_frame, text="Wide Synopsis", bg="white").grid(row=0,column=0)
wide_synopsis_text = Text(wide_synopsis_frame, bg="white", highlightbackground="blue", highlightcolor="blue", height="10")
wide_synopsis_text.grid(row=1,column=0)

star_frame = Frame(window)
star_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(star_frame, text="Star Image Path /", bg="white").pack(side="left")
star_image_path = StringVar()
Entry(star_frame, textvariable=star_image_path, bg="white", width="35", highlightbackground="purple").pack(side="left")
ratings = ["0.0","0.5","1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5","5.0"]
rating = StringVar()
rating.set(ratings[0])
OptionMenu(star_frame, rating, *ratings).pack(side="left")
Button(star_frame, text ="Directory Select", command = select_star_image).pack(side="left")

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
