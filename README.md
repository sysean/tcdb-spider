# tcdb-spider

## 1. Introduction
This is a web crawler for www.tcdb.com 

## 2. Technical Detail

There are 3 scripts that handle the entire crawl process:

Select a ball class like Football

Get all the years from this site `https://www.tcdb.com/ViewAll.cfm/sp/Football?MODE=Years`

The program traverses all years, a json file for each year, store the set list for that year in the json file.

This list of json files will be used as a configuration file later in the official crawler