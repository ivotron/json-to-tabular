FROM ivotron/jq

RUN apk --no-cache add python py-yaml

ADD . /root/

WORKDIR /data

ENTRYPOINT ["/root/to_csv.py"]
