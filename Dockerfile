FROM tensorflow/tensorflow:latest
RUN pip install --upgrade pip
RUN pip install Pillow
COPY Roboto-Regular.ttf /notebooks/Roboto-Regular.ttf
COPY CaptchaGeneration.ipynb /notebooks/CaptchaGeneration.ipynb