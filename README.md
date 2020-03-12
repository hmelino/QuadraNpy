# QuadraNpy




QuadraNpy is module to process "Payment Data" and "Sales Detailed " .csv reports from qls.quadranet website and creates graph with searched items.

  - Search for items sales in specified time period
  - Plot a graph using matplotlib

### Tech

QuadraNpy uses a number of open source projects to work properly:

* [matplotlib](https://pypi.org/project/matplotlib/) - Python plotting package
* [requests](https://pypi.org/project/requests2/) - Python HTTP for Humans

### How to use

QuadraNpy requires 'PaymentData.csv' and 'SalesDetailed.csv' from same time period (month/week/year ...)

The newest version of QuadraNpy can automaticly detect type of report, so they can be bulk imported from folder, instead of importing them one by one.

```sh
$ import QuadraNpy.main import Sales
$ yearlyReport = Sales()
$ yearlyReport.loadFolder('D:\Reports')
$ yearlyReport.findTotal('Cappucino')
```