# QuadraNpy




QuadraNpy is module to process "Payment Data" and "Sales Detailed " .csv reports from qls.quadranet website and creates graph with searched items.

  - Search for items sales in specified time period
  - Plot a graph using matplotlib

### Tech

QuadraNpy uses a number of open source projects to work properly:

* [matplotlib](https://pypi.org/project/matplotlib/) - Python plotting package
* [requests](https://pypi.org/project/requests2/) - Python HTTP for Humans

### How to use

QuadraNpy requires reports named 'SalesDetailedMMYY.csv' and 'PaymentDataMMYY.csv' , where MMYY are month and year of reports, for example 'SalesDetailed0319.csv' is report from March 2019.

Reports needs to be in folder called 'Reports' inside module.

```sh
$ import QuadraNpy
$ ourVariable= QuadraNpy
$ ourVariable.addSalesNPayments('0319')
$ ourVariable.findTotal('Cappucino')
```


