#!/bin/bash

set -euo pipefail

set -a
# source .env
set +a

NEO4J_USER="neo4j"
NEO4J_PASS="${NEO4J_PASSWORD}"
GRAPH_NAME="city-road-graph"

echo "Waiting for Neo4j to accept connections..."

until cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASS}" -d system \
    "SHOW DATABASE neo4j YIELD currentStatus WHERE currentStatus = 'online' RETURN 1" \
    | grep -q 1; do
    sleep 2
done

echo "Neo4j is ready."

echo "Checking if graph '${GRAPH_NAME}' exists..."

GRAPH_EXISTS=$(
cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASS}" --format plain <<EOF
CALL gds.graph.exists('${GRAPH_NAME}') YIELD exists RETURN exists;
EOF
)

GRAPH_EXISTS=$(echo "$GRAPH_EXISTS" | tail -n 1 | tr -d '[:space:]')

if [ "$GRAPH_EXISTS" = "true" ]; then
    echo "Graph '${GRAPH_NAME}' already exists. Skipping creation."
    exit 0
fi

echo "Creating graph '${GRAPH_NAME}'..."

cypher-shell -u "${NEO4J_USER}" -p "${NEO4J_PASS}" <<EOF
CALL gds.graph.project(
    '${GRAPH_NAME}',
    'City',
    {
        ROAD_TO: {
            type: 'ROAD_TO',
            orientation: 'UNDIRECTED',
            properties: ['km']
        }
    }
);
EOF

echo "Graph '${GRAPH_NAME}' created successfully."

echo "Post-init completed."
