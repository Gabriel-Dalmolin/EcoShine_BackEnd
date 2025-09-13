from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pydantic import BaseModel

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

def format_data(data):
    return_data = []

    for line in data:
        if line.strip() == "customer,email,nb,nt,nv,paid":
            continue
        line = line.strip()
        return_data.append(line)

    return return_data

@app.post("/new_customer")
def add_new_customer(body: Customer):
    customer = body.customer.title().strip()

    with open("data.csv", "a") as f:
        f.write(f"{customer},{body.email},{body.n_baby},{body.n_tutti},{body.n_vanilla},0\n")

@app.get("/")
def return_customers():
    with open("data.csv", "r") as f:
        data = f.readlines()
        return_data = format_data(data)
        return return_data


@app.post("/user_paid/")
def user_paid(
    customer: str,
    paid: bool,
):
    dataframe = pd.read_csv("data.csv")
    dataframe.loc[dataframe["customer"] == customer.strip().capitalize(), "paid"] = int(paid)
    
    with open("data.csv", "w", newline="") as f:
        f.write(dataframe.to_csv(index=False))

@app.post("/delete_user/")
def delete_user(
    customer: str,
):
    dataframe = pd.read_csv("data.csv")
    dataframe = dataframe[dataframe["customer"] != customer.strip().capitalize()]
    
    with open("data.csv", "w", newline="") as f:
        f.write(dataframe.to_csv(index=False))
