from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai


openai.api_key = "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"

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://riddhi19:hellfire123@clonedb.modwzr6.mongodb.net/chatgpt"
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    chats = mongo.db.chats.find({})
    mychats=[chat for chat in chats]
    print(mychats)
    return render_template('index.html',mychats = mychats)


@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        if not request.json or not "question" in request.json:
            return jsonify({"result": "Hello! How can I assist you today?"})
        print(request.form, request.json)
        question=request.json.get("question")
        chat=mongo.db.chats.find_one({"question":question})
        print(chat)
        if chat:
            # data={"result":f"{chat['answer']}"}
            data = {"question": question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=question,
                    temperature=0.7,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                print(response)
                # data={"question":question,"answer":response}
                data = {"question": question, "answer": response["choices"][0]["text"]}
                # mongo.db.chats.insert_one({"question":question,"answer":response})
                mongo.db.chats.insert_one({"question": question, "answer": response["choices"][0]["text"]})
                return jsonify(data)
            
            except openai.error.RateLimitError:
                data = {"result": "You have exceeded your current quota. Please check your plan and billing details."}
                return jsonify(data)
    data={"result":"Hello! How can I assist you today?"}
    return jsonify(data) 


app.run(debug=True) 
