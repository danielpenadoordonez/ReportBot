import json
import os

def loadGoals() -> dict:
    goal_List_File = os.path.join("DAL", "Data", "Goals.json")
    with open(goal_List_File, "r") as file:
        return json.load(file)