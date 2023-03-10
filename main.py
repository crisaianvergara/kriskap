from kriskap import create_app, db

app = create_app()

if __name__ == "__main__":  # Start the web server
    db.create_all()  # Create all tables from models
    app.run(debug=True)  # Run python main.py
