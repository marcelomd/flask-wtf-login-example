#!/usr/bin/env python
# coding: utf-8

def create_db():
    from app import db, create_app
    app = create_app()
    with app.app_context():
        db.create_all()


def main():
    from app import create_app
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
