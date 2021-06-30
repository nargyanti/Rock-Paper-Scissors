## **HOW TO USE**

1. You must download python and install it in your text editor / IDE.
2. Open the folder (workspace) with your text editor / IDE.
3. Open terminal.
4. Type: 

        py -3 -m venv venv
5. Then copy all of folder and file in this folder (exclude README.md, .gitignore, and .git).
6. Create folder `uploads` in static folder.
7. Type this again in terminal: 

        cd venv
        Scripts\activate
        python.exe -m pip install --upgrade pip
        pip install flask
        pip install keras
        pip install tensorflow
        pip install Pillow
        pip install random2
        pip install flask_bootstrap
8. Then run the project with type this in terminal:
   
        flask run