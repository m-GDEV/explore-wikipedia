import subprocess
import networkx as nx
import matplotlib.pyplot as plt

def explore_wiki(url: str, graph: nx.Graph, depth: int):
    if depth > 20:
        print("This was called 20 times recursively, ending...")
        raise Exception("Depth limit reached")


    prefix = "https://en.wikipedia.org"
    url = f"{prefix}{url}"
    
    try: 
        if graph.nodes[url]["visited"]:
            print(f"Already Explored: {url} - Skipping...")
            return
        elif not graph.nodes[url]["valid"]:
            print(f"Already attempted exploration of {url}, not valid - Skipping...")
            return
    except:
        graph.add_node(url, valid=True, visited=True)
            

    print( "\n\n------------------------------------------------------------------------------")
    print(f"----- EXPLORING {url} -----")
    print("------------------------------------------------------------------------------")
    
    # Extract all inter-wikipedia urls from page
    command = f"curl -s \'{url}\' | htmlq a | grep -o \'href=\"/wiki/[^\"]*\' | sed \'s/href=\"//g\'"
    new_urls = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)

    # Checking if command was sucessful
    if new_urls.returncode != 0:
        print(f"Error finding new_urls in {url}")
        # Not super important since we're not gonna come back to this anyways
        graph.nodes[url]["valid"] = False 
        return
    # Exploration was sucessful
    else:
        graph.nodes[url]["visited"] = True
        graph.nodes[url]["valid"] = True
    
    # Doing stuff with new_urls in graph 
    # 1. Add edges from url to all items in new_urls
    # 2. If graph[new_urls[i]] exists and valid and not visited explore it 
    # 3. If graph[new_urls[i]] does not exist, make a new node and mark it valid and not visited and explore it 
    for i in new_urls.stdout.split("\n"):
        # No logic checking node since explore_wiki should do it above
        explore_wiki(i, graph, depth + 1)
        graph.add_edge(url, i)


def main():

    starting_url="/wiki/B_(programming_language)"

    wikis_graph = nx.Graph()
    
    try:
        explore_wiki(starting_url, wikis_graph, 1)
    except Exception:
        print(wikis_graph)
        nx.draw(wikis_graph)
        plt.show()

    #  wikis_graph.add_node(starting_url, valid=False, visited=True)
    #  wikis_graph.add_node("four", valid=False, visited=True)
    #  wikis_graph.add_node("one", valid=False, visited=True)
    #
    #  wikis_graph.add_edge(starting_url, "four")
    #  wikis_graph.add_edge(starting_url, "one")
    #
    #  if wikis_graph.nodes[starting_url]:
    #      print("not adding node again")
    #  else:
    #      wikis_graph.add_node(starting_url, valid=True, visited=True)
    #
    #  #
    #  #  print(wikis_graph.nodes)
    #  #  print(wikis_graph.edges)
    #
    #  for i in wikis_graph.nodes.data():
    #      #  print(i)
    #      if i[1]['visited'] == True:
    #          print(f"{i} is visisted")
    #
    #  print("BREAK")
    #
    #  try:
    #      if wikis_graph.nodes[starting_url]:
    #          print("here")
    #          wikis_graph.nodes[starting_url]["visited"] = True
    #  except KeyError:
    #      print("not in graph")
    #
    #  for i in wikis_graph.nodes.data():
    #      #  print(i)
    #      if i[1]['visited'] == True:
    #          print(f"{i} is visisted")

    #  if wikis_graph.nodes.get(starting_url) != None:
    #      if wikis_graph.nodes.get(starting_url)['visited'] == True:

    #      print("skipping...")

    #  new_node = wikiNode(starting_url, False, False)
    #  nn = wikiNode("dick", True, True)
    #  print(new_node)
    #
    #  wikis_graph.add_node(new_node)
    #  new_node.url = "four"
    #  print(wikis_graph.nodes.get(new_node))
    #  wikis_graph.add_node(nn)
    #
    #  wikis_graph.add_edge(new_node,nn)
    #  print(wikis_graph.edges.get(new_node.url))

    #  print(wikis_graph.nodes.data())
    #  print(wikis_graph.edges.data())
    #  print(*wikis_graph.nodes.get(nn))
    #  print(wikis_graph.nodes.get(new_node))
    #  #
    #  for i in list(wikis_graph.nodes):
    #  print(i)
    #
    #  for i in list(wikis_graph.edges):
    #      print(*i)
    #

    #  if

    #  explore_wiki(starting_url, wikis_graph)

if __name__ == "__main__": 
    main()
