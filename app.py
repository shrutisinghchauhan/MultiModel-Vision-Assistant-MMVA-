import os
from flask import Flask, render_template, request, jsonify
from PIL import Image

# Importing llm_model loads CLIP, the FAISS store, and the Llama model ONCE at startup.
import llm_model
from imgchecker import if_valid
from img2txt import img2txt

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DATA_FOLDER = "data"
DB_FAISS_PATH = "vectorstore/db_faiss"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)


def generate_answer(text, image):
    """Runs the full pipeline and returns the answer PLUS the intermediate
    signals (caption, label, retrieved chunks) so the UI can show its work."""
    label = if_valid(image)          # VGG16 chest-X-ray class, or None
    caption = img2txt(image)         # BLIP caption
    clip = llm_model.model

    text_emb = clip.encode(text + (label or ""))   # guard against label=None
    image_emb = clip.encode(image)
    imgtxt_emb = clip.encode(caption)

    text_hits = llm_model.db.similarity_search_by_vector(text_emb)
    image_hits = llm_model.db.similarity_search_by_vector(image_emb)
    imgtxt_hits = llm_model.db.similarity_search_by_vector(imgtxt_emb)

    sources, seen = [], set()
    for via, hits in (("text query", text_hits), ("image", image_hits), ("caption", imgtxt_hits)):
        if hits:
            content = hits[0].page_content.strip()
            if content and content[:60] not in seen:
                seen.add(content[:60])
                sources.append({"via": via, "content": content})

    prompt = f"""'{text}'
    The image shows {caption} and {label}
    The context from the image from the document of interest: '{image_hits[0].page_content if image_hits else ""} and {imgtxt_hits[0].page_content if imgtxt_hits else ""}'
    The context from the text from the document of interest: '{text_hits[0].page_content if text_hits else ""}'"""

    answer = llm_model.llm(prompt)

    return {
        "answer": answer.strip(),
        "caption": caption,
        "label": label if label else "General image (no X-ray class matched)",
        "sources": sources,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    text = request.form.get("text", "").strip()
    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify({"error": "Please attach an image before sending."}), 400
    try:
        image = Image.open(file.stream).convert("RGB")
    except Exception:
        return jsonify({"error": "That file could not be read as an image."}), 400

    image.save(os.path.join(UPLOAD_FOLDER, "uploaded_image.jpg"))
    try:
        return jsonify(generate_answer(text, image))
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}"}), 500


@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    file = request.files.get("pdf")
    if file is None or not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Please choose a .pdf file."}), 400
    file.save(os.path.join(DATA_FOLDER, file.filename))
    try:
        from ingest import create_vector_db
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS

        create_vector_db()
        emb = HuggingFaceEmbeddings(
            model_name="sentence-transformers/clip-ViT-L-14",
            model_kwargs={"device": "cpu"},
        )
        llm_model.db = FAISS.load_local(DB_FAISS_PATH, emb)
        return jsonify({"status": f"Knowledge base rebuilt with '{file.filename}'."})
    except Exception as e:
        return jsonify({"error": f"{type(e).__name__}: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=False, port=8000, host="0.0.0.0")
