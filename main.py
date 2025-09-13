from fastapi import FastAPI
import pandas as pd

app = FastAPI()

def format_data(data):
    return_data = []

    for line in data:
        if line == r"customer,email,nb,nt,nv,paid\n":
            continue
        line = line.strip()
        return_data.append(line)

    return return_data

@app.post("/new_customer")
def add_new_customer(
    customer: str,
    email: str,
    n_baby: int,
    n_tutti: int,
    n_vanilla: int,
):
    customer = customer.title().strip()

    with open("data.csv", "a") as f:
        f.write(f"{customer},{email},{n_baby},{n_tutti},{n_vanilla},0\n")

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
