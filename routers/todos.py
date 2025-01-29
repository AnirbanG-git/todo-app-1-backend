from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import crud
from database import SessionLocal

from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
#from langchain.chains import LLMChain

router = APIRouter(
    prefix="/todos"
)

# LANGCHAIN
langchain_llm = OpenAI(temperature=0)

summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

# summarize_chain = LLMChain(
#     llm=langchain_llm,
#     prompt=summarize_prompt,
# )

summarize_chain = summarize_prompt | langchain_llm

write_poem_template_string = """
        Write a short poem with the following text:
        {text}
"""

write_poem_prompt = PromptTemplate(
    template=write_poem_template_string,
    input_variables=['text'],
)

# write_poem_chain = LLMChain(
#     llm=langchain_llm,
#     prompt=write_poem_prompt,
# )

write_poem_chain = write_poem_prompt | langchain_llm

@router.post('/summarize-text')
async def summarize_text(request: schemas.SummarizeRequest):
    print("in summarize router \n")
    summary = summarize_chain.invoke(input=request.text)
    return {'summary': summary}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/write-poem/{id}")
async def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    poem = write_poem_chain.invoke(input=todo.name)
    return {'poem': poem}        

@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, todo)
    return todo

@router.get("", response_model=List[schemas.ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.put("/{id}")
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")