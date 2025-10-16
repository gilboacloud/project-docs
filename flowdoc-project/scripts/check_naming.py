#!/usr/bin/env python3
"""
Flowdoc Naming Convention Checker
This script verifies naming consistency across the Flowdoc codebase.
"""

import os
import re
import yaml
import json
from typing import List, Dict, Any

class FlowdocConsistencyChecker:
    """Checks naming consistency in Flowdoc codebase"""
    
    EXPECTED_PREFIX = "flowdoc"
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.issues: List[str] = []
    
    def check_env_variables(self, filepath: str) -> None:
        """Check environment variable naming"""
        with open(filepath, 'r') as f:
            content = f.read()
            env_vars = re.findall(r'\${?([A-Z_]+)}?', content)
            for var in env_vars:
                if not var.startswith('FLOWDOC_'):
                    self.issues.append(f"Non-prefixed env var in {filepath}: {var}")
    
    def check_kubernetes_resources(self, filepath: str) -> None:
        """Check Kubernetes resource naming"""
        with open(filepath, 'r') as f:
            try:
                resources = list(yaml.safe_load_all(f))
                for resource in resources:
                    if resource:
                        name = resource.get('metadata', {}).get('name', '')
                        if not name.startswith('flowdoc'):
                            self.issues.append(f"Non-prefixed K8s resource in {filepath}: {name}")
            except yaml.YAMLError:
                self.issues.append(f"Invalid YAML in {filepath}")
    
    def check_docker_services(self, filepath: str) -> None:
        """Check Docker service naming"""
        with open(filepath, 'r') as f:
            try:
                compose = yaml.safe_load(f)
                services = compose.get('services', {})
                for service_name in services:
                    if not service_name.startswith('flowdoc'):
                        self.issues.append(f"Non-prefixed Docker service in {filepath}: {service_name}")
            except yaml.YAMLError:
                self.issues.append(f"Invalid YAML in {filepath}")
    
    def check_python_constants(self, filepath: str) -> None:
        """Check Python constant naming"""
        with open(filepath, 'r') as f:
            content = f.read()
            if 'class Config' in content:
                constants = re.findall(r'([A-Z_]+)\s*=', content)
                for const in constants:
                    if not (const.startswith('FLOWDOC_') or const in ['DEBUG', 'TESTING']):
                        self.issues.append(f"Non-prefixed constant in {filepath}: {const}")
    
    def run_checks(self) -> List[str]:
        """Run all consistency checks"""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                filepath = os.path.join(root, file)
                
                if file.endswith(('.yaml', '.yml')):
                    self.check_kubernetes_resources(filepath)
                
                if file == 'docker-compose.yml':
                    self.check_docker_services(filepath)
                
                if file.endswith('.py'):
                    self.check_python_constants(filepath)
                
                if file in ['.env', '.env.example', 'config.yaml']:
                    self.check_env_variables(filepath)
        
        return self.issues

def main():
    checker = FlowdocConsistencyChecker('.')
    issues = checker.run_checks()
    
    if issues:
        print("Found naming consistency issues:")
        for issue in issues:
            print(f"- {issue}")
        exit(1)
    else:
        print("All naming conventions are consistent!")
        exit(0)

if __name__ == '__main__':
    main()