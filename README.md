# Optical Character Recognition API
This app was developped other the course of a few days as a technical test for an intership interview. Happy reading !

## Running the app

### Base

To start, go to the git and clone, or download a zipfile and unzip it at
https://github.com/Serfcxd/OCR_API_Python

Open a terminal in the OCR_API_Python folder, or with an app like codium, then run

~ sh ./init.sh

In order to create a virtual environnement and download the necessery python packages.
To use the app (without telemetry), run

~ sh ./runBase.sh

You can now go to the following localhost webpage and use the app :
http://127.0.0.1:8000/

To stop the application, do ctrl+C.
You can deactivate the virtual environnement with 

~ sh ./deactivate.sh

### Telemetry

To use the telemetry functionnality, you must stop running fastapi, and run (once is enought)

~ sh ./telemetryInit.sh

Then you can open a second terminal (same folder) and run

~ sh ./runDocker.sh

while it is running go back to the first terminal and run

~ sh ./runDocker.sh

You can now open 2 browser tabs, one for telemetry and the other for the app (same address for the later)

Once you have used the app at least once (upload), you can go to
http://localhost:16686/
and select the ocr-api service (if it doesn't appear, try using the app to download a file. Don't worry, it will be visible as well)
You can select an operation and see telemetry data, for example a POST can be expended to reveal the ocr-api text field, whose tags contain a text.value of the text returned by the operation.  
The selected name is the one designated by "--service_name ocr-api" and you can change it at your convenience

WARNING : If you are using Firefox, a bug with the jeager version in the docker image will make it hard to read;
referenced at https://github.com/jaegertracing/jaeger-ui/issues/3203,
Use a different browser to avoid this issue.

## Testing

### Test data
Uses the base data from the pytesseract github repo, and additionnal images

New tests include:
- test2.png doesn't read character '9' on the right-hand side
- birthday.png incorrectly reads at 2 points ('Join ud:\n\n' instead of 'Join us:\n and 'Balhday' instead of 'Birthday')
- Carte visite john doe incorrectly read the mail address (a space and an 'm' is read as 'n')

tesseract has a few spelling issues even in the base tests.

### Your own tests
Please do your own tests as well ! The app has limits, max ... file size and a 10 seconds computation limit.

Those can be changed by opening main.py and changing the variables:
line 9 TIMEOUT (10 by default, can be a float)
line 10 MAXFILESIZE (2 Mo by default, max size of a temporary file, bigger giles are stored in disk)

## Sources

These are some of the sources I used for this project

stop request "GET /favicon.ico HTTP/1.1" : https://stackoverflow.com/questions/1321878/how-to-prevent-favicon-ico-requests

sources for html implementation:
- https://www.reddit.com/r/FastAPI/comments/10vwf58/422_error/ (main solving thread)
css:
- https://www.w3schools.com/css/css_examples.asp
- https://www.reddit.com/r/css/comments/1n83a8o/how_can_i_align_items_within_a_div_to_the_right/?tl=fr
maxfilsize:
- https://www.youtube.com/watch?v=y_JPb8vOh28
during various code versions, the following were used (in order):
- https://fastapi.tiangolo.com/tutorial/request-files/#multiple-file-uploads (several pages from the fastapi doc actually https://fastapi.tiangolo.com/)
- https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi
- https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
- https://api.jquery.com/serialize/ & https://api.jquery.com/jQuery.post/
- https://stackoverflow.com/questions/18169933/submit-form-without-reloading-page
- https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest_API/Using_FormData_Objects
- https://stackoverflow.com/questions/70109999/how-to-get-file-data-from-input-html-element

sources for opentelemetry:
- https://uptrace.dev/guides/opentelemetry-fastapi
- https://www.youtube.com/watch?v=m28TTogdcbk (note : one command in the video is incorrect, following link is how to solve it)
- https://opentelemetry.io/docs/zero-code/python/logs-example/

sources of my attempt at making the app contenerised:
- https://lctoan.medium.com/fastapi-by-a-python-beginner-1-0ebc3892d414
- https://stackoverflow.com/questions/71118438/i-am-to-run-python-fastapi-locally-but-when-trying-to-run-through-container-no
- https://forums.docker.com/*
- https://docs.docker.com/reference/*
- https://doc.ubuntu-fr.org/docker
- https://www.docker.com/blog/how-to-dockerize-your-python-applications/
