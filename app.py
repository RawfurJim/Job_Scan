from flask import Flask, render_template, request
from src.pipeline.predict_pipeline import PredictPipeline

app = Flask(__name__)

pipeline = PredictPipeline()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_skills', methods=['GET', 'POST'])
def get_skills():
    if request.method == 'POST':
        job_desc = request.form.get('job_desc')
        resume = request.form.get('resume')

        job_desc_skills = pipeline.evaluate_model(job_desc)
        resume_skills = pipeline.evaluate_model(resume)

        job_desc_skills_set = set(job_desc_skills)
        resume_skills_set = set(resume_skills)

        matching_skills = job_desc_skills_set.intersection(resume_skills_set)
        missing_skills = job_desc_skills_set.difference(resume_skills_set)

        matching_hard_skills = [skill for skill in matching_skills if skill[1] == 'Hard_Skills']
        matching_soft_skills = [skill for skill in matching_skills if skill[1] == 'Soft_Skills']

        missing_hard_skills = [skill for skill in missing_skills if skill[1] == 'Hard_Skills']
        missing_soft_skills = [skill for skill in missing_skills if skill[1] == 'Soft_Skills']

        return render_template('get_skills.html', 
                               matching_hard_skills=matching_hard_skills, missing_hard_skills=missing_hard_skills,
                               matching_soft_skills=matching_soft_skills, missing_soft_skills=missing_soft_skills)
    else:
        return render_template('get_skills.html', message="No input given.")


if __name__ == '__main__':
    app.run(debug=True)
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port = int("6000"), debug=True)

# from flask import Flask, render_template, request
# from src.pipeline.predict_pipeline import PredictPipeline

# app = Flask(__name__)

# pipeline = PredictPipeline()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_skills', methods=['GET', 'POST'])

# def get_skills():
#     if request.method == 'POST':
#         job_desc = request.form.get('job_desc')
#         resume = request.form.get('resume')

#         job_desc_skills = pipeline.evaluate_model(job_desc)
#         print(job_desc_skills)
#         job_desc_skills_set = set([skill[0] for skill in job_desc_skills])
        
#         resume_skills = pipeline.evaluate_model(resume)
#         resume_skills_set = set([skill[0] for skill in resume_skills])

#         matching_skills = job_desc_skills_set.intersection(resume_skills_set)
#         missing_skills = job_desc_skills_set.difference(resume_skills_set)

#         return render_template('get_skills.html', matching_skills=matching_skills, missing_skills=missing_skills, job_skills=job_desc_skills_set, resume_skills=resume_skills_set)
#     else:
#         return render_template('get_skills.html', message="No input given.")
# if __name__ == '__main__':
#     app.run(debug=True)