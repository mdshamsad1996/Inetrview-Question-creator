from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn
import os
import aiofiles
import json
from src.helper import llm_pipeline
import csv



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})


@app.post("/upload")
async def chat(request: Request, pdf_file: bytes=File(), filename: str = Form(...)):
   
    base_folder = 'static/docs/'

    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    
    pdf_filename = os.path.join(base_folder,filename)

    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)
    
    response_data = jsonable_encoder(json.dumps({"msg": "sucess", "pdf_filename":pdf_filename}))
    res = Response(response_data)
    return res


def get_csv(file_path):
    answer_generation, question_list = llm_pipeline(file_path)
    base_folder = 'static/output/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    output_file = base_folder+"QA.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"])
        for question in question_list:
            print("Question : ",question)
            answer = answer_generation.run(question)
            print("Answer : ",answer)
            print("---------------------------------------\n\n")
            # save answer to csv file
            csv_writer.writerow([question, answer])
    return output_file

@app.post("/analyze")
async def chat(request: Request, pdf_filename: str = Form(...)):
    output_file = get_csv(pdf_filename)
    response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
    res = Response(response_data)
    return res


if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)