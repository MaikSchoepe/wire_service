# wire_service

strawberry export-schema wire_service.app:schema > schema.graphql
python3 -m sgqlc.introspection --exclude-deprecated --exclude-description http://127.0.0.1:5000/graphql schema.json
