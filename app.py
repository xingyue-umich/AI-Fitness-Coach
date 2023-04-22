from flask import Flask, request, render_template
import openai

app = Flask(__name__)
openai.api_key = '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'

def create_plan_prompt(goal, days_per_week, hour_per_training, place, weight, age, gender, experience, height):
    prompt = f"Create a weekly workout plan for the person who is {age} years old, {height} feet tall, and weighs {weight} lbs. \
    This person's gender is {gender} and their workout experience level is {experience}. \
    Their primary goal is to {goal}, and they want to work out {days_per_week} days per week,\
        each workout is around {hour_per_training} hours. They usually work out at {place}. Limit the plan to 8 actitivies per day."
    return prompt


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/plan', methods=['POST'])
def plan():
    goal = request.form['goal']
    age = request.form['age']
    gender = request.form['gender']
    weight = request.form['weight']
    height = request.form['height']
    experience = request.form['experience']
    days_per_week = request.form['days_per_week']
    hours_per_training = request.form['hours_per_training']
    place = request.form['place']

    prompt = create_plan_prompt(goal, days_per_week, hours_per_training, place, weight, height, age, gender, experience)

    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=512,
            temperature=0.7
        )
        plan = response.choices[0].text.split("\n")
        plan_dict = {}

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            plan_dict[day] = []

        current_day = ''
        for line in plan:
            line = line.strip()
            if line.startswith(('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')):
                current_day = line
            elif line != "":
                plan_dict[current_day].append(line)

        for day in days:
            if not plan_dict[day]:
                plan_dict[day].append('Rest day')

    except Exception as e:
        plan_dict = {"Error": str(e)}

    return render_template('plan.html', plan=plan_dict)

if __name__ == '__main__':
    app.run(debug=True)
