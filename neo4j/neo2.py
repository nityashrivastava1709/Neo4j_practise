import json
from neo4j import GraphDatabase

with open("companies.json", "r") as file:
    companies = json.load(file)

print(type(companies))
print(len(companies))
print(companies[0])

URI = "neo4j+s://ae7752a3.databases.neo4j.io"
USERNAME = "ae7752a3"
PASSWORD = "UVQUIExYh9C4NfKKs-OM_IzgALyC42IAftgK31SjxqI"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

print("Connected to Neo4j")
def create_company(tx, company):
    query = """
    MERGE (c:Company {name: $name})
    SET c.revenue = $revenue

    WITH c, $acquisitions AS acquisitions

    UNWIND acquisitions AS acquisition

    MERGE (a:Company {name: acquisition.name})
    MERGE (c)-[r:ACQUIRED]->(a)
    SET r.year = acquisition.year
    """

    tx.run(
        query,
        name=company["name"],
        revenue=company["revenue"],
        acquisitions=company["acquisitions"]
    )

for company in companies:
    with driver.session() as session:
        session.execute_write(create_company, company)

with open("people.json", "r") as file:
    people = json.load(file)


print(type(people))
print(len(people))
print(people[0])

def create_person(tx, person):
    query = """
    MERGE (p:Person {name: $name})
    SET p.role = $role

    MERGE (c:Company {name: $company})

    MERGE (p)-[:WORKS_AT]->(c)
    """

    tx.run(
        query,
        name=person["name"],
        role=person["role"],
        company=person["company"]
    )

for person in people:
    with driver.session() as session:
        session.execute_write(create_person, person)