# le Dockerfile
FROM python:3.11-slim

WORKDIR /app

# copy all service files
COPY . .

#copy the dist folder into container
COPY dist /app/dist

# install le dependacies 
RUN pip install --no-cache-dir -r requirements.txt

#ENV values
ENV FLAG=SPARK{g0tt4_b3_53cure}
ENV DB_PATH=/app/data/insecure_web.db
ENV SCHEMA_PATH=/app/schema.sql
ENV PORT="8000"

#expose 8000!!!!!
EXPOSE 8000

# run init_db then start the app.py
CMD ["sh", "-c", "python init_db.py && python app.py"]


