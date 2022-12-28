from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def send_email(email: str, message: str):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    message = "Bestellung ist aufgegeben."
    background_tasks.add_task(send_email, email, message)
    return {"message": f"Email ist an {email} verschickt worden"}
