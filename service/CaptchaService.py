import cv2
import pytesseract
import numpy as np
from skimage import exposure
import util.CaptchaUtil as util

tesseract_parameters = r'--psm 8 --oem 3 -c  tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


kernel_2x2 = np.ones((2, 2), np.uint8)
kernel_3x3= np.ones((3, 3), np.uint8)

mask_potilhada = cv2.imread("/app/mascaras/mask-point-default.png")
mask_wave = cv2.imread("/app/mascaras/mask-wave-default.png")
mask_fish_eye_v1 = cv2.imread("/app/mascaras/mask-fish-eye-default-01.png")
mask_fish_eye_v2 = cv2.imread("/app/mascaras/mask-fish-eye-default-02.png")


def breakCaptcha (base64EncodedFile):
   
  
   image_mask = util.pre_process_image(base64EncodedFile)

   if(util.is_same_type(mask_wave,image_mask)):
    return quebrarCaptchaWave(image_mask)
   if(util.is_same_type(mask_potilhada,image_mask)):
      return quebrarCaptchaPontilhado(image_mask)
   if((util.is_same_type(mask_fish_eye_v1,image_mask)) or (util.is_same_type(mask_fish_eye_v2,image_mask))):
      return quebrarCaptchaFishEye(image_mask) 
   
   return "Tipo não identificado"
   


def quebrarCaptchaPontilhado(image_mask):

    image_without_background = cv2.bitwise_not(image_mask)

    # Engrossa os pixels
    erosed_image = cv2.erode(image_without_background,kernel_3x3,iterations = 3)

    # definição de região em que a imagem vai ser cortada
    x_start, y_start, x_end, y_end = util.get_bounding_box(erosed_image)

    cropped_img = erosed_image[y_start - 5:y_end + 5, x_start - 5:x_end + 5]

    # Aumenta a imagem
    zoomed = cv2.resize(cropped_img, (289, 114), interpolation=cv2.INTER_LINEAR)
  
    # aplica BLUR
    average = cv2.blur(zoomed, (5, 5))

    captcha_code = pytesseract.image_to_string(average, config=tesseract_parameters)

    return captcha_code.strip()

def quebrarCaptchaWave(image_mask):

    image_without_background = cv2.bitwise_not(image_mask)
    
    not_waved_image = util.remove_wave_effect(image_without_background)

    # Engrossa os pixels
    erosed_image = cv2.erode(not_waved_image,kernel_3x3,iterations = 1)

    # definição de região em que a imagem vai ser cortada
    x_start, y_start, x_end, y_end = util.get_bounding_box(erosed_image)


    cropped_img = erosed_image[13 :y_end + 5, x_start -3:x_end + 5]

    # Aumenta a imagem
    zoomed = cv2.resize(cropped_img, (289, 114), interpolation=cv2.INTER_LINEAR)
  
    # aplica BLUR
    bilateral_blur = cv2.bilateralFilter(zoomed, 9, 75, 75)

    captcha_code = pytesseract.image_to_string(bilateral_blur, config=tesseract_parameters)

    return captcha_code.strip()

def quebrarCaptchaFishEye(image_mask):

    return "fish_yey"

    