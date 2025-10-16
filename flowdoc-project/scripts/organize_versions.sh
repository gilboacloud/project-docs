#!/bin/bash

# Base directories
ROOT_DIR="f:/DevSecOps/projects/xproject/flowdoc-consolidated"
V1_DIR="$ROOT_DIR/versions/flowdoc-v1"
SOURCE_DIR="f:/DevSecOps/projects/xproject"

# Create version directories
mkdir -p "$V1_DIR/backend/node/src"
mkdir -p "$V1_DIR/backend/python/src"
mkdir -p "$V1_DIR/frontend/admin-panel"
mkdir -p "$V1_DIR/infrastructure/docker"
mkdir -p "$V1_DIR/infrastructure/kubernetes"
mkdir -p "$V1_DIR/infrastructure/terraform"

# Copy and rename files with version note headers
for file in $(find "$SOURCE_DIR/docfly" -type f); do
    filename=$(basename "$file")
    case "$filename" in
        "main-api.js")
            echo '/**
 * Flowdoc v1 (Legacy)
 * Originally developed as "docfly"
 * Main API Implementation
 */
' > "$V1_DIR/backend/node/src/flowdoc-api.js"
            cat "$file" >> "$V1_DIR/backend/node/src/flowdoc-api.js"
            ;;
        "admin panel.js")
            echo '/**
 * Flowdoc v1 (Legacy)
 * Originally developed as "docfly"
 * Admin Panel Implementation
 */
' > "$V1_DIR/frontend/admin-panel/flowdoc-admin.js"
            cat "$file" >> "$V1_DIR/frontend/admin-panel/flowdoc-admin.js"
            ;;
        # Add more file mappings
    esac
done

# Create version documentation
echo "# Flowdoc v1 (Legacy)

This directory contains the first version of Flowdoc, originally developed under the name 'docfly'.
While the code maintains its original implementation for historical reference, all new development
should follow current Flowdoc naming conventions and architectural patterns.

For current version, see ../flowdoc-v2/" > "$V1_DIR/README.md"

# Create symlink to current version
ln -s "$ROOT_DIR/src" "$ROOT_DIR/versions/flowdoc-v2/current"