FROM selenium/standalone-chrome

# change active user to root
USER root

RUN sudo apt-get -y update
RUN sudo apt-get install -y python3-pip

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

# Install uvicorn
RUN pip install uvicorn[standard]

## Install Chrome browser and ChromeDriver
#RUN apt-get update && apt-get install -y wget unzip libglib2.0-0 libnss3 libx11-6
#RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
#RUN apt-get update && apt-get install -y google-chrome-stable
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
#    unzip /tmp/chromedriver_linux64.zip chromedriver -d /usr/local/bin && \
#    chmod +x chromedriver && \
#    mv chromedriver /usr/local/bin/ && \
#    rm chromedriver_linux64.zip

#
#RUN pip install selenium==3.8.0

COPY ./app /app

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
