from fastapi import FastAPI, APIRouter, UploadFile, File, Form, Body
from .vector_ops import vectorize_file, hybrid_search
from .db_utils import connect_db, load_file_to_db
import tempfile

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

@router.post("/upload_data")
async def upload_data(
    file: UploadFile = File(...),
    db_url: str = Form("sqlite:///app.db"),
    table_name: str | None = Form(None),
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
    engine = connect_db(db_url)
    return load_file_to_db(path, engine, table_name)

@router.get("/prompt_templates")
def get_prompt_list():
    from .prompt_templates import list_prompts
    return {"files": list_prompts()}

@router.get("/prompt_template")
def get_prompt(filename: str):
    from .prompt_templates import load_prompt
    return {"content": load_prompt(filename)}

@router.put("/prompt_template")
def update_prompt(filename: str, content: str = Body(...)):
    from .prompt_templates import save_prompt
    save_prompt(filename, content)
    return {"msg": "저장 완료"}

app = FastAPI()
app.include_router(router)

