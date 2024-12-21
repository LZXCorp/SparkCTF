from flask import Flask, render_template, request
import re
from functools import wraps

app = Flask(__name__)

app.config['FLAG'] = "SIG24{REDACTED_FLAG2}"

def security_filter(value):
    """The blacklist of doom lol"""
    blacklist = [
        r'.*settings.*',
        r'.*config.*',
        r'.*import.*',
        r'.*os.*',
        r'.*system.*',
        r'.*popen.*',
        r'.*subprocess.*',
        r'.*file.*',
        r'.*open.*',
        r'.*eval.*',
        r'.*exec.*',
        r'.*getattr.*',
        r'.*setattr.*',
        r'.*delattr.*',
        r'.*locals.*',
        r'.*dir.*',
        r'.*vars.*',
    ]
    
    value_str = str(value).lower()
    for pattern in blacklist:
        if re.search(pattern, value_str, re.IGNORECASE):
            return "Blocked by security filter!"
    
    return value

@app.route('/', methods=['GET', 'POST'])
def index():
    template_string = request.form.get('template', '{{ message }}')
    message = "I wonder where the flag could be located at..."
    flag = "SIG24{REDACTED_FLAG1}"
    
    # Apply security filter before rendering
    if security_filter(template_string) == "Blocked by security filter!":
        rendered = "Blocked by security filter!"
    else:
        try:
            template = app.jinja_env.from_string(template_string)
            rendered = template.render(message=message,flag=flag)
            rendered = re.sub(r'\s+', '', rendered)
            
            # Replaces the flag with nothing
            rendered = rendered.replace(app.config['FLAG'], "")
        except Exception as e:
            rendered = f"Error: {str(e)}"
    
    return render_template('index.html', 
                         template_string=template_string,
                         rendered_result=rendered,
                         message=message,
                         flag=flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
