# main.py
from fastapi import FastAPI, UploadFile, File, Form
from ai_engine import load_csv_text, answer_question

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Starting app")

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    data = await file.read()
    load_csv_text(data)
    return {"ok": True, "filename": file.filename, "size": len(data)}

@app.post("/ask")
async def ask(question: str = Form(...)):
    answer = answer_question(question)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)