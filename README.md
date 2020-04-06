# Scraping-pharmacies
General scrapping web page project to analyze location of pharamcies in Austria


## Information

This project was developed under python 3.6.9 and using a Mac OS 10.15.2(19C5)

##  Motivation

The project itself is not really complicated to code, however, this page was developed no using `id` in the tags, that is why the collection process have to be a mix of `classes`, `xpath`, and find elements by `tag names`, which of course, will make this code harder to sustaing if the tags or their attributes changes. But, I mean, it was made for fun.

## Installation

Clone the repository

```
<>
```

Install dependencies

```
cd <root>
pip install -r requirements.txt
```

Add the driver to the PATH

```
export PATH=$PATH:/opt/WebDriver/bin >> ~/.zshrc
```
