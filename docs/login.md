# Login

We have created a simplistic login system with the ability to change the username later on. The interface is minimalistic so that registration and logging in is easy.

For the login table we use the server-wide SQLite database, which we access using our [Model classes](../SB/models/__init__.py). To add users to the table, we make use of Flask-WTF and WTF-forms.

We have used login and registration forms with included validators.
