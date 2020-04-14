import requests
import shutil
import tempfile

# This is the image url.
image_url = "https://dl.airtable.com/.attachmentThumbnails/88d659562211e4f363bf2b5b784a8565/d8ecf824"

# Open the url image, set stream to True, this will return the stream content.
resp = requests.get(image_url, stream=True)
resp.raw.decode_content = True

tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
tmp_img_file.write(resp.raw)
tmp_img_file.close()


# Set decode_content value to True, otherwise the downloaded image file's size will be zero.

# Copy the response stream raw data to local image file.
shutil.copyfileobj(resp.raw, local_file)

# Remove the image url response object.
del resp
