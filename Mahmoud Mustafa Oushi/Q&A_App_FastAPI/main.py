from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from embedder import embed_and_store
from vector_store import retrieve_similar_chunks
from llms import query as groq_query
import os

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = file.filename
        content = await file.read()
        chunks = embed_and_store(filename, content)
        return {"message": f"File '{filename}' processed and stored.", "chunks": len(chunks), "status":True}
    except Exception as e:
        print("Error:", str(e))
        return {"message": f"Error: {str(e)}", "chunks": 0, "status":False}
        
        # return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query")
async def query_llm(prompt: str = Form(...)):
    try:
        relevant_chunks = retrieve_similar_chunks(prompt)
        context = "\n".join([c.text for c in relevant_chunks])
        response = groq_query(context, prompt)  
        return {"response": response, "status": True, "message": "request was successful"}
    except Exception as e:
        return {"response": '', "status": False, "message": f"Error: {str(e)}"}

