# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("image-classification", model="nateraw/food")
# pipe("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/hub/parrots.png")

# def classify_food_image(image):
#     if not image:
#         return None
#     if image.content_type != 'image/jpeg' and image.content_type != 'image/png':
#         return None
#     pipe = pipeline("image-classification", model="nateraw/food")
#     results = pipe(image, top_k=3)
#     return results
# # results = classify_food_image(image_path, pipe)