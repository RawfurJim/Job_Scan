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
        job_desc_skills_set = set([skill[0] for skill in job_desc_skills])
        
        resume_skills = pipeline.evaluate_model(resume)
        resume_skills_set = set([skill[0] for skill in resume_skills])

        matching_skills = job_desc_skills_set.intersection(resume_skills_set)
        missing_skills = job_desc_skills_set.difference(resume_skills_set)

        return render_template('get_skills.html', matching_skills=matching_skills, missing_skills=missing_skills, job_skills=job_desc_skills_set, resume_skills=resume_skills_set)
    else:
        return render_template('get_skills.html', message="No input given.")
if __name__ == '__main__':
    app.run(debug=True)