FROM wlads/opencv3-contrib-python

# Add requirements.txt
ADD requirements.txt /src/requirements.txt

# Install app requirements
RUN apt-get update && apt-get install -y libav-tools
RUN cd /src; pip install -r requirements.txt

# Bundle app source
COPY ./src /src

# Set working directory, default is '/'
WORKDIR /src

# Expose
EXPOSE  5050


# Run
CMD ["python", "/src/app.py"]

