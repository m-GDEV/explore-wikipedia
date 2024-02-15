import subprocess
import networkx as nx
import matplotlib.pyplot as plt
import time

global global_depth
global_depth = 1

class TerminationException(Exception):
    pass

# With source and target defined it will recursve until depth is reached or if a path is found 
# Without source and target it'll just keep recursing until depth is reached
def explore_wiki(url: str, graph: nx.Graph, depth: int, depth_limit: int, source = None, target = None):
    global global_depth
    if depth > global_depth:
        global_depth = depth

    if depth > depth_limit:
        # Doing this hard limits all other explorations of this depth 
        # Basically, all explorations will end and the main will take over again
        raise TerminationException("Depth Limit Reached")


    prefix = "https://en.wikipedia.org"
    url = f"{prefix}{url}"
    
    try: 
        if graph.nodes[url]["visited"]:
            print(f"Already Explored/Invalid: {url} - Skipping...")
            return
        # Previously non-visited is now visited
        else:
            graph.nodes[url]["visited"] = True
    # Happens if node doesnt exist, should only happen on the first run 
    # when we give a new url. All other urls should have nodes because we make them
    except:
        graph.add_node(url, visited=True)
            

    print( "\n\n------------------------------------------------------------------------------")
    print(f"----- EXPLORING {url} -----")
    print("------------------------------------------------------------------------------")
    
    # Extract all inter-wikipedia urls from page
    # 1. Get html page 
    # 2. Get all <a> tags 
    # 3. match all <a> tags with href="/wiki*"
    # 4. remove href from links 
    # 5. Only match urls not in the form of /wiki/*:* (this format is used for meta wiki pages)
    # 6 & 7. Sort (because uniq only removes duplicate adjacent lines) and remove duplicates
    # 8. Sleep to not be a dick to wikipedia's servers
    command = f"curl -s '{url}' | htmlq a | grep -o 'href=\"/wiki/[^\"]*' | sed 's/href=\"//g' | ugrep '^/wiki/[\\w_()/\\-\\.]*$' | sort | uniq "
    found_urls = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    time.sleep(0.2)

    # Checking if command was sucessful
    if found_urls.returncode != 0:
        print(f"Error finding new_urls in {url}")
        return
    
    # Get stdout and remove last element as it is just a \n
    new_urls = found_urls.stdout.split("\n")[:-1]
    # Append prefix to each element
    new_urls_prefixed = [prefix + new_url for new_url in new_urls]

    # Adding nodes and edges  
    new_url_count: int = 0
    for i in new_urls_prefixed:
        # Create new node if it doesnt exist
        if graph.nodes.get(i) == None: 
            #  print(f"New url: {i}")
            graph.add_node(i, visited=False)
            new_url_count +=1
    
    # Separate loop so they get printed separately
    new_edge_count = 0
    for i in new_urls_prefixed:
        # Add edge from url to i (i node must (probably) exist)
        # Avoiding adding self-cycles (could happen if page has link to self)
        if not graph.has_edge(url,i) and url != i:
            graph.add_edge(url, i)
            new_edge_count += 1

    # Print info on new nodes and edges 
    print(f"Added {new_url_count} urls and {new_edge_count} edges")
    
    # If we're looking for specifc target url 
    if source and target:
        prefixed_source = f"{prefix}{source}"
        prefixed_target = f"{prefix}{target}"
        
        # Check if path exists, handle different cases when it doesn't
        try:
            path = nx.shortest_path(graph, source=prefixed_source, target=prefixed_target)

            print(f"Found path from {source} to {target}:")
            print(f"{path}\n")
            
            raise TerminationException(f"Path found {global_depth} layers deep")
        except nx.NetworkXNoPath:
            # This should be impossible
            print("No path found between source and taget, continuing")
        except nx.NodeNotFound:
            print("Target has not been discovered yet")


    # Explore the new_urls
    for i in new_urls:
        # No logic checking node since explore_wiki should do it above
        # Just passing along source and target, don't need to check if they exist
        explore_wiki(i, graph, depth + 1, depth_limit, source, target)

# Convert nx graph to a cytoscape compatible format
def nx_graph_to_cytoscape(graph: nx.Graph): 
    # Assume script is run from project root
    with open("./build/converted.js", "w") as f: 
        
        file = "export const elements = [\n"
        for node in graph.nodes:
            file += f"{{ data: {{ id: \"{node}\" }} }},\n"
        
        for edge in graph.edges:
            file += f"{{ data: {{\n\tsource: \"{edge[0]}\",\n\ttarget: \"{edge[1]}\"\n}}}},\n"

        file += "]"

        f.write(file)

def main():

    starting_url="/wiki/B_(programming_language)"
    #  target_url = "/wiki/Windows"
    target_url = "/wiki/ABC_ALGOL"
    #  starting_url = "/wiki/List_of_universities_in_Canada"
    #  target_url = "/wiki/1819"

    wikis_graph = nx.Graph()

    try:
        explore_wiki(url=starting_url, graph=wikis_graph, depth=1, depth_limit=1000, source=starting_url, target=target_url)
    except (TerminationException, KeyboardInterrupt, RecursionError) as e:
        print(repr(e))
        print(wikis_graph)
        nx_graph_to_cytoscape(wikis_graph)
#
        #  nx.draw(wikis_graph, with_labels=True, node_size=200, font_size=12)
        #  plt.show()

        #  nx.write_graphml(G=wikis_graph, path="../../graphs/saved.graphml", prettyprint=True)


if __name__ == "__main__": 
    main()
