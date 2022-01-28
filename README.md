# Dashboards
Creating many dashboards using flask for various projects

## Application Tracker
Creating a Python project to facilitate the tracking of applications in a shift away from Excel

### Motivations
Following my recruitment for Summer '22 during the Fall of 2021 (my junior year), I wanted to gain additional insight and clarity into the recruiting progress as well as gain experience with a large (r than leetcode) sized Python project.

### Eventual Goals
- [ ] Display information on number of applications, success rate, breakdown of status, etc
- [ ] Ability to find HQ based on company names
- [ ] Include networking information in cover letter
- [ ] Ability to gain insight/data on the progression of applications on a large scale and extract to visualizations

### Tips
- You should create a `.env` file with `SECRET_KEY=your_key_here`
- Passing any arguments to `launch.py` will launch the program in debug mode
- You can utilize flask-migrate through `py -m flask db...`
  - When using Windows Powershell, you must set the environment variable with the following syntax: `$env:FLASK_APP = "launch"`

## Resumes

### This repository is responsible for the creation and updates to my resume and cover letter over the years
