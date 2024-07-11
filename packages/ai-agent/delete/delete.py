import openai

def main(args):
      name = args.get("name", "stranger")
      greeting = "Goodbye " + name + "!"
      print(greeting)
      return {"body": greeting}