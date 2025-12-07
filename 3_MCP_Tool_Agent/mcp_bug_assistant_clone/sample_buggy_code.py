#!/usr/bin/env python3
"""
Sample buggy code for testing the Bug Assistant
Contains various intentional bugs and security issues
"""

import os
import sys

# TODO: Refactor this entire module
# FIXME: Security issues need addressing


def dangerous_eval_usage(user_input):
    """Security risk: using eval with user input"""
    result = eval(user_input)  # DANGEROUS!
    return result


def dangerous_exec_usage(code_string):
    """Security risk: using exec"""
    exec(code_string)  # DANGEROUS!


def bare_except_example():
    """Poor error handling"""
    try:
        risky_operation()
    except:  # Bare except - catches everything!
        pass


def password_logging(username, password):
    """Security risk: logging sensitive data"""
    print(f"User {username} logged in with password: {password}")
    logger.info(f"Password is: {password}")


def sql_injection_risk(user_id):
    """SQL injection vulnerability"""
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)  # Vulnerable to SQL injection!


def incomplete_function():
    """Incomplete implementation"""
    # TODO: Implement this function
    pass


class BuggyClass:
    """Class with various issues"""
    
    def __init__(self):
        self.data = None
    
    def process_data(self, input_data):
        # HACK: This is a temporary workaround
        try:
            result = eval(input_data)
        except:
            result = None
        return result
    
    def unsafe_file_operation(self, filename):
        """Unsafe file handling"""
        # No validation of filename
        exec(open(filename).read())


# Syntax error example (commented out to allow file to be imported)
# def syntax_error_function(
#     print("Missing closing parenthesis"


def another_todo_item():
    """Another incomplete function"""
    # FIXME: This needs proper implementation
    # XXX: Temporary hack
    return None


# More security issues
API_KEY = "secret_key_12345"
print(f"API Key: {API_KEY}")  # Exposing secrets!


def use_dangerous_import():
    """Dynamic imports can be risky"""
    module_name = input("Enter module name: ")
    mod = __import__(module_name)  # Dangerous!
    return mod


if __name__ == "__main__":
    print("This is intentionally buggy code for testing")
    # More issues here
    user_code = input("Enter code to execute: ")
    eval(user_code)  # Very dangerous!
