from flask_migrate import Migrate

from app import create_app, db

app = create_app()
Migrate(app, db)

# from app.base.models import User, ACCESS
# user = User(username='Admin', password='Admin', role=ACCESS['admin'])
# db.session.add(user)
# db.session.commit()

if __name__ == '__main__':
    app.run(debug = True)
