This data set contains a number of products and real customer search terms from Home Depot's website. The challenge is to predict a relevance score for the provided combinations of search terms and products. To create the ground truth labels, Home Depot has crowdsourced the search/product pairs to multiple human raters.<br>

The relevance is a number between 1 (not relevant) to 3 (highly relevant). For example, a search for "AA battery" would be considered highly relevant to a pack of size AA batteries (relevance = 3), mildly relevant to a cordless drill battery (relevance = 2), and not relevant to a snow shovel (relevance = 1).<br>

Each pair was evaluated by at least three human raters. The provided relevance scores are the average value of the ratings. There are three additional things to know about the ratings:<br>

The specific instructions given to the raters is provided in relevance_instructions.docx.<br>
Raters did not have access to the attributes.<br>
Raters had access to product images, while the competition does not include images.<br>
Your task is to predict the relevance for each pair listed in the test set. Note that the test set contains both seen and unseen search terms.<br>

<h3>File descriptions</h3>

-   train.csv - the training set, contains products, searches, and relevance scores
-   test.csv - the test set, contains products and searches. You must predict the relevance for these pairs.
-   product_descriptions.csv - contains a text description of each product. You may join this table to the training or test set via the product_uid.
-   attributes.csv -  provides extended information about a subset of the products (typically representing detailed technical specifications). Not every product will have attributes.
-   sample_submission.csv - a file showing the correct submission format
-   relevance_instructions.docx - the instructions provided to human raters

Data fields
-   id - a unique Id field which represents a (search_term, product_uid) pair
-   product_uid - an id for the products
-   product_title - the product title
-   product_description - the text description of the product (may contain HTML content)
-   search_term - the search query
-   relevance - the average of the relevance ratings for a given id
-   name - an attribute name
-   value - the attribute's value