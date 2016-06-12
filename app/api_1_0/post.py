from flask.ext.login import login_required
from . import api
from flask import jsonify, g, request, current_app, url_for, abort
from .. import db
from ..models import User, Post, Permission
from .errors import forbidden
from .decocrator import permission_required


@api.route('/post/', method=['POST'])
@permission_required(Permission.ADMINISTOR)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201


def get_posts():
    posts = Post.query.all()
    return jsonify({'posts': [post.to_json() for post in posts]})


@api.route('/post/<int:id>')
@permission_required(Permission.ADMINISTOR)
def get_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return forbidden('Insuficient permission')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


@api.route('/post/<int:id>', method=['PUT'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return forbidden('Insuficient permission')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


@api.route('/post/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POST_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page + 1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
