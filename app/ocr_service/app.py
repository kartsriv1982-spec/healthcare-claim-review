from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

import easyocr
import tempfile

app = FastAPI(
    title="OCR Service"
)

reader = easyocr.Reader(['en'])


@app.get("/health")
def health():

    return {
        "status": "UP"
    }


@app.post("/ocr/extract")
async def extract(
    file: UploadFile = File(...)
):

    with tempfile.NamedTemporaryFile(
        delete=False
    ) as temp_file:

        temp_file.write(
            await file.read()
        )

        temp_path = temp_file.name

    result = reader.readtext(
        temp_path,
        detail=0
    )

    text = "\n".join(result)

    return {
        "status": "SUCCESS",
        "text": text
    }