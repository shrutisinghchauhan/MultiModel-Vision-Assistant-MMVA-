from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def img2txt(image):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    raw_image = image.convert('RGB')

    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    output_string =(processor.decode(out[0], skip_special_tokens=True))
    return output_string
# print(img2txt('uploads/xraytest.jpeg'))