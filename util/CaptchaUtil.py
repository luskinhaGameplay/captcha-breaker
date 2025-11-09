import cv2
import numpy as np
from PIL import Image
from skimage import exposure
import base64
from datetime import datetime

masks = []


masks.append(cv2.imread("/app/mascaras/mask-wave-default.png"))
masks.append(cv2.imread("/app/mascaras/mask-point-default.png")) 
masks.append(cv2.imread("/app/mascaras/mask-fish-eye-default-01.png"))
masks.append(cv2.imread("/app/mascaras/mask-fish-eye-default-02.png"))


def get_bounding_box(img):

  img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

  # Define os limites de "preto"
  lower = np.array([0, 0, 0], dtype=np.uint8)
  upper = np.array([50, 50, 50], dtype=np.uint8)  # Ajuste esse valor para sensibilidade

  mask = cv2.inRange(img, lower, upper)

  # Pega a bounding box dos pixels pretos
  mask_pil = Image.fromarray(mask)
  bbox = mask_pil.getbbox()

  if bbox:
    return bbox
  
def remove_wave_effect(wave_img):
   

    h, w = wave_img.shape[:2]
    X, Y = np.meshgrid(np.arange(w, dtype=np.float32),
                    np.arange(h, dtype=np.float32))

    amplitude = 12.0          # altura da onda (quanto mais alto, mais visível)
    comprimento_onda = 130.0   # distância entre cristas
    deslocamento = 25.0        # deslocamento horizontal da onda (pode animar)

  

    # distorção apenas no eixo Y (vertical)
    map_x = X
    map_y = Y + amplitude * np.sin(2 * np.pi * (X + deslocamento) / comprimento_onda )

    # aplica o remapeamento
    result = cv2.remap(wave_img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return result

def get_mask(img):

  img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

  # Define os limites de "preto"
  lower = np.array([0, 0, 0], dtype=np.uint8)
  upper = np.array([50, 50, 50], dtype=np.uint8)  # Ajuste esse valor para sensibilidade

  mask = cv2.inRange(img, lower, upper)

  return mask

def remove_background(img):
  
  gray_chanel_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  gray_chanel_image = exposure.rescale_intensity(gray_chanel_image, in_range='image', out_range=(0, 255)).astype(np.uint8)

  denoised_image = cv2.bilateralFilter(gray_chanel_image, d=9, sigmaColor=75, sigmaSpace=75)

  mask = get_mask(denoised_image)

  

  return mask

def decodificar_imagen_base_64(base64EncodedFile):

  decoded_data = base64.b64decode(base64EncodedFile)

  np_data = np.fromstring(decoded_data,np.uint8)

  imagem_decodificada = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

  nome_arquivo = f"original_saida_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
  cv2.imwrite(nome_arquivo, imagem_decodificada)

  return imagem_decodificada


def pre_process_image(base64EncodedFile):
   original_image = decodificar_imagen_base_64(base64EncodedFile)

   image_mask = remove_background(original_image)

   return image_mask


def get_image_type (img_teste):
    
    img_teste = cv2.cvtColor(img_teste, cv2.COLOR_GRAY2BGR)
    similarity = []

    for i in range(len(masks)) :
       res = cv2.matchTemplate(masks[i], img_teste, cv2.TM_CCOEFF_NORMED)
       similarity.append(cv2.minMaxLoc(res)[1]) 
    
    return similarity.index(max(similarity))