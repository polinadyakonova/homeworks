from pymystem3 import Mystem
import re
from flask import Flask
from flask import url_for, render_template, request, redirect
import math

app = Flask(__name__)

@app.route('/')
def index(name = None):
    if request.args:
        story = request.args['joke'] 
        mystem = Mystem()
        gramm = mystem.analyze(story)
        characters = set()
        for i in gramm:
            if (str(i).find("од=") != -1) and (str(i).find("неод=") == -1):
                s1 = str(i)[str(i).find("'lex': '") + 8:]
                characters.add(s1[:s1.find(        "'")])
        
        file = open("corp.txt", 'r', encoding = "UTF-8")
        f = file.read()[1:].split('\n\n')
        file.close()
        
        file = open("ans.txt", 'w', encoding = "UTF-8")
        for i in f:
            words = ((re.sub('[,\.\?\!\—\-\(\)\:\;]', '', i)).lower()).split(' ')
            if characters <= set(words):
                f = file.write(i + '\n\n')
        file.close()
        with open("ans.txt", "r", encoding='utf-8') as f:
                content = f.read().split('\n\n')
        return render_template("index.html", content=content)        
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
