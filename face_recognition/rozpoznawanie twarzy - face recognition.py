from fastapi import FastAPI
import asyncio

from keras_vggface.vggface import VGGFace
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.utils import preprocess_input
import os
from PIL import Image
from numpy import expand_dims
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
from keras_vggface.utils import preprocess_input
from keras_vggface.utils import decode_predictions
import numpy as np

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "skrypt3"}


@app.get("/current_dir")
async def current_dir():
    return {"cwd": os.listdir('./app')}


@app.get("/test")
async def get_test():
    print('test started')
    await asyncio.sleep(1)
    print('test ended')
    return {"Hello": "skrypt1 test"}


# extract a single face from a given photograph
def extract_face(filename, required_size=(224, 224)):
    
    if filename.lower().endswith(".png"):
        pixels = convert_png_to_jpg(filename)
    else:
        pixels = pyplot.imread(filename)
    
    detector = MTCNN()
    results = detector.detect_faces(pixels)
    #TODO if enough time, do this for multiple faces
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height

    # FACE EXTRACTION
    face = pixels[y1:y2, x1:x2]


    # RESIZE IMAGE TO THE MODEL SIZE
    image = Image.fromarray(face)
    image = image.resize(required_size)

    face_array = asarray(image)
    return face_array


def convert_png_to_jpg(filepath):
    im1 = Image.open(filepath)
    rgb_im = im1.convert('RGB')
    rgb_im.save("./tmp.jpg")
    file = pyplot.imread("tmp.jpg")
    if os.path.exists("tmp.jpg"):
        os.remove("tmp.jpg")
    return file
def get_embeddings(filenames):
    
    #extract face from image
    faces = [extract_face(f) for f in filenames]
    samples = asarray(faces, 'float32')
    
    #preprocess image and create model
    samples = preprocess_input(samples, version=2)
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    
    #prediction
    yhat = model.predict(samples)
    return yhat



#def make_file_list(dir_path):
#    
#    all_filelist = []
##     for dirname, _, filenames in os.walk(online_path):
##         for filename in filenames:
##             all_filelist.append(os.path.join(dirname, filename))
#    res = os.listdir(dir_path)
#    for file in res:
#        filepath = os.path.join(dir_path,file)
#        all_filelist.append(filepath)
#
#    return all_filelist



@app.get("/model")
async def get_model():
    # files_to_delete = [] #tmp files to delete after script is finished #miss 
    # all_filelist = [] #list of all files
    #daniel_obajtek_face_path = "/kaggle/input/fake-ads-face-recognition/daniel_obajtek/" #files with face of daniel obajtek
    #rafal_trzaskowski_face_path = "/kaggle/input/fake-ads-face-recognition/rafal_trzaskowski/" #files with face of rafal trzaskowski 
    #ads_files_path = "/kaggle/input/fake-ads-face-recognition/fake_ads/" #ads files

    is_daniel_obajtek_face = False
    is_rafal_trzaskowski_face = False

    cwd = "./app/"
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    #ads_files = make_file_list(ads_files_path)
    ads_files = f'{cwd}ReklamaFacebookOrlen.PNG'
    ads_embeddings = get_embeddings([ads_files])
    rafal_trzaskowski_embeddings = np.load(f'{cwd}rafal_trzaskowski_embeddings.npy')
    daniel_obajtek_embeddings = np.load(f'{cwd}daniel_obajtek_embeddings.npy')
    def is_match(known_embedding, candidate_embedding, thresh=0.45):
        score = cosine(known_embedding, candidate_embedding)
        if score <= thresh:
            # print('>Match (%.3f <= %.3f)' % (score, thresh))
            return True
        else:
            # print('>NOT Match (%.3f > %.3f)' % (score, thresh))
            return False
    #check if rafał trzaskowski

    match_count = 0
    for idx_face, embedding in enumerate(rafal_trzaskowski_embeddings):
    #     for idx_ad, embedding in enumerate(ads_files_embeddings):
        if is_match(rafal_trzaskowski_embeddings[idx_face], ads_embeddings[0]):
            match_count+=1

    if match_count / len(rafal_trzaskowski_embeddings) > 0.5:
        is_rafal_trzaskowski_face = True


    #check if daniel obajtek
    match_count = 0
    for idx_face, embedding in enumerate(daniel_obajtek_embeddings):
    #     for idx_ad, embedding in enumerate(ads_files_embeddings):
        if is_match(daniel_obajtek_embeddings[idx_face], ads_embeddings[0]):
            match_count+=1

    if match_count / len(daniel_obajtek_embeddings) > 0.5:
        is_daniel_obajtek_face = True

    return is_rafal_trzaskowski_face,is_daniel_obajtek_face




