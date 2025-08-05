FROM sphinxdoc/sphinx

WORKDIR /docs
ADD requirements.txt /docs

RUN apt-get update && apt-get install -y git
RUN pip3 install -r requirements.txt
