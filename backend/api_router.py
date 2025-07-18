from fastapi import APIRouter, UploadFile, File, Form, Body
from .vector_ops import vectorize_file, hybrid_search

router = APIRouter()

@router.post("/vectorize")
async def vectorize(
    file: UploadFile = File(...),
    doc_type: str = Form("PDF"),
):
    meta = {"filename": file.filename}
    return vectorize_file(file.file, doc_type, meta)

@router.post("/search")
def search(payload: dict = Body(...)):
    question = payload.get("question")
    sources = payload.get("sources", ["규칙", "사례", "용어", "PDF"])
    return hybrid_search(question, sources=sources)
