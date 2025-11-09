from fastapi import FastAPI
import service.CaptchaService as captchaService
from util.Base64File import Base64File


app = FastAPI()

@app.post("/solvecaptcha")
async def solveCaptcha(file_payload: Base64File):
    #print("recebi")
    captchaText = captchaService.breakCaptcha(file_payload.file_data)
    print(captchaText)
    return {"captcha": captchaText}