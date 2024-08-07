from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


# Replace with your LLM API endpoint (host and port)
LLM_API_URL = str(os.environ.get('LLM_API_URL', "http://ollama.ollama.svc.cluster.local:11434/api"))
APP_MODELS = [
    {
        "name": "funny-model",
        "modelfile": "FROM mistral\nSYSTEM You are a comedian, you must be funny\nPARAMETER temperature 0.2\n"
    },
    {
        "name": "sql-model",
        "modelfile": "FROM mistral\nSYSTEM You are data analyst trying to help people to query from their databases. They send you a tables strcture and they want to query and you help them with that. \nPARAMETER temperature 0.2\n",
    }
]


def get_available_models():
    try:
        response = requests.get(f"{LLM_API_URL}/tags")
        models_response = response.json()
        return models_response["models"]
    except Exception as e:
        logging.exception(e)

def create_model(model_name, required_models):
    model = next((m for m in required_models if m["name"] == model_name))
    try:
        request = {"model": model["name"], "modelfile": model["modelfile"]}
        response = requests.post(f"{LLM_API_URL}/create", json=request)
        response.raise_for_status()
    except Exception as e:
        logging.exception(e)

def set_up_models(models):
    required_models_names = [model["name"] for model in models]
    available_models = [model["name"].split(":")[0] for model in get_available_models()]
    logging.info("the available models are: %s", available_models)
    logging.info("the required models are: %s", required_models_names)

    if len(set(required_models_names) - set(available_models)) == 0:
        logging.info("All models available")
    else:
        logging.info("missing models are: %s", set(required_models_names) - set(available_models))
        for model in set(required_models_names) - set(available_models):
            create_model(model, required_models_names)
            logging.info("models created succesfully")

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        req_data = request.get_json()
        user_prompt = req_data.get("user_prompt")  # Use get() to avoid KeyError if key is not present
        if not user_prompt:
            return jsonify({"error": "Invalid input"})

        # Format the prompt for LLM request
        llm_request = {"stream": "false", "model": "sql-model", "prompt": user_prompt}

        # Make an HTTP request to LLM API
        logging.info("request to LLM is: %s", llm_request)
        response = requests.post(f"{LLM_API_URL}/generate", json=llm_request, timeout=120)
        logging.info("Full request: %s", json.dumps(llm_request))
        response.raise_for_status()
        logging.info("LLM reponse is: %s", response.raw)
        llm_response = response.json()
        
        # Extract response text and return
        response_text = llm_response.get("text")
        if response_text:
            return jsonify({"response": response_text})
        else:
            return jsonify({"error": "No response text received from LLM"})
    except Exception as e:
        logging.exception("An error occurred: %s", e)
        return jsonify({"error": "An error occurred"})


if __name__ == "__main__":

    set_up_models(APP_MODELS)
    app.run(host='0.0.0.0', port=8080)