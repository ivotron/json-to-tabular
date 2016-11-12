FROM ivotron/jq

RUN apk --no-cache add python

ADD . /root/

ENTRYPOINT ["/root/to_csv.py"]
