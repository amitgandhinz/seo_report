## SEO Report ##
FROM ubuntu:16.04
MAINTAINER Amit Gandhi <amit@drawbuildplay.com>

RUN apt-get -qq update && apt-get -qq upgrade && apt-get install -qqy \
    git-core \
    python-dev \
    python-pip \
    python-setuptools

VOLUME /home/seoreport

# Upgrade pip prior to installing python dependencies
RUN pip install -U pip

# Install python requirements
ADD ./requirements.txt /home/requirements.txt
RUN pip install --upgrade -r /home/requirements.txt

# Create log & pid directories
RUN mkdir -p /var/log/seoreport
RUN mkdir -p /var/run/seoreport
RUN chmod -R +w /var/log/seoreport
RUN chmod -R +w /var/run/seoreport

# Add all code
ADD . /home/seoreport
RUN pip install -e /home/seoreport/.

# Enter container
CMD [seo_report, -d, 'https://www.drawbuildplay.com']