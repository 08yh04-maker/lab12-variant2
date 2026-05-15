from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, books, readers, borrows, fines, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="Full-featured library management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrows.router)
app.include_router(fines.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "Library Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }
