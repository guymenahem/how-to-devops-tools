#/bin/sh
kubectl patch sts postgres-postgresql --patch-file ./DB-actions/fail-db.yaml
kubectl delete pod postgres-postgresql-0