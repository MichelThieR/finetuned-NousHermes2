from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from gradientai import Gradient

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.post("/")
def chat_response():
    user_prompt = request.json.get("prompt")
    response = generate_response(user_prompt)
    result = {"response": response}
    return jsonify(result)



def generate_response(prompt):

    with Gradient() as gradient:
        llm_model = gradient.get_model_adapter(
            model_adapter_id="cc1beb01-cae2-4d74-8c83-0d5bb484caa5_model_adapter"
        )

        query = f"### Instruction: {prompt}\n\n### Response: "

        complete_response = llm_model.complete(
            query=query,
            max_generated_token_count=128
        )
    
    return complete_response.generated_output

if __name__ == "__main__":
    app.run(debug=True)