import subprocess
import networkx as nx

def explore_wiki(url: str, graph: nx.Graph):
    url = f"https://en.wikipedia.org{url}"

    print( "\n\n------------------------------------------------------------------------------")
    print(f"----- EXPLORING {url} -----")
    print("------------------------------------------------------------------------------")

    command = f"curl -s \'{url}\' | htmlq a | grep -o \'href=\"/wiki/[^\"]*\' | sed \'s/href=\"//g\'"
    new_urls = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)

    # Checking if command was sucessful
    if new_urls.returncode != 0:
        print(f"Error finding new_urls in {url}")
        return

    if url in list(graph.nodes):
        print(f"Skipping this url: {url}")
        return

    #  current_url_node = node(url, )
    graph.add_node(url)

    for i in new_urls.stdout.split("\n"):
        print(i)

    for i in new_urls.stdout.split("\n"):
        explore_wiki(i, graph)


def main():
    starting_url="/wiki/B_(programming_language)"

    wikis_graph = nx.Graph()

    wikis_graph.add_node(starting_url, valid=False, visited=True)
    wikis_graph.add_node("four", valid=False, visited=True)
    wikis_graph.add_node("one", valid=False, visited=True)

    wikis_graph.add_edge(starting_url, "four")
    wikis_graph.add_edge(starting_url, "one")
    #
    #  print(wikis_graph.nodes)
    #  print(wikis_graph.edges)

    for i in wikis_graph.nodes.data():
        #  print(i)
        if i[1]['visited'] == True:
            print("d")

    if wikis_graph.nodes[starting_url]["visited"]:
        print("skipping...")

    try:

        if wikis_graph.nodes["dic"]["visited"]:
            print("skipping...")
    except KeyError:
        print("not in graph")
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

main()
