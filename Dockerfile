FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY auth_system/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

# Collect static if needed (disabled by default)
# RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "auth_system.wsgi:application", "--bind", "0.0.0.0:8000"]
