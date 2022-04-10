FROM python:3.8
RUN pip install requests
ADD albums.py /
ENTRYPOINT [ "python3", "/albums.py" ]
