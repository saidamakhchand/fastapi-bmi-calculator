from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class BMIOutout(BaseModel):
    bmi: float  
    message: str

app = FastAPI()

# CORS middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def Hi():
    return {"message": "Marhaba python"}

@app.get("/calculate_bmi", response_model=BMIOutout)
def calculate_bmi(
    weight: float = Query(..., gt=20, lt=200, description="KG"),
    height: float = Query(..., gt=100, lt=250, description="CM")  # تعديل الطول بالسنتيمترات
):
    height_in_meters = height / 100  # تحويل السنتيمترات إلى أمتار
    bmi = weight / (height_in_meters ** 2)
    if bmi < 18.5:
        message = "لديك نقص في الوزن، كل أكثر"
    elif 18.5 <= bmi < 25:
        message = "لديك وزن طبيعي، حافظ عليه"
    elif 25 <= bmi < 30:
        message = "لديك زيادة في الوزن، تمرن أكثر"
    else:
        message = "أنت تعاني من السمنة"
    
    return BMIOutout(bmi=bmi, message=message)
