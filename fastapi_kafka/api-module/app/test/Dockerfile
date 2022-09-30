FROM python:3.9

ENV CUDA_DEVICE 0

WORKDIR /app

RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY ./test.py ./

CMD ["python", "./test.py"]