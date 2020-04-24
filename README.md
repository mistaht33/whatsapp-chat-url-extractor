# WhatsApp-Chat URL Extractor
Simple Script to Read WhatsApp Chat History and extract URL's which have been shared. Project came about from  chat with fellow Developers in WhatsApp group.

## How It Works
### Pre-requisites
The Script Was Created using Python 3.7. To install the dependencies using `pip` run:
```
pip install -r requirements.txt
```
Once the requirements have been installed, check that the `cwd` variable in the script `whatsapp_url_extractor` is the folder with the WhatsApp exported file.
```python
cwd = '/Users/aibakitembo/Desktop/Private/WhatsApp Hackathon'
```
Also change the `file_name` variable to match your WhatsApp exported filename as below:
```python
file_name = cwd + '/WhatsApp Chat with The Devs from Z.txt'
```

## Execution
Run the script:
```
python3 whatsapp_url_extractor
```

## TODO:

- Add Visualizations and check URL's shared per person
- Automatically scrape the WhatsApp Chat Files using Selenium or another way to get files
- Add Support ot Export to EverNote and Other Web Browsers

