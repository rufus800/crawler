import openai
from constants import OPENAI_API_KEY


users_data = {}

default_user_messages = {
    "role": "system",
    "content": "You are a helpful hiring manager and tech recruiter.",
}


def get_user_data(user_id):
    if user_id in users_data and len(users_data[user_id]) > 1:
        user_messages = users_data[user_id]
        return user_messages
    else:
        users_data[user_id] = [default_user_messages]
        user_messages = users_data[user_id]
        return user_messages


def update_user_data(user_id, type, response):
    user_messages = get_user_data(user_id)
    if type == "user":
        user_messages.append({"role": "user", "content": f"{response}"})
    elif type == "assistant":
        user_messages.append({"role": "assistant", "content": f"{response}"})
    users_data[user_id] = user_messages


def prompt_gpt_bot(cv_raw_text, job_title, job_description_text, username):
    question = f"Imagine you were a hiring manager or recruiter hiring for a {job_title} Role, How would you match this cv {cv_raw_text} to this job {job_description_text}"

    """
    TODO
    Create a loop here to ask 4 questions.
    some questions
    1. What to improve in the CV as regards the JD
    1. What to improve in the CV to increase my chances.
    3. What score does the the AI rate the Cv with respect to the job description
    4. What score does the the AI rate the Cv in general terms

    Note: Limit people to asking only 3 CV reviews per day , meaning only 3 endpoints calls per username daily.

    """
    # Log message
    print(str(question))

    # get user id
    user_id = f"{username}"
    user_text = f"{question}"

    update_user_data(user_id, "user", user_text)

    user_messages = get_user_data(user_id)

    # Prompt ChatGPT
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=user_messages
    )

    response_text = response.choices[0].message["content"]

    update_user_data(user_id, "assistant", f"{response_text}")

    return response_text
