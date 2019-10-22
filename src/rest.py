from appp import create_app

__version__ = "0.1.0"
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
