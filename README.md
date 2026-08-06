# GenX-PFAS-Dashboard
GenX Exposure Study Preliminary Dashboard  
Important Notes:
1) First, add the data and demographics files from Google Drive. I would recommend installing the Google Drive app on your laptop and inserting a file path from Google Drive. Eventually, I would recommend changing this to the Google Drive API.
2) Next, do "git clone https://github.ncsu.edu/genx-exposure-study/GenX_Study_Dashboard.git" to obtain all of the Python code from the same repository to be contained in one folder.
3) Each tab has its own Python file. If you are debugging code, you will go to the relevant file to edit.
4) To launch the dashboard locally, add the data files from Google drive, and then write "streamlit run master_file.py" in the terminal.

This is my first time creating a private repository so I may not have set up the file paths correctly. If you encounter errors the first thing I would check is the image file paths and the each dashboard Python file path. 

Future considerations:
1) The dashboard can be deployed using for free in Streamlit's cloud. I would recommend researching more about the [specifics of deployment](https://streamlit.io/security) since I am not as familiar with it.
2) Eventually the plan is for the dashboard to be embedded in the GenX website. Once the dashboard is deployed on Streamlit, there will be a link anyone can access, but I would look into how to add this to a website hosted on Wordpress. 
