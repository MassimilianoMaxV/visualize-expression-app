import streamlit as st
import networkx as nx
from pyvis.network import Network
import re
import os

# Function to parse and build a graph from the logical expression
def build_logical_graph(expression, graph=None, parent=None, edge_label=""):
    if graph is None:
        graph = nx.DiGraph()

    # Regular expressions to split by operators
    expression = expression.strip()
    
    # Handle NOT (~)
    if expression.startswith("~"):
        operand = expression[1:].strip()
        graph.add_node(operand, label=operand, color="lightblue", shape="circle")
        graph.add_node('NOT', label='NOT', color="red", shape="box")
        graph.add_edge('NOT', operand, label="NOT")
        return graph

    # Handle AND (&) and OR (|)
    if '&' in expression or '|' in expression:
        # Split the expression into components by logical operators
        sub_expressions = re.split(r"(&|\|)", expression)
        
        operator = None
        for part in sub_expressions:
            part = part.strip()
            if part == '&':
                operator = 'AND'
                graph.add_node(operator, label=operator, color="green", shape="box")
            elif part == '|':
                operator = 'OR'
                graph.add_node(operator, label=operator, color="orange", shape="box")
            else:
                graph.add_node(part, label=part, color="lightblue", shape="circle")
                if parent:
                    graph.add_edge(parent, part, label=edge_label)
                if operator:
                    graph.add_edge(operator, part, label=edge_label)

        return graph

    # Handle nested parentheses by recursion
    if '(' in expression:
        # Remove outermost parentheses
        inner_expr = expression[1:-1].strip()
        return build_logical_graph(inner_expr, graph, parent, edge_label)

    # Otherwise, treat the expression as a variable
    graph.add_node(expression, label=expression, color="lightblue", shape="circle")
    if parent:
        graph.add_edge(parent, expression, label=edge_label)

    return graph

# Function to visualize the graph using pyvis
def visualize_graph(graph):
    net = Network(notebook=False, width="100%", height="500px")
    
    # Customize the appearance of nodes and edges in the network
    for node in graph.nodes(data=True):
        net.add_node(node[0], label=node[1]['label'], color=node[1]['color'], shape=node[1]['shape'])
    
    for edge in graph.edges(data=True):
        net.add_edge(edge[0], edge[1], label=edge[2].get('label', ""))

    # Save and display the graph
    path = "./graph.html"
    net.write_html(path)  # Use write_html instead of show to generate the HTML file
    
    return path

# Streamlit app
def main():
    st.title("Logical Expression Visualizer")
    st.write("Paste a logical expression below, and it will be visualized as a network graph.")
    
    # Input field for the logical expression
    expr_input = st.text_area("Enter logical expression:", value="""
        ~draft
        & (
            (private_user & suspicious_word_taxidermie & ~whitelist_taxidermie)
            |
            (category_pets & suspicious_don_organe)
            |
            (category_pet_accessories & suspicious_pets_products & ~whitelist_pets_products)
            |
            (in_categories_ivoire & suspicious_words_ivoire_nt & suspicious_word_ivoire_pw 
             & suspicious_word_tortue & suspicious_word_corne & suspicious_word_defense 
             & suspicious_word_dent & suspicious_word_griffe & suspicious_word_poil 
             & suspicious_word_queue & ~whitelist_words_ivoire)
        )
    """)

    # Button to visualize
    if st.button("Visualize"):
        # Build the graph
        graph = build_logical_graph(expr_input.strip())
        
        # Visualize the graph and show the output in Streamlit
        html_path = visualize_graph(graph)
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=600)

if __name__ == '__main__':
    main()
