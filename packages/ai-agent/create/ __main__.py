import openai

def main(args):
      name = args.get("name", "stranger")
      greeting = "Hello " + name + "!"
      print(greeting)
      return {"body": greeting}
