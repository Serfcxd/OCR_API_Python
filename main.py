from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from PIL import Image
from starlette.formparsers import MultiPartParser
import pytesseract

from opentelemetry import trace

TIMEOUT = 10 # 10 seconds
MultiPartParser.max_part_size = 2 * 1024 * 1024 # 2 Mo MAXFILESIZE

tracer = trace.get_tracer("ocr.tracer")

app = FastAPI()

def tesseractOCR(image: bytes = File()):
    try:
        outputString = pytesseract.image_to_string( image, timeout=TIMEOUT )
    except:
        return {"error": "error during optic character reading"}
    with tracer.start_as_current_span('text') as textspan:
        if (len(outputString) < 1):
            output = {"text": ""}
        else:
            output = {"text": outputString[:-1]}
        textspan.set_attribute('text.value', output["text"])
        return output

commonHTML = """
    <link rel="icon" href="data:;base64,=">
    <style>
body {
    background-color: #f1e5ce;
}
ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    background-color: #333333;
    display: flex;
}
ul li a {
    display: inline-block;
    color: white;
    padding: 16px 0px 16px 10px;
    font-size: 20px;
    text-decoration: none;
}
h3 {
    color: maroon;
    font-size: 28px;
    margin-left: 40px;
}
form {
    background-color: lightgrey;
    width: 330px;
    padding-top: 6px;
    padding-bottom: 8px;
    text-align: center;
    border: 2px solid black;
    margin: 15px 20px 50px 40px;
}
p {
    background-color: white;
    padding: 10px;
    text-align: left;
    border: 2px solid #025344;
    margin: 40px;
}
    </style>
</head>
<body>
    <ul>
        <li><a href='/'>Home page<a/></li>
        <li><a href='/singleUpload/'>Single Use Page<a/></li>
        <li><a href='/multiUpload/'>Reusable Page<a/></li>
        <li><a href='/docs/'>Docs<a/></li>
    </ul>

"""

formHTML = """
    <form enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    <br>

"""

# app root
@app.get("/")
async def main():
    htmlContent = """
<head>
    <title>OCR API root</title>
    """
    htmlContent += commonHTML + "\t<h3>OCR API Home Page</h3>\n</body>"
    return HTMLResponse(content=htmlContent)

# app one time file upload (must recharge page or go back to previous to try again)
@app.get("/singleUpload/")
async def create_upload_file():
    htmlContent = """
<head>
    <title>OCR API Single Upload</title>
    """
    htmlContent += commonHTML + "\t<h3>OCR API Single Upload</h3>\n" + formHTML + "</body>"
    return HTMLResponse(content=htmlContent)

@app.post("/singleUpload/")
async def read_upload_file(file: UploadFile):
    if not file:
        return {"message": "No file sent"}
    if (file.content_type[0:5] != "image"):
        return {"error": "invalid file type (not an image)"}
    return tesseractOCR(Image.open(file.file))

# app attempt to send back html
@app.get("/multiUpload/")
async def create_upload_file():
    htmlContent = """
<head>
    <title>OCR API Multi Upload</title>
"""
    htmlContent += commonHTML + "\t<h3>OCR API Multi Upload</h3>\n" + formHTML + "</body>"
    return HTMLResponse(content=htmlContent)

@app.post("/multiUpload/")
async def read_upload_file(file: UploadFile):
    if not file:
        return {"message": "No file sent"}
    if (file.content_type[0:5] != "image"):
        return {"error": "invalid file type (not an image)"}
    fileContent = tesseractOCR(Image.open(file.file))
    htmlfileContent = fileContent['text'].replace('\n', '<br>')

    htmlContent = """
<head>
    <title>OCR API Multi Upload</title>
"""
    htmlContent += commonHTML + "\t<h3>OCR API Multi Upload</h3>\n" + formHTML + "<p>"
    htmlContent += htmlfileContent + "\n\t</p>\n</body>"
    return HTMLResponse(content=htmlContent)
