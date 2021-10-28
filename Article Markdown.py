from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

window=Tk()
window.title("Article Markdown")
window["bg"] = "white"

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
def select_crown_image():
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Crown Image",
                                             filetypes=(("jpeg files", "*.jpeg"), ("jpg files", "*.jpg"), ("png files", "*.png")))
    crown_image_path.set(file_path)
def process():
    #Gather Variables
    istesting = bool(testing.get())
    film_specific = not bool(article_subject.get())
    star_rating = float(rating.get())

    #article_txt_path.get()
    print(article_txt_path.get())
    #feature_image_path.get()
    #wide_image_path.get()
    #crown_image_path.get()

    folder_path = os.path.abspath(os.getcwd())
    full_folder_path = folder_path+"/Features/"+structure_title.get().strip()
    if not os.path.exists(full_folder_path):
        os.mkdir(full_folder_path)
    variables_dict = {"title" : title.get(),
                      "structure_title" : structure_title.get().strip(),
                      "article_type" : ["Review","Analysis"][article_type.get()],
                      "article_type_specification" : article_type_specification.get(),
                      "feature_image_source" : feature_image_source.get(),
                      "wide_image_source" : wide_image_source.get(),
                      "synopsis_text" : synopsis_text.get("1.0","end-1c"),
                      "wide_synopsis_text" : wide_synopsis_text.get("1.0","end-1c")}
    if article_type_specification.get().strip() == "":
        variables_dict["article_type_specification"] = variables_dict["article_type"]
    if film_specific:
        variables_dict["title"] = variables_dict["title"].replace(variables_dict["structure_title"],"<i>"+variables_dict["structure_title"]+"</i>")
    #Gather Variables
        
    #Synopsis Compact
    synopsis_compact_template = open(folder_path+"/Features/Template/Synopsis Compact Template.html","r")
    synopsis_compact_text = synopsis_compact_template.read()
    synopsis_compact_template.close()
    for variable_name, variable in variables_dict.iteritems():
        synopsis_compact_text = synopsis_compact_text.replace(variable_name, variable)
    synopsis_compact = open(full_folder_path+"/Synopsis Compact.html","w")
    synopsis_compact.write(synopsis_compact_text)
    synopsis_compact.close()
    #Synopsis Compact

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
title = Entry(title_frame, bg="white", width="35", highlightbackground="red")
title.grid(row=0,column=1)
Label(title_frame, text="Structure Title : ", bg="white", justify="left").grid(row=1,column=0)
structure_title = Entry(title_frame, bg="white", width="35", highlightbackground="red")
structure_title.grid(row=1,column=1)
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
article_type_specification = Entry(article_type_frame, bg="white", highlightbackground="yellow")
article_type_specification.pack(side="left")

image_frame = Frame(window)
image_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(image_frame, text="Image Source", bg="white").grid(row=0,column=2)
Label(image_frame, text="File Path /", bg="white").grid(row=0,column=1)
Label(image_frame, text="Feature Image", bg="white").grid(row=1,column=0)
feature_image_path = StringVar()
Entry(image_frame, textvariable=feature_image_path, bg="white", width="25", highlightbackground="lawn green").grid(row=1,column=1)
feature_image_source = Entry(image_frame, bg="white", width="10", highlightbackground="lawn green")
feature_image_source.grid(row=1,column=2)
Button(image_frame, text ="Directory Select", command = select_feature_image).grid(row=1,column=3,padx=(3,0))
Label(image_frame, text="Wide Image", bg="white").grid(row=2,column=0)
wide_image_path = StringVar()
Entry(image_frame, textvariable=wide_image_path, bg="white", width="25", highlightbackground="lawn green").grid(row=2,column=1)
wide_image_source = Entry(image_frame, bg="white", width="10", highlightbackground="lawn green")
wide_image_source.grid(row=2,column=2)
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

crown_frame = Frame(window)
crown_frame.pack(padx=(10, 10), pady=(2,2), anchor="w")
Label(crown_frame, text="Crown Image Path /", bg="white").pack(side="left")
crown_image_path = StringVar()
Entry(crown_frame, textvariable=crown_image_path, bg="white", width="35", highlightbackground="purple").pack(side="left")
ratings = ["0.0","0.5","1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5","5.0"]
rating = StringVar()
rating.set(ratings[0])
OptionMenu(crown_frame, rating, *ratings).pack(side="left")
Button(crown_frame, text ="Directory Select", command = select_crown_image).pack(side="left")

process_frame = Frame(window)
process_frame.pack(padx=(10, 10), pady=(2,2), anchor="center")
Label(process_frame, text="→", bg="white", fg="red").pack(side="left")
Label(process_frame, text="→", bg="white", fg="orange").pack(side="left")
Label(process_frame, text="→", bg="white", fg="yellow").pack(side="left")
Label(process_frame, text="→", bg="white", fg="lawn green").pack(side="left")
Label(process_frame, text="→", bg="white", fg="cyan").pack(side="left")
Label(process_frame, text="→", bg="white", fg="blue").pack(side="left")
Label(process_frame, text="→", bg="white", fg="purple").pack(side="left")
Button(process_frame, text ="Process", command=process).pack(side="left")
Label(process_frame, text="←", bg="white", fg="purple").pack(side="left")
Label(process_frame, text="←", bg="white", fg="blue").pack(side="left")
Label(process_frame, text="←", bg="white", fg="cyan").pack(side="left")
Label(process_frame, text="←", bg="white", fg="lawn green").pack(side="left")
Label(process_frame, text="←", bg="white", fg="yellow").pack(side="left")
Label(process_frame, text="←", bg="white", fg="orange").pack(side="left")
Label(process_frame, text="←", bg="white", fg="red").pack(side="left")
