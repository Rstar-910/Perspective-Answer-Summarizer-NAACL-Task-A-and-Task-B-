import os
import torch
import json
from flask import Flask, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
def load_model():
    t5_model_path = "C:/Users/Dell/Desktop/NAACL/T5_model"  
    t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_path)
    t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_path).to(device)
    return t5_tokenizer, t5_model



# def extract_spans_rule_based(answer):
#     spans = []

#     # Keywords for each category
#     cause_keywords = ["because", "due to", "caused by", "reason for", "linked to"]
#     suggestion_keywords = ["should", "recommend", "try", "consider", "advisable", "suggested"]
#     experience_keywords = ["I experienced", "some people", "many users", "often report", "in my case"]
#     information_keywords = ["is known to", "commonly", "typically", "often", "generally", "characterized by"]

#     sentences = answer.split(".")  # Split answer into sentences

#     for sentence in sentences:
#         sentence = sentence.strip()
#         if not sentence:
#             continue

#         for word in cause_keywords:
#             if word in sentence:
#                 spans.append({"text": sentence, "category": "CAUSE"})
#                 break
#         for word in suggestion_keywords:
#             if word in sentence:
#                 spans.append({"text": sentence, "category": "SUGGESTION"})
#                 break
#         for word in experience_keywords:
#             if word in sentence:
#                 spans.append({"text": sentence, "category": "EXPERIENCE"})
#                 break
#         for word in information_keywords:
#             if word in sentence:
#                 spans.append({"text": sentence, "category": "INFORMATION"})
#                 break

#     # Deduplicate spans
#     unique_spans = {span["text"]: span for span in spans}.values()
#     return list(unique_spans) if unique_spans else [{"text": "No relevant spans found.", "category": "NONE"}]

# Span extraction function
def extract_spans_rule_based(answer):
    spans = []

    # Keywords for each category
    cause_keywords = ["because", "due to", "caused by", "reason for", "linked to"]
    suggestion_keywords = ["should", "recommend", "try", "consider", "advisable", "suggested", "use", "take", "flush", "apply", "put"]
    experience_keywords = ["I experienced", "some people", "many users", "often report", "in my case"]
    information_keywords = ["is known to", "commonly", "typically", "often", "generally", "characterized by"]

    sentences = answer.split(".")  # Split answer into sentences

    for sentence in sentences:
        sentence = sentence.strip()

        for word in cause_keywords:
            if word in sentence:
                spans.append({"text": sentence, "category": "CAUSE"})
                break
        for word in suggestion_keywords:
            if word in sentence:
                spans.append({"text": sentence, "category": "SUGGESTION"})
                break
        for word in experience_keywords:
            if word in sentence:
                spans.append({"text": sentence, "category": "EXPERIENCE"})
                break
        for word in information_keywords:
            if word in sentence:
                spans.append({"text": sentence, "category": "INFORMATION"})
                break

    # Deduplicate spans
    unique_spans = {span["text"]: span for span in spans}.values()
    return list(unique_spans)

# Summary generation function
# def generate_summary(question, spans, task, tokenizer, model):
#     task_prompts = {
#         "information_summary": "Summarize the key information:",
#         "cause_summary": "Summarize the main causes:",
#         "experience_summary": "Summarize user experiences:",
#         "suggestion_summary": "Provide actionable suggestions:"
#     }

#     # Use extracted spans instead of full answers
#     extracted_text = " ".join([span["text"] for span in spans]) if spans else "No relevant spans found."
#     input_text = f"{task_prompts[task]} Question: {question} Answer: {extracted_text}"

#     inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)

#     output = model.generate(
#         **inputs,
#         max_length=100,
#         num_beams=7,
#         repetition_penalty=2.0,
#         length_penalty=1.0,
#         early_stopping=True
#     )

#     return tokenizer.decode(output[0], skip_special_tokens=True)

def generate_summary(question, spans, task, tokenizer, model):
    task_prompts = {
        "information_summary": "Summarize the key information:",
        "cause_summary": "Summarize the main causes:",
        "experience_summary": "Summarize user experiences:",
        "suggestion_summary": "Provide actionable suggestions:"
    }

    # Refine extracted spans for better input
    extracted_text = "\n".join([f"{span['category']}: {span['text']}" for span in spans]) if spans else "No relevant spans found."
    input_text = f"{task_prompts[task]} Question: {question}\nExtracted Information:\n{extracted_text}"

    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True).to(device)

    output = model.generate(
        **inputs,
        max_length=100,
        num_beams=5,  # Reduced beams for faster generation
        repetition_penalty=2.5,  # Increased to reduce repetition
        length_penalty=1.2,  # Encourage concise summaries
        early_stopping=True
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)

# Load model at startup
tokenizer, model = load_model()

@app.route('/api/process-question', methods=['POST'])
def process_question():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')

    # Extract spans
    spans = extract_spans_rule_based(answer)

    # Generate summaries
    summaries = {
        'information_summary': generate_summary(question, spans, 'information_summary', tokenizer, model),
        'cause_summary': generate_summary(question, spans, 'cause_summary', tokenizer, model),
        'experience_summary': generate_summary(question, spans, 'experience_summary', tokenizer, model),
        'suggestion_summary': generate_summary(question, spans, 'suggestion_summary', tokenizer, model)
    }

    # Combine results
    results = {
        'spans': spans,
        **summaries
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)