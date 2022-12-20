
## Setup DB
``` bash
helm repo add bitnami https://charts.bitnami.com/bitnami;
helm install postgres bitnami/postgresql --set auth.postgresPassword=postgres
```

Connect to the DB:
``` bash
kubectl run postgres-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:15.1.0-debian-11-r0 --env="PGPASSWORD=postgres" --command -- psql --host postgres-postgresql -U postgres -d postgres -p 5432
```

Create a Table:
``` bash
CREATE TABLE accounts (
	account_id serial PRIMARY KEY,
	name VARCHAR ( 50 ) UNIQUE NOT NULL,
	owner_email VARCHAR ( 255 ) NOT NULL,
	created_on TIMESTAMP NOT NULL
);
```

Add dummy info:
``` bash
INSERT INTO accounts(name,owner_email,created_on)
VALUES('demo', 'aaa@demo-test.com', CURRENT_DATE);
```
