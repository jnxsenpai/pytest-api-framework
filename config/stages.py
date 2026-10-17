import os

stages = {
    "dev": "https://aqa-proka4.org/sandbox"
}

def get_stage():
    stage_key = os.getenv("STAGE")
    return stages[stage_key]