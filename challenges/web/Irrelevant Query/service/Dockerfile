FROM node:20-slim

WORKDIR /app
RUN npm install express
COPY . .

EXPOSE 6721

CMD ["node", "app.js"]
