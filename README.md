# Interruption Parser

Interruption Parser is a microservice that allows one to get data out of `KPLC` planned power outtage announcement pdfs.

## How it works
The project uses `pdfminer.six` to get the text in a pdf document. The text is then parsed to get the relevant information about the planned blackouts.


## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed `Python3` and `Pipenv`.
* You have a `Unix` or `Windows` machine.

## Installing interruption_parser

To install `interruption_parser`, follow these steps:

Linux and macOS and Windows:

1. `git clone https://github.com/LittleKidogo/interruption_parser`
2. `cd interruption_parser`
3. `pipenv install`


## Using interruption_parser

To use interruption_parser, follow these steps:

1. `pipenv shell`
2. `python manage.py run`


To try it:

### Using curl

```curl --header "Content-Type: application/json" \
  --request POST \
    --data '{"document_link":"xyz","callback_url":"http://localhost:2300"}' \
      http://localhost:5000/
```
You should get the response
```{
    "error": null,
  "status": "Ok"
  }
```

After a while you should get a request on the supplied callback url of the parsed data.

## Contributing to interrupt_parser
To contribute to interrupt_parser, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin interrupt_parser/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
