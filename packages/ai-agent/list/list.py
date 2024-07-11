import openai

def main(event):
      name = event.get("name", "stranger")
      greeting = "Here's a list of " + name + "s!"
      print(greeting)
      return {"body": greeting}