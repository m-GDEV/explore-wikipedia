Steps in explore_wiki():

-   Get new url in parameter
    -   if this url is already visited skip it
-   Make new node and mark it visited
-   Get urls this url is connected to
    -   if this url is invalid skip it (its already marked visited)
-   For every url this node is connected to, make a node and mark it not visited
-   For every url this node is connected to, add an edge from that url to the current url
-   Explore each url
