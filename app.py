from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp
import re

class WordForm(FlaskForm):
    avail_letters = StringField("Letters")
    #, validators= [
        #Regexp(r'^[a-z]+$', message="must contain letters only")
    #])
    #def validate_letters(form, field):
    #    if len(avail_letters) < 2:
    #        raise ValidationError("TEST")
    word_length = SelectField("Word Length",
        choices=[('0', 'Any'), ('3', '3'), ('4', '4'), ('5', '5'),
                 ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')
    ])
    user_regex = StringField("Search Pattern")
    submit = SubmitField("Go")

    


csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/index')
def index():
    form = WordForm()
    return render_template("index.html", form=form)


@app.route('/words', methods=['POST','GET'])
def letters_2_words():

    form = WordForm()
    if form.validate_on_submit():
        letters = form.avail_letters.data
        length = int(form.word_length.data)
        pattern = re.compile(form.user_regex.data + '$')
    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        good_words = set(x.strip().lower() for x in f.readlines())

    if not letters:
        word_set = good_words

    else:
        word_set = set()
        if length == 0:
            for l in range(2,len(letters)+1):
                for word in itertools.permutations(letters,l):
                    w = "".join(word)
                    if pattern and re.match(pattern, w):
                        if w in good_words:
                            word_set.add(w)
                    else:
                        if w in good_words:
                            word_set.add(w)
        else:
            for l in range(length,length+1):
                for word in itertools.permutations(letters,l):
                    w = "".join(word)
                    if pattern and re.match(pattern, w):
                        if w in good_words:
                            word_set.add(w)
                    else:
                        if w in good_words:
                            word_set.add(w)
    

    alphSort = sorted(word_set, key=len)
    print(alphSort)
    return render_template('wordlist.html',
        wordlist=sorted(alphSort),
        name="CS4131")




@app.route('/proxy')
def proxy():
    result = requests.get(request.args['url'])
    resp = Response(result.text)
    resp.headers['Content-Type'] = 'application/json'
    return resp


