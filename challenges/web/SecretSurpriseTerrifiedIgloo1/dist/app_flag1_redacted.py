from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    template_string = request.form.get('template', '{{ message }}')
    message = "I wonder where the flag could be located at..."
    flag = "SIG24{REDACTED_FLAG1}"
    
    try:
        template = app.jinja_env.from_string(template_string)
        rendered = template.render(message=message,flag=flag)
        rendered = re.sub(r'\s+', '', rendered)
    except Exception as e:
        rendered = f"Error: {str(e)}"
    
    return render_template('index.html', 
                        template_string=template_string,
                        rendered_result=rendered,
                        message=message,
                        flag=flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
