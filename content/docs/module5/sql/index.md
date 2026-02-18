---
title: "Les bases de données relationnelles et SQL"
weight: 20
---

# Les bases de données relationnelles et SQL

Test :

{{< sql >}}
CREATE TABLE etudiants (
  id INTEGER PRIMARY KEY,
  nom TEXT,
  age INTEGER
);

INSERT INTO etudiants VALUES (1, 'Alice', 22), (2, 'Bob', 25);
{{< /sql >}}

{{< sql >}}

select * from etudiants;

{{< /sql >}}