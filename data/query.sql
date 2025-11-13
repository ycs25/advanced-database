.timer on

.output results.txt
.header on

SELECT Invoice.InvoiceId, Invoice.CustomerId, Customer.Country, Track.Name as TrackName, Track.GenreId
FROM Invoice
INNER JOIN Customer
ON Invoice.CustomerId = Customer.CustomerId
INNER JOIN InvoiceLine
ON Invoice.InvoiceId = InvoiceLine.InvoiceId
INNER JOIN Track
ON InvoiceLine.TrackId = Track.TrackId;

.output stdout
.header off