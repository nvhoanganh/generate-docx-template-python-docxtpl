# Generate WORD document from template file using https://github.com/elapouya/python-docx-template

## Set up

-   clone the solution
-   Inside the root folder, create new Python env: `python -m venv .venv`
-   In VScode, select the newly created Python env using `Python: Select Interpreter` option
-   Start new terminal session (using the newly created env)
-   Install dependencies: `pip install -r requirements.txt`
-   modify the data in the `context` property
-   run `python main.py`
-   open the `output.docx` file in the output folder

## Deploy to Gcloud

-   install `gcloud` tools https://cloud.google.com/sdk/docs
-   `gcloud init` and select existing project or create new one (login required)
-   `gcloud functions list` to show the list of functions
-   `gcloud functions deploy multipart --runtime python37 --trigger-http --allow-unauthenticated --set-env-vars SENDGRID_API_KEY=bar` to deploy the simple test function
-   `gcloud functions describe airtable2docx` -> get the deployed URL
-   `gcloud functions logs read airtable2docx`
