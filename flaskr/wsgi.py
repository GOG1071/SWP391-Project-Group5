import app
if __name__ == "__main__":
  app.run("0.0.0.0", port=os.environ["port"], debug=True)