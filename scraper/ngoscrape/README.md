# Web  Crawler Scraper

## Scrapes `https://ngosindia.org/#`

This is an  example  of a web scraper using the  `scrapy` python framework.

## Requirements

* scrapy (`pip install scrapy`)

* twisted (`pip install --upgrade twisted`)

* pandas


###Usage

Run the following:

```python
cd ngoscrape
scrapy crawl ngos -o ngo.json
```

This  will run the python crawler(takes about 5-10 minutes to finish running) into a file called `ngo.json`, scraping ngo info at a state  level.

Further work can  be done to include a district, city, town,  village column. 



## Pipeline

After the `ngo.json` is created, this file can then  be read into a jupyter notebook for any  kind of processing, from classic data science cleaning, EDA, and data analysis, to uploading this  data into a database. 

See  `pipeline/After_Scraper_Processing.ipynb`


## References

*  https://www.youtube.com/watch?v=ALizgnSFTwQ&ab_channel=TraversyMedia



