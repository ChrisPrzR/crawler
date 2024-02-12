# crawler
This project was created to track prices of certain products within Ebay

# Installation
To be able to execute this project, you need to install Python and Scrapy, for more details visit https://docs.scrapy.org/en/latest/intro/install.html

Command to execute the default crawler
`scrapy crawl products`

To filter products by condition add the `-a` flag with the following options:
`products=used` or `products=new`

For example:
`scrapy crawl products -a products=new`

Feel free to reach out if you have any ideas to improve this project.
PRs are welcome, thank you.
