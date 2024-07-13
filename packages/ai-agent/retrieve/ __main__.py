import openai

def main(args):
      name = args.get("name", "stranger")
      greeting = "Here's a " + name + "!"
      print(greeting)
      return {"body": greeting}
