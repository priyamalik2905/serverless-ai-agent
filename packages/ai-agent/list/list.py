import openai
from flask_assistants import FlaskAssistants

def main(args):
      name = args.get("name", "stranger")
      greeting = "Here's a list of " + name + "s!"
      print(greeting)
      return {"body": greeting}