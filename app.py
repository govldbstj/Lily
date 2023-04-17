import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

API_KEY = ' 여기에 API 키 복붙해서 넣으세요 '
openai.api_key = API_KEY


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        #menu = request.form["menu"]
        feels = request.form["feels"]
        response = openai.Completion.create(
            model="text-davinci-003",
            #prompt=generate_prompt(menu),
            prompt=generate_prompt(feels),
            temperature=0.6,
            max_tokens = 300
        )
        print('response', response)

        return redirect(url_for("index", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(feels):
    return """나 오늘 기분이 {}한데, 나에게 적절한 말을 한 문장 해줄래?
    feels : 우울
    recommend : 오늘 우울하구나. 따뜻한 차를 마시면서 하루를 정리하는 건 어떄? 너의 우울함이 나아지면 좋겠어.
    feels : 행복
    recommend : 네가 행복하다니, 나도 덩달아 행복해. 나는 네가 매일 행복하면 좋겠어.
    feels : {}
    recommend :""".format(
        feels, feels
    )

'''
def generate_prompt(menu):
    return """오늘 뭐 먹을 지 추천해주라!
    menu : 피자
    recommend : 포테이토 피자, 하와이안 피자, 미트 피자
    menu : 스파게티
    recommend : 크림 스파게티, 토마토 스파게티
    menu : 치킨
    recommend : 간장치킨, 후라이드치킨, 양념치킨
    menu : {}
    recommend :""".format(
        menu.split(',')
    )
'''

'''prompt example
Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
'''