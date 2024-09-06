from app import create_app

app = create_app()

def main():
  app = create_app()
  app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=True)

if __name__ == '__main__':
  main()