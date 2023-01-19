from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run("localhost") if app.debug else app.run()
