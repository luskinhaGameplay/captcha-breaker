from fastapi import FastAPI
import service.CaptchaService as captchaService
from util.Base64File import Base64File


app = FastAPI()

@app.get("/solvecaptcha")
async def solveCaptcha(file_payload: Base64File):

    captchaText = captchaService.breakCaptcha(file_payload.file_data)
    return {"captcha": captchaText}