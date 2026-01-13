from fastapi import APIRouter, HTTPException
from datetime import datetime

from starlette import status

from app.models.passage_model import PassageModel
from app.routers.journals import get_journal

router = APIRouter(
    prefix="/passages",
    tags=["passages"]
)

# Temporary passage db
passage_database = {
    1: PassageModel(
        id=1,
        journal_id=1,
        title="Passage 1",
        content="Passage 1 goes here",
        created_at=datetime(2026, 1, 9, 10,35),
    ),
    2: PassageModel(
        id=2,
        journal_id=1,
        title="Passage 2",
        content="Passage 2 goes here",
        created_at=datetime(2026, 1, 9, 10,37),
    ),
    3: PassageModel(
        id=3,
        journal_id=2,
        title="Passage 3",
        content="Passage 3 goes here",
        created_at=datetime(2026, 1, 9, 10,38),
    ),
    4: PassageModel(
        id=4,
        journal_id=2,
        title="Passage 4",
        content="Passage 4 goes here",
        created_at=datetime(2026, 1, 9, 10,39),
    ),
    5: PassageModel(
        id=5,
        journal_id=3,
        title="Passage 5",
        content="Passage 5 goes here",
        created_at=datetime(2026, 1, 9, 10,40),
    ),
    6: PassageModel(
        id=6,
        journal_id=3,
        title="Passage 6",
        content="Passage 6 goes here",
        created_at=datetime(2026, 1, 9, 10,41),
    ),
    7: PassageModel(
        id=7,
        journal_id=3,
        title="Passage 7",
        content="Passage 7 goes here",
        created_at=datetime(2026, 1, 9, 10,42),
    )
}


# PUT passage -
@router.post("/journals/{journal_id}/new_passage", status_code=201)
async def create_passage(passage: PassageModel, journal_id: int):


   # TODO: Maybe try to work on this later

    # for existing_passage in passage_database.keys():
    #     if existing_passage.id == passage.id:
    #         raise HTTPException(status_code=409, detail="")

    journal_id = passage.journal_id
    journal = await get_journal(journal_id)
    passage.id = len(passage_database) + 1


    passage_database[passage.id] = passage

    return {
       "message":passage.title + f" in {journal.title} created",
       "inserted_passage":passage
   }


# GET all passages from all journals
@router.get("/")
async def get_all_passages():
    return passage_database


# GET all passages from journal -
@router.get("/journals/{journal_id}/passages/")
async def get_all_passages_from_journal(journal_id: int):
    journal_passages = {}
    for key, value in passage_database.items():
        if value.journal_id == journal_id:
            journal_passages[key] = value
    return journal_passages
    # TODO: maybe if the DB is empty, return a 404 (not found) or 204 (no content)



# GET passage by id -
@router.get("/journals/{journal_id}/passages/{passage_id}")
async def get_passage(passage_id: int):
    if passage_id in passage_database:
        return passage_database[passage_id]
    else:
        raise HTTPException(status_code=404 , detail="Passage not found")


# PATCH update passage by id -
@router.patch("/journals/{journal_id}/passages/{passage_id}")
async def update_passage(passage_id: int, updated_passage: PassageModel):
    if passage_id in passage_database:
        passage_database[passage_id].title = updated_passage.title
        passage_database[passage_id].content = updated_passage.content
        passage_database[passage_id].created_at = updated_passage.created_at
        passage_database[passage_id].updated_at = updated_passage.updated_at

        passage_database[passage_id] = updated_passage

        return {
            "message":updated_passage.title,
            "inserted_passage":updated_passage
        }
    else:
        raise HTTPException(status_code=404 , detail="Passage not found")

# DELETE passage by id
@router.delete("/journals/{journal_id}/passages/{passage_id}")
async def delete_passage(passage_id: int):
    if passage_id in passage_database:

        passage = passage_database[passage_id]
#       if using a real db there would be a: passage.delete()
        deleted_passage = passage_database.pop(passage_id)

        return {
            "message":f"Passage {passage.title} deleted successfully!",
            "deleted_passage":deleted_passage
        }
    else:
        raise HTTPException(status_code=404 , detail="Passage not found - can't delete!")
