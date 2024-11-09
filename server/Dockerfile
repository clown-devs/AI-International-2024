FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /AI-International-2024

RUN pip install --upgrade pip
COPY ./requirements.txt /AI-International-2024/
# COPY ./backend/.env /AI-International-2024/backend/
# COPY ./ai/.env /AI-International-2024/ai/
RUN pip install -r requirements.txt
COPY . .

EXPOSE 85