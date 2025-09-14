from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url: str = os.environ.get("SUPABASE_URL") # type: ignore
supabase_key: str = os.environ.get("SUPABASE_KEY") # type: ignore
supabase = create_client(supabase_url, supabase_key)

app = FastAPI()

origins = [
    "http://localhost:5500",  # frontend
    "http://127.0.0.1:5500",
    "https://ecoshine-74nv.onrender.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite GET, POST, OPTIONS etc.
    allow_headers=["*"],
)

class Customer(BaseModel):
    customer: str
    email: str
    n_baby: int
    n_tutti: int
    n_vanilla: int

@app.head("/")
def head_root():
    return Response(status_code=200)

@app.post("/new_customer")
def add_new_customer(body: Customer):
    customer = body.customer.title().strip()
    email = body.email.lower().strip()
    n_baby = body.n_baby
    n_tutti = body.n_tutti
    n_vanilla = body.n_vanilla

    supabase.table("EcoShine").insert({
        "customer": customer,
        "email": email,
        "n_baby": n_baby,
        "n_tutti": n_tutti,
        "n_vanilla": n_vanilla,
        "paid": False
        }).execute()
    

@app.get("/")
def return_customers():
    return supabase.table("EcoShine").select("*").execute().data

class UserPaid(BaseModel):
    id: int
    paid: bool

@app.post("/user_paid/")
def user_paid(req: UserPaid):
    supabase.table("EcoShine").update({"paid": req.paid}).eq("id", req.id).execute()

class DeleteCustomer(BaseModel):
    id: int

@app.post("/delete_user/")
def delete_user(req: DeleteCustomer):
    supabase.table("EcoShine").delete().eq("id", req.id).execute()

