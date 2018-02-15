from flask import Flask,render_template,request
import json
from difflib import get_close_matches

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/dictionary/", methods=['POST','GET'])
def dictionary():
    if request.method == 'POST':
        print("***")
        result = request.form
        try :
            yn=result["yn"]
            if yn=="Yes":
                word=result["word"]
            elif yn=="No":
                word=""
        except:
            yn=None
            word=result["word"]
        replace=None
        print(result)
        print(word)
        word = word.lower()
        data = json.load(open("data.json"))
        if word in data:
            mean=data[word]
        elif word.title() in data:
            mean=data[word.title()]
        elif word.upper() in data:
            mean=data[word.upper()]
        elif len(get_close_matches(word, data.keys())) > 0:
            replace=get_close_matches(word, data.keys())[0]
            #error="Did you mean %s instead? Enter Y if yes, or N if no: " %replaced
            mean=""
        else :
            mean="The word doesn't exist. Please double check it."
        """
            if yn.lower() == "y":
                return data[get_close_matches(w, data.keys())[0]]
            elif yn.lower() == "n":
                return "The word doesn't exist. Please double check it."
            else:
                return "We didn't understand your entry."
        """
        print(word,mean,replace)
        return render_template("dictionary.html",word=word,mean=mean,replace=replace)
    return render_template("dictionary.html",)


if __name__=="__main__":
    app.run(debug=True)
