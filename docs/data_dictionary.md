| Column Name    | Data Type  | Description                                                    |
|----------------|------------|----------------------------------------------------------------|
| Row ID         | Number     | Sequential number assigned to each row in the dataset          |
| Order ID       | General    | Unique identifier for each order                               |
| Order Date     | Date       | Date when the order was placed                                 |
| Ship Date      | Date       | Date when the order was shipped                                |
| Ship Mode      | Text       | Shipping method used for delivery                              |
| Customer ID    | General    | Unique identifier for each customer                            |
| Customer Name  | General    | Full name of the customer                                      |
| Segment        | General    | Type of customer segment (Consumer, Corporate, Home Office)    |
| Country        | General    | Country where the order was placed                             |
| City           | General    | City where the order was delivered                             |
| State          | General    | State where the order was delivered                            |
| Postal Code    | Text       | ZIP/Postal code of delivery location                           |
| Region         | General    | Geographic region of the sale (West, East, Central, South)     |
| Product ID     | Text       | Unique identifier for each product                             |
| Category       | General    | Main product category (Furniture, Office Supplies, Technology) |
| Sub-Category   | General    | Detailed product subcategory                                   |
| Product Name   | General    | Full name/description of the product                           |
| Sales          | Currency   | Revenue generated from the order in dollars                    |
| Quantity       | Number     | Number of units ordered                                        |
| Discount       | Percentage | Discount percentage applied to the order (0% to 100%)          |
| Profit         | Currency   | Profit earned from the order (can be negative for losses)      |

What is the earliest date and latest date in the Order Date column? (This tells you the time range).
Answer: 1/3/2014 the earliest , 12/30/2017

Look at the Profit column. Are there negative numbers? (This tells you some orders lost money).
Answer: yes there is approximately 1800-1900 rows with negative values

How many unique Regions are there? (Central, East, etc.?)
Answer: 4 unique columns 


The "Granularity" Check: Look at your Order IDs. Do you see the same Order ID appearing on multiple rows? (This tells us if one "Order" can contain multiple different "Products").
Answer: Yes, there is duplicates

Profitability Driver: Quickly scan a few of those negative profit rows. Do they have high Discounts? (e.g., is there a 50% or 80% discount on those losing rows?)
Answer: yes, it ranges from 40-80%

Top Category: Just by scrolling, which Category seems to appear most often?
Answer: Office supplies, 6026



What does “profit” represent in this dataset?
Answer: Profit represents the net earnings from each order after deducting costs and discounts from the sales revenue. It can be negative when an order results in a loss (costs exceed revenue).

Are discounts applied per item or per order?
Answer: Discounts are applied per order. Each row represents a single order, and the discount percentage shown applies to the entire order regardless of quantity.

What time range does the data cover?
Answer: The data covers orders from January 3, 2014 to December 30, 2017, spanning approximately 4 years.

What are the main business dimensions?
(examples: time, region, category, segment)

Answer: The main business dimensions are:
1. Time - Order Date and Ship Date (when orders occurred)
2. Geography - Region, State, City (where orders came from)
3. Product - Category, Sub-Category, Product Name (what was sold)
4. Customer - Segment (who bought: Consumer, Corporate, Home Office)
5. Operations - Ship Mode (how orders were delivered)