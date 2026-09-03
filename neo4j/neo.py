from neo4j import GraphDatabase
uri = "neo4j+s://ae7752a3.databases.neo4j.io"
username = "ae7752a3"
password = "UVQUIExYh9C4NfKKs-OM_IzgALyC42IAftgK31SjxqI"

driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)

def create_peopl(name):
    with driver.session() as session:
        session.run(
            "Merge(p:Person{name: $name})",
            name=name
        )


def create_company(name):
    with driver.session() as session:
        session.run(
            "MERGE (c:Company {name: $name})",
            name=name
        )

create_company("Adobe")
create_company("Figma")

def create_relationship(company_a, company_b, year):
    print("Creating relationship...")
    with driver.session() as session:
        session.run(
            """
            MATCH (a:Company {name: $company_a})
            MATCH (b:Company {name: $company_b})
            MERGE (a)-[:ACQUIRED {year: $year}]->(b)
            """,
            company_a=company_a,
            company_b=company_b,
            year=year
        )

create_relationship(
    "Adobe",
    "Figma",
    2022
)

def query_relationships(company_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Company {name: $company_name})-[r]->(b)
            RETURN a, r, b
            """,
            company_name=company_name
        )

        for record in result:
            print(record["a"]["name"])
            print(record["r"].type)
            print(record["r"]["year"])
            print(record["b"]["name"])

query_relationships("Adobe")

# People → Companies

def create_works_at(person, company):
    with driver.session() as session:
        session.run(
            """
            MATCH (p:Person {name: $person})
            MATCH (c:Company {name: $company})
            MERGE (p)-[:WORKS_AT]->(c)
            """,
            person=person,
            company=company
        )


# Company → Company

def create_company_relationship(company_a, company_b, relationship):
    with driver.session() as session:
        session.run(
            """
            MATCH (a:Company {name: $company_a})
            MATCH (b:Company {name: $company_b})
            MERGE (a)-[:COMPETES_WITH]->(b)
            """,
            company_a=company_a,
            company_b=company_b
        )

def people_at_acquired_companies(company_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Company {name: $company_name})
                  -[:ACQUIRED]->
                  (acquired:Company)
                  <-[:WORKS_AT]-
                  (person:Person)
            RETURN person.name AS person,
                   acquired.name AS company
            """,
            company_name=company_name
        )

        for record in result:
            print(
                record["person"],
                "works at",
                record["company"]
            )


create_company("Adobe")
create_company("Figma")
create_company("Microsoft")
create_company("Google")
create_company("Canva")
create_company("Atlassian")

create_people("Shantanu")
create_people("Dylan")
create_people("Satya")
create_people("Sundar")

create_works_at("Shantanu", "Adobe")
create_works_at("Dylan", "Figma")
create_works_at("Satya", "Microsoft")
create_works_at("Sundar", "Google")

create_company_relationship("Microsoft", "Google", "COMPETES_WITH")
create_company_relationship("Canva", "Adobe", "COMPETES_WITH")
create_company_relationship("Atlassian", "Microsoft", "COMPETES_WITH")


