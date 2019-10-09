from flask import Flask, Response, jsonify

""" Create own Flask class to response with format json

Keyword arguments:
Return: Flask object
"""


class MyResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(MyResponse, cls).force_type(rv, environ)


class MyFlask(Flask):
    response_class = MyResponse
