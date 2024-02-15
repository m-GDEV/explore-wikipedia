## Steps in explore_wiki():

-   Get new url in parameter
    -   if this url is already visited skip it
-   Make new node and mark it visited
-   Get urls this url is connected to
    -   if this url is invalid skip it (its already marked visited)
-   For every url this node is connected to, make a node and mark it not visited
-   For every url this node is connected to, add an edge from that url to the current url
-   Explore each url

## Pipeline plan:

-   Make site with simple, enter url: prompt
-   Explore the url the user entered, updating the number of nodes, edges, and max depth
    -   Do this using a websocket
-   Once python is done finding, navigate to the graph page

## Other (better!) pipeline plan:

-   As we are generating the grpah, continuosly send graph data over a websocket and the frontend should visually update as the graph is populated. would be very cool

## Things to do:

-   Style graph
-   Make proper naming and saving scheme for files
