from PIL import Image
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from sentence_transformers import SentenceTransformer, util
from imgchecker import if_valid
from img2txt import img2txt

DB_FAISS_PATH = 'vectorstore/db_faiss'

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/clip-ViT-L-14',
                                       model_kwargs={'device': 'cpu'})
db = FAISS.load_local(DB_FAISS_PATH, embeddings)

model = SentenceTransformer('clip-ViT-L-14')




config = {"max_new_tokens": 512, "repetition_penalty": 1.1, "top_k": 30, "top_p": 0.90}
llm = CTransformers(
    model="models/llama-2-7b-chat.ggmlv3.q8_0.bin", model_type="llama", config=config
)


def text_generate(text, image):
    label=if_valid(image)
    img_txt=img2txt(image)
    text_emb=model.encode(text+label)
    image_emb=model.encode(image)
    # label_emb=model.encode(label)
    imgtxt_emb=model.encode(img_txt)

    text_similar = db.similarity_search_by_vector(text_emb)
    image_similar = db.similarity_search_by_vector(image_emb)
    image_text_similar = db.similarity_search_by_vector(imgtxt_emb)

    prompt_for_llm = f"""'{text}'
    The image shows {img_txt} and {label}
    The context from the image from the document of interest: '{image_similar[0].page_content} and {image_text_similar[0].page_content}'
    The context from the text from the document of interest: '{text_similar[0].page_content}'"""

    output_string = llm(prompt_for_llm)

    return output_string
