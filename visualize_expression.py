import streamlit as st
import sympy as sp
import networkx as nx
from pyvis.network import Network
import os

# Helper function to break down an expression
def parse_expression(expr_str):
    try:
        # Use sympy to parse and simplify the expression
        expr = sp.sympify(expr_str)
        return expr
    except (sp.SympifyError, TypeError):
        st.error("Invalid expression. Please check your syntax.")
        return None

# Function to build a graph from the expression
def build_graph(expr, graph=None, parent=None, edge_label=""):
    if graph is None:
        graph = nx.DiGraph()
    
    if isinstance(expr, sp.Symbol):
        graph.add_node(str(expr))
        if parent:
            graph.add_edge(parent, str(expr), label=edge_label)
    elif isinstance(expr, sp.Number):
        graph.add_node(str(expr))
        if parent:
            graph.add_edge(parent, str(expr), label=edge_label)
    elif isinstance(expr, sp.Basic):
        operator = type(expr).__name__
        graph.add_node(operator)
        if parent:
            graph.add_edge(parent, operator, label=edge_label)
        
        for i, arg in enumerate(expr.args):
            build_graph(arg, graph, parent=operator, edge_label=str(i))
    
    return graph

# Function to visualize the graph using pyvis
def visualize_graph(graph):
    net = Network(notebook=False, width="100%", height="500px")
    net.from_nx(graph)
    
    # Save and display the graph
    path = "./graph.html"
    net.show(path)
    
    return path

# Streamlit app
def main():
    st.title("Mathematical Expression Visualizer")
    st.write("Paste a mathematical expression below, and it will be visualized as a network graph.")

    # Input field for the expression
    expr_input = st.text_area("Enter expression (e.g., (a + b) * (c + d) / e):", value="(a + b) * (c + d) / e")
    
    # Button to visualize
    if st.button("Visualize"):
        # Parse the expression
        expr = parse_expression(expr_input)
        
        if expr is not None:
            # Build the graph
            graph = build_graph(expr)
            
            # Visualize the graph and show the output in Streamlit
            html_path = visualize_graph(graph)
            st.write(f"Visualized expression: {expr_input}")
            st.components.v1.html(open(html_path, 'r').read(), height=600)

if __name__ == '__main__':
    main()
