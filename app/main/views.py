# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, current_app,\
    abort, flash
from flask.ext.login import login_required, current_user
from . import main
from ..models import Post, Role, User, Permission, Comment
from ..decorators import admin_required, permission_required
from .. import db
from .forms import PostForm, CommentForm


@main.route('/', methods=['GET', 'POST'])
def index():

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POST_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts,
                           pagination=pagination)


@main.route('/post_form', methods=['GET', 'POST'])
@login_required
def post_form():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))

    return render_template('post_form.html', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTRATOR):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          # author=current_user._get_current_object()
                          )
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        #comment or comments
        page = (post.comments.count() - 1) //\
            current_app.config['FLASKY_COMMNET_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMNET_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)

# ToDo: 需要将index中post文本框新建为单独的网页，以免造成删除后加载页面失败
# 该错误造成的主要原因为页面返回时，需要重新渲染页面，查询form参数


@main.route('/post/delete/<int:id>')
def post_delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return render_template('post.html',
                           page=request.args.get('page', 1, type=int))


@main.route('/moderate/enbale/<int:id>')
@login_required
#@permission_required(Permission.ADMINISTOR)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
#@permission_required(Permission.ADMINISTOR)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate')
@login_required
#@permission_required(Permission.ADMINISTOR)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMNET_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/delete/<int:id>/')
@login_required
def comments_delete(id):
    comment = Comment.query.get_or_404(id)
    # Comment.query.filter_by(comment=comment).delete()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
