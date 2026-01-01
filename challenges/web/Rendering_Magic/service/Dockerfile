FROM python:3.11-slim

# set work directory
WORKDIR /app

# copy your flask app
COPY . /app

# create a flag file in the container root
RUN echo "SPARK{sSt1_1nJeCTED_w00Hoo_e4Sy}" > flag.txt

# install flask (jinja2 comes with it)
RUN pip install flask

# for reproducibility, don't expose gunicorn etc.
EXPOSE 2509


CMD ["python", "rendering_magic.py"]
