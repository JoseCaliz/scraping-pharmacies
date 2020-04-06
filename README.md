# Scraping-pharmacies
General scrapping web page project to analyze location of pharamcies in Austria


## Information

This project was developed under python 3.6.9 and using a Mac OS 10.15.2(19C5)

##  Motivation

The project itself is not really complicated to code, however, this page was developed no using `id` in the tags, that is why the collection process have to be a mix of `classes`, `xpath`, and find elements by `tag names`, which of course, will make this code harder to sustaing if the tags or their attributes changes. But, I mean, it was made for fun.

## Installation

Clone the repository

```
git clone 
```

Install dependencies

```
cd <root>
pip install -r requirements.txt
```

I have added the webdriver-manager which will handle the process of adding the driver to the path and download the right version, howerver in case you need to use your own driver, I should be added to the path

```
echo "export PATH=\$PATH:<driver_path>" >> ~/.zshr
source  ~/.zshr
```

Run the program

```
python scrapper.py
```

By default it will try to load the saved information and compare if all the links are already in the csv file, if you don't want this validation, feel free to delete `data/results.csv`


