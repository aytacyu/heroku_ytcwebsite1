from flask import Flask,render_template,request
import json
from difflib import get_close_matches
from random import choice

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/dictionary/", methods=['POST','GET'])
def dictionary():
    with open("data.json","r") as json_file:
        data = json.load(json_file)
    if request.method == 'POST':
        if request.form['action'] == 'Check':
            word = request.form["data"].lower()
            word_found = 0
            match_found =0
            if word in data:
                mean = data[word]
                word_found =1
            elif len(get_close_matches(word, data.keys())) > 0:
                word = get_close_matches(word, data.keys())[0]
                mean = data[word]
                match_found = 1
            else :
                mean="The word doesn't exist. Please double check it."
            return render_template("dictionary.html",word=word,mean=mean,word_found=word_found,match_found=match_found)
        elif request.form['action'] == 'TELL':
            word = choice(list(data.keys()))
            mean = data[word]
            word_found = 1
            return render_template("dictionary.html",word=word,mean=mean,word_found=word_found)
        elif request.form['action'] == 'Add/Remove':
             return render_template("change.html")
        elif request.form['action'] == "Add":
            word = request.form["data"]
            exists = 0
            mean = ""
            if word in data:
                mean = data[word]
                exists = 1
            return render_template("add.html",add_word=word,exists=exists,mean=mean)

        elif request.form['action'] == "Add_Meaning":
            word = request.form["word"]
            meaning = request.form["data"]
            if word in data:
                data[word].append(meaning)
            else:
                mean_list = [meaning]
                data[word] = mean_list
            with open('data.json', 'w') as json_file:
                json_file.write(json.dumps(data, indent=4, sort_keys=True))
            return render_template("dictionary.html")
        elif request.form['action'] == "Remove":
            word = request.form["data"]
            if word in data:
                remove_mean = data[word][-1]
                if len(data[word]) > 1:
                    data[word].pop()
                    mean = data[word]
                else:
                    data.pop(word)
                    mean = ""
                with open('data.json', 'w') as json_file:
                    json_file.write(json.dumps(data, indent=4, sort_keys=True))
                return render_template("remove.html",remove_word=word,remove_mean=remove_mean,mean=mean)
            else:
                return render_template("change.html",not_found=word)
        elif request.form['action'] == "Remove_Meaning":
            return render_template("dictionary.html")
    return render_template("dictionary.html")


if __name__=="__main__":
    app.run(debug=True)
