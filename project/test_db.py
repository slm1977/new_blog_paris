from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paris_blog_db.sqlite'
db.init_app(app)

class Page(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    menu_title = db.Column(db.String(1000), unique=True)
    path = db.Column(db.String(1000), unique=True)
    index = db.Column(db.Integer)

    def __repr__(self):
        return "<Page: %s index:%s menu_title:%s filepath:%s>" % (self.id, self.index, self.menu_title, self.path)


@app.route("/")
def get_pages():
    #pages = Page.query.order_by(Page.index).all()
    # ultimo id
    #last_id = Page.query.order_by(Page.id.desc()).first().id
    #print("Numero delle pagine:%s Ultimo id:%s" % (Page.query.count(), last_id))
    #for p in pages:
        print(p)
    # None
    #get_page(33)
    return "ok"

def get_page(page_id):
    page = Page.query.get(page_id)
    print("pagina con id:%s %s" % (page_id, page))

def add_page_to_db(menu_title, index, page_id=None):
    try:
        if page_id==None:
            # create new page with the form data. Hash the password so plaintext version isn't saved.
            new_id = 1 if Page.query.count()==0 else Page.query.order_by(Page.id.desc()).first().id +1
            filename= "%s.html" % new_id
            path = "./project/static/menu_pages/%s" % filename
            new_page = Page(menu_title=menu_title,path=path, index=int(index))

            # add the new page to the database
            db.session.add(new_page)
            db.session.commit()
            return path

    except Exception as ex:
        print("Eccezione nella scrittura della pagina sul db:%s" % ex)
        #raise ex
        return None

    return None

def update_page(page_id, new_path, new_index, new_menu_title):
    if page_id<0:
        return
    page = Page.query.get(page_id)
    page.menu_title = new_menu_title
    page.path = new_path
    page.index = new_index
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)



