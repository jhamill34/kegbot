FROM python:2.7
MAINTAINER Joshua Rasmussen <xlr8runner@gmail.com>

ENV PORT 3000
ENV SQL_STRING "postgresql://docker:mysecretpassword@db:5432/kegbot"
EXPOSE 3000

COPY ./ /app

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
