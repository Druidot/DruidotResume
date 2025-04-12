from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for


def error_messages(e):
    for error in e.errors():
        flash(f"{error['loc'][0]}: {error['msg']}", "error") 


