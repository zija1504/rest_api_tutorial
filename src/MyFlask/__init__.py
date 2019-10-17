from flask import Flask, Response, jsonify


""" Create own Flask class to response with format json

Keyword arguments:
Return: Flask object
"""


class MyFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, (dict, list)):
            rv = jsonify(rv)
        return super().make_response(rv)
