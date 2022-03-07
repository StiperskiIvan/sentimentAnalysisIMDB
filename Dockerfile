# init a base image (Alpine is small Linux distro)
FROM python:3.9-slim-buster
# Step 2: Add requirements.txt file
COPY requirements.txt requirements.txt
# Step 3:  Install required python dependencies from requirements file
RUN pip install -r requirements.txt
RUN pip3 install opencv-python-headless
# define the present working directory
WORKDIR /poslovnaInteligencija
# copy the contents into the working dir
ADD . /poslovnaInteligencija
# Step 6: Expose the port app is running on
EXPOSE 5432
# define the command to start the container
CMD ["python","main.py"]