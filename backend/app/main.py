from councils.edinburgh import download_pdf_file
from helpers.parse_data import get_bin_calendar
from helpers.get_street_names import get_edinburgh_streets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
    
app = FastAPI()

# Allow React frontend running on http://localhost:3000 to make requests to FastAPI
origins = [
    "http://localhost:5173",  # React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/street_names/edinburgh")
async def get_edinburgh_street_names():
    return get_edinburgh_streets()

@app.get("/calendar/edinburgh/{street_name}")
async def get_calendar_by_street_name(street_name):
    download_pdf_file(street_name)
    return get_bin_calendar('temp/bin_calendar_temp.pdf')
