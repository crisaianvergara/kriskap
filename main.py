from kriskap import create_app, db

# Setup
app = create_app()

# Mainline
if __name__ == "__main__":  # Start the web server
    db.create_all()  # Create all tables from models
    app.run(debug=True)  # Run python main.py
