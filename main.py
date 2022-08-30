from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

from database import Base, SessionLocal, engine
from config import HOSTNAME, PORT, PROTOCOL
from errors import raise_not_found
from models import URL
from schemas import URLListResponse, URLRequest, URLResponse
from utils import generate_unique_key


app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/url",
    response_model=URLResponse,
    description="""
    Create url which will be shortened.\n
        Examples:\n
        'http://youtube.com'\n
        'https://google.com'
    """
)
def create_url(url: URLRequest, db: Session = Depends(get_db)):
    key = generate_unique_key(db)
    db_url = URL(
        original_url=url.target_url, key=key
    )
    target_url = f'{PROTOCOL}://{HOSTNAME}:{PORT}/{key}'
    db_url.target_url = target_url
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return URLResponse(
        key=db_url.key,
        target_url=db_url.target_url,
        original_url=db_url.original_url,
        click=db_url.click
    )


@app.get(
    "/url",
    response_model=URLListResponse,
    description="List url which will be shortened."
)
def list_urls(db: Session = Depends(get_db)):
    records = db.query(URL).all()
    resp = []
    for record in records:
        resp.append(
            URLResponse(
                key=record.key,
                target_url=record.target_url,
                original_url=record.original_url,
                click=record.click
            )
        )
    return URLListResponse(data=resp)


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    db_url = (
        db.query(URL)
        .filter(URL.key == url_key, URL.is_active)
        .first()
    )
    try:
        if db_url:
            db_url.click += 1
            db.add(db_url)
            db.commit()
            return RedirectResponse(db_url.original_url)
        else:
            raise_not_found(request)
    except HTTPException as exc:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "message": exc.detail,
            },
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
