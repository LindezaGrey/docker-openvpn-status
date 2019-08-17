FROM python:3.7.0-alpine3.8
WORKDIR /app
RUN pip install docker flask-restful
COPY statusgrabber.py /app
CMD ["python","-u","statusgrabber.py"]
LABEL maintainer="BetrUG"