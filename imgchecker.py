from img2txt import img2txt
from vgg16pred import predictive_label
import torch
from sentence_transformers import SentenceTransformer, util
from PIL import Image



model = SentenceTransformer('clip-ViT-L-14')

def sim_score_img_vgg(image):
    img_caption=img2txt(image)
    vgg_label=predictive_label(image)
    img_caption=img2txt(image)
    vgg_label=predictive_label(image)
    text_emb1 = model.encode([img_caption])
    text_emb2=model.encode([vgg_label])
    cos_scores = util.cos_sim(text_emb1, text_emb2)
    tensor_val = torch.tensor(cos_scores)
    value = tensor_val.item()
    return value
    # print(value)
def if_valid(image):
    img_caption=img2txt(image)
    vgg_label=predictive_label(image)
    value=sim_score_img_vgg(image)
    if value>0.55:
        return vgg_label
    else:
        return None
# print(if_valid('uploads/xraytest.jpeg'))