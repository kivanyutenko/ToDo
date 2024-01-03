TODO LIST APP

This app allows users to create and update tasks with the option of having, among others, images and tags attached to them. They can be placed into custom folders.

-Requirements

Install python (https://www.python.org/downloads)
Install a code editor (eg. VS Code)
Install a tool to view your database (eg. TablePlus) which will be created after you start using the app.

-Installation and configuration

Download the code
Using your code editor, open the main folder you downloaded. Open the terminal inside the editor and type "python -m venv env" and after its completed, run "pip install -r requirements.txt"
Run "env\Scripts\activate" (on windows machines) and then "uvicorn main:app --reload" in the terminal. 
You will get a link (http://127.0.0.1:8000) and upon clicking, it will take you to app's interface in your browser. From there, you can use and interact with the app.
You can see the database (including your tasks, folders, tags, images etc) with your database tool.

-Features

Create a user with password.
Create, update and delete tasks.
Each task has a title, description, status (new, in progress, done), priority, folder, date, time, image, deadline and flag attributes.
