import os
from flask_cors import CORS
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask.json import JSONEncoder
import json

# class CustomJSONEncoder(JSONEncoder):
# 	def default(self, obj):
# 		if isinstane(obj, set):
# 			return list(obj)
# 		return JSONEncoder.default(self, obj)


app = Flask(__name__)
CORS(app)
API_KEY = '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'
openai.api_key = API_KEY


# Q1. 당신은 행복한가요?  // 현재 유저의 행복도
Q1 = ["", "불행해. "]

# Q2. 사소한 일도 버거워졌던 적이 있나요? 있다면 어느 빈도야? // 현재 유저의 우울감
Q2 = ["", "우울해. "]

# Q3. 최근 초조하거나 불안하거나 조마조마하게 느낀적이 있으세요? // 현재 유저의 불안 수치
Q3 = ["", "불안감이 너무 높아. "]

# Q4. 어려운 일들이 너무 많이 쌓여서 극복하지 못할 것 같다고 느낀 적 있어? // 현재 유저의 스트레스
Q4 = ["", "스트레스를 매우 많이 받았어. "]

# Q5. 상대방이 위로가 필요하다고 할 때, 어떻게 위로해주는 편이야? // T.F  // case1, 2
Q5 = ["격려와 감정적인 위로와 지지가 필요해. 공감과 따뜻한 말들을 듣고 싶어.", "지금 이 상황을 어떻게 해결하면 좋을지 실용적인 조언이 듣고 싶어."]

# Q6. 힘든 일이 있을 때 어떻게 극복하는 편인가요? // 유저가 힘든 상황을 극복하는 방법에 대한 정보 (혼자 / 사람과) //case3
Q6 = ["혼자서 할 수 있는 일을 추천해줘" , "사람들과 함께 할 수 있는 일을 추천해줘"]

# Q7. 좋아하는 것들을 골라주세요 // 할 일 추천 시 참고
#  노래 듣기, 산책하기, 낮잠 자기, 친구 만나기, 영화보기, 요리하기, 게임하기, 책 읽기, 운동하기, 여행하기 이 중 최대 5개 선택 // case3
Q7 = ["노래 듣기", "산책 하기", "음악 듣기","책 읽기","친구 만나기", "요리하기", "게임하기", "운동하기", "그림 그리기", "노래 부르기", "여행하기", "등산하기", "영화보기", "하늘 보기", "드라이브하기"]

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/comfort", methods = ['POST'])
def comfort():
    
    payload = json.loads(request.json['value'])
    prompt = "나에게 힘이 될 수 있는 따뜻한 이야기를 반드시 40자 이내로 해줘. 나는 " + Q1[int(payload['q1'])]+Q2[int(payload['q2'])]+Q3[int(payload['q3'])]+Q4[int(payload['q4'])]+Q5[int(payload['q5'])] + "나에게 힘이 되는 말 한 마디를 해줘."
    print("{\"prompt\" : \"" + prompt + "\",", end = "")
    completion=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {
        "role":"user",
        "content": prompt,
    }
    ],
    temperature= 0.8,
    max_tokens= 100,
    )
    print("\"completion\" : \"" + completion.choices[0].message.content + "\" }")
    
    return jsonify({
		'text' : completion.choices[0].message.content.replace("\"", ""),
	})
        
        
@app.route("/advice", methods=['POST'])
def advice():
    payload = json.loads(request.json['value'])
    prompt = "오늘의 조언을 해줘. 반드시 40자 이내로 해줘. 나는 " + Q1[int(payload['q1'])]+Q2[int(payload['q2'])]+Q3[int(payload['q3'])]+Q4[int(payload['q4'])]
    print("{\"prompt\" : \"" + prompt + "\",", end = "")
    completion=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {
        "role":"user",
        "content": prompt,
    }
    ],
    temperature= 0.8,
    max_tokens= 100,
    )
    print("\"completion\" : \"" + completion.choices[0].message.content + "\" }")
    
    return jsonify({
		'text' : completion.choices[0].message.content.replace("\"", ""),
	})
        
        
        
@app.route("/todo", methods=['POST'])
def todo():
    payload = json.loads(request.json['value'])
    prompt = "반드시 40자 이내로 알려줘. 내가 오늘 하루동안 사소한 할 일 하나를 \"~ 하는 건 어때요?\" 하는 형식으로 제시해줘. 예를 들어, \"제일 좋아하는 음식을 먹어보는 건 어때요?\" 처럼. 참고로 나는 " + Q1[int(payload['q1'])]+Q2[int(payload['q2'])]+Q3[int(payload['q3'])]+Q4[int(payload['q4'])] + Q6[int(payload['q6'])]+"나는 평소에 힘들 때 "
    data = payload['q7'].strip("]").strip("[")
    print("data : ", data)
    list = data.split(",")
    for i in range(len(list)):
        prompt += Q7[int(list[i])] + ", "
    prompt +="를 하곤 해. 참고해서 오늘 내가 하면 좋을 일을 추천해줘. "
    print("{\"prompt\" : \"" + prompt + "\",", end = "")
    completion=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {
        "role":"user",
        "content": prompt,
    }
    ],
    temperature= 0.8,
    max_tokens= 100,
    )
    print("\"completion\" : \"" + completion.choices[0].message.content + "\" }")
    
    return jsonify({
		'text' : completion.choices[0].message.content.replace("\"", ""),
	})

    
        


# @app.route("/", methods=("GET", "POST"))
# def index():
#     if request.method == "POST":
#         #menu = request.form["menu"]
#         feels = request.form["feels"]
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             #prompt=generate_prompt(menu),
#             prompt=generate_prompt(feels),
#             temperature=0.6,
#             max_tokens = 300
#         )
#         print('response', response)

#         return redirect(url_for("index", result=response.choices[0].text))
#     result = request.args.get("result")
#     return render_template("index.html", result=result)

# def generate_prompt(feels):
#     return """나 오늘 기분이 {}한데, 나에게 적절한 말을 한 문장 해줄래?
#     feels : 우울
#     recommend : 오늘 우울하구나. 따뜻한 차를 마시면서 하루를 정리하는 건 어떄? 너의 우울함이 나아지면 좋겠어.
#     feels : 행복
#     recommend : 네가 행복하다니, 나도 덩달아 행복해. 나는 네가 매일 행복하면 좋겠어.
#     feels : {}
#     recommend :""".format(
#         feels, feels
#     )
