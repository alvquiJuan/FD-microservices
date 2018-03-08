FROM python:3.6
ADD . /microservices
WORKDIR /microservices
RUN pip install -r requirements.txt
RUN pip install scikit-fuzzy
