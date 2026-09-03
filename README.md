Neo4j Practice & Basics

A lightweight repository for learning Neo4j graph database fundamentals and Cypher Query Language (CQL) using mock data.

Features
Graph Modeling: Nodes, relationships, properties, and labels.

Data Seeding: Mock dataset setup for testing queries.

Cypher Operations: Basic CRUD, pattern matching, and graph traversals.

Data Model
Nodes: :Person (name, age), :Product (name, category)

Relationships: :FRIENDS_WITH, :PURCHASED, :WORKS_AT


Sample Queries
Insert Sample Data:

Cypher
CREATE (a:Person {name: 'Alice', age: 28}),
       (b:Person {name: 'Bob', age: 32}),
       (a)-[:FRIENDS_WITH]->(b);
Find Friends of Friends:

Cypher
MATCH (p:Person {name: 'Alice'})-[:FRIENDS_WITH*2]-(fof:Person)
WHERE p <> fof
RETURN DISTINCT fof.name;
Clear Database:

Cypher
MATCH (n) DETACH DELETE n;
