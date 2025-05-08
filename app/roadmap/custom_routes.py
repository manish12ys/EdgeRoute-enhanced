from flask import render_template, request, jsonify, flash, redirect, url_for, Blueprint, abort
from flask_login import current_user, login_required
from app import db
from app.models import Roadmap, RoadmapNode, CustomRoadmap, CustomRoadmapNode
from app.forms import CustomRoadmapForm, CustomRoadmapNodeForm, ResourceLinkForm
from app.roadmap import roadmap
import json
import uuid

@roadmap.route("/custom")
@login_required
def list_custom_roadmaps():
    """List all custom roadmaps created by the user"""
    custom_roadmaps = CustomRoadmap.query.filter_by(user_id=current_user.id).all()
    public_roadmaps = CustomRoadmap.query.filter_by(is_public=True).filter(CustomRoadmap.user_id != current_user.id).all()

    return render_template('roadmap/custom/list.html',
                          title='My Custom Roadmaps',
                          custom_roadmaps=custom_roadmaps,
                          public_roadmaps=public_roadmaps)

@roadmap.route("/custom/create", methods=['GET', 'POST'])
@login_required
def create_custom_roadmap():
    """Create a new custom roadmap"""
    form = CustomRoadmapForm()

    if form.validate_on_submit():
        # Process tags
        tags = form.tags.data.strip()

        # Create new custom roadmap
        custom_roadmap = CustomRoadmap(
            id=str(uuid.uuid4()),
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            difficulty=form.difficulty.data,
            tags=tags,
            is_public=form.is_public.data,
            user_id=current_user.id
        )

        db.session.add(custom_roadmap)
        db.session.commit()

        flash('Your custom roadmap has been created!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=custom_roadmap.id))

    return render_template('roadmap/custom/create.html',
                          title='Create Custom Roadmap',
                          form=form)

@roadmap.route("/custom/clone/<string:roadmap_id>", methods=['GET', 'POST'])
@login_required
def clone_roadmap(roadmap_id):
    """Clone an existing roadmap to create a custom one"""
    # Get the source roadmap
    source_roadmap = Roadmap.query.get_or_404(roadmap_id)

    form = CustomRoadmapForm()

    if request.method == 'GET':
        # Pre-fill the form with the source roadmap data
        form.title.data = f"My version of {source_roadmap.title}"
        form.description.data = source_roadmap.description
        form.category.data = source_roadmap.category
        form.difficulty.data = source_roadmap.difficulty
        form.tags.data = source_roadmap.tags

    if form.validate_on_submit():
        # Create new custom roadmap
        custom_roadmap = CustomRoadmap(
            id=str(uuid.uuid4()),
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            difficulty=form.difficulty.data,
            tags=form.tags.data,
            is_public=form.is_public.data,
            user_id=current_user.id,
            cloned_from=source_roadmap.id
        )

        db.session.add(custom_roadmap)

        # Clone the nodes
        source_nodes = RoadmapNode.query.filter_by(roadmap_id=source_roadmap.id).all()
        for i, node in enumerate(source_nodes):
            custom_node = CustomRoadmapNode(
                id=str(uuid.uuid4()),
                roadmap_id=custom_roadmap.id,
                title=node.title,
                description=node.description,
                links=node.links,
                position=i
            )
            db.session.add(custom_node)

        db.session.commit()

        flash(f'You have successfully cloned "{source_roadmap.title}"!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=custom_roadmap.id))

    return render_template('roadmap/custom/clone.html',
                          title=f'Clone {source_roadmap.title}',
                          form=form,
                          source_roadmap=source_roadmap)

@roadmap.route("/custom/<string:roadmap_id>")
def view_custom_roadmap(roadmap_id):
    """View a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)

    # Check if the user has permission to view this roadmap
    if not custom_roadmap.is_public and (not current_user.is_authenticated or custom_roadmap.user_id != current_user.id):
        abort(403)

    # Get all nodes ordered by position
    nodes = CustomRoadmapNode.query.filter_by(roadmap_id=roadmap_id).order_by(CustomRoadmapNode.position).all()

    return render_template('roadmap/custom/view.html',
                          title=custom_roadmap.title,
                          roadmap=custom_roadmap,
                          nodes=nodes)

@roadmap.route("/custom/<string:roadmap_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_custom_roadmap(roadmap_id):
    """Edit a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    form = CustomRoadmapForm()

    if request.method == 'GET':
        # Pre-fill the form with the roadmap data
        form.title.data = custom_roadmap.title
        form.description.data = custom_roadmap.description
        form.category.data = custom_roadmap.category
        form.difficulty.data = custom_roadmap.difficulty
        form.tags.data = custom_roadmap.tags
        form.is_public.data = custom_roadmap.is_public

    if form.validate_on_submit():
        # Update the roadmap
        custom_roadmap.title = form.title.data
        custom_roadmap.description = form.description.data
        custom_roadmap.category = form.category.data
        custom_roadmap.difficulty = form.difficulty.data
        custom_roadmap.tags = form.tags.data
        custom_roadmap.is_public = form.is_public.data

        db.session.commit()

        flash('Your roadmap has been updated!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))

    # Get all nodes ordered by position
    nodes = CustomRoadmapNode.query.filter_by(roadmap_id=roadmap_id).order_by(CustomRoadmapNode.position).all()

    return render_template('roadmap/custom/edit.html',
                          title=f'Edit {custom_roadmap.title}',
                          form=form,
                          roadmap=custom_roadmap,
                          nodes=nodes)

@roadmap.route("/custom/<string:roadmap_id>/delete", methods=['POST'])
@login_required
def delete_custom_roadmap(roadmap_id):
    """Delete a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)

    # Check if the user has permission to delete this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    db.session.delete(custom_roadmap)
    db.session.commit()

    flash('Your roadmap has been deleted!', 'success')
    return redirect(url_for('roadmap.list_custom_roadmaps'))

@roadmap.route("/custom/<string:roadmap_id>/node/add", methods=['GET', 'POST'])
@login_required
def add_custom_roadmap_node(roadmap_id):
    """Add a new node to a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    form = CustomRoadmapNodeForm()

    if form.validate_on_submit():
        # Get the highest position value
        highest_position = db.session.query(db.func.max(CustomRoadmapNode.position)).filter_by(roadmap_id=roadmap_id).scalar() or -1

        # Create new node
        node = CustomRoadmapNode(
            id=str(uuid.uuid4()),
            roadmap_id=roadmap_id,
            title=form.title.data,
            description=form.description.data,
            position=highest_position + 1
        )

        db.session.add(node)
        db.session.commit()

        flash('Node added successfully!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))

    return render_template('roadmap/custom/add_node.html',
                          title='Add Node',
                          form=form,
                          roadmap=custom_roadmap)

@roadmap.route("/custom/<string:roadmap_id>/node/<string:node_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_custom_roadmap_node(roadmap_id, node_id):
    """Edit a node in a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)
    node = CustomRoadmapNode.query.get_or_404(node_id)

    # Check if the node belongs to the roadmap
    if node.roadmap_id != roadmap_id:
        abort(404)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    form = CustomRoadmapNodeForm()

    if request.method == 'GET':
        # Pre-fill the form with the node data
        form.title.data = node.title
        form.description.data = node.description
        form.position.data = node.position

    if form.validate_on_submit():
        # Update the node
        node.title = form.title.data
        node.description = form.description.data

        db.session.commit()

        flash('Node updated successfully!', 'success')
        return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))

    return render_template('roadmap/custom/edit_node.html',
                          title='Edit Node',
                          form=form,
                          roadmap=custom_roadmap,
                          node=node)

@roadmap.route("/custom/<string:roadmap_id>/node/<string:node_id>/delete", methods=['POST'])
@login_required
def delete_custom_roadmap_node(roadmap_id, node_id):
    """Delete a node from a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)
    node = CustomRoadmapNode.query.get_or_404(node_id)

    # Check if the node belongs to the roadmap
    if node.roadmap_id != roadmap_id:
        abort(404)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    # Get the position of the deleted node
    deleted_position = node.position

    # Delete the node
    db.session.delete(node)

    # Update positions of remaining nodes
    nodes_to_update = CustomRoadmapNode.query.filter(
        CustomRoadmapNode.roadmap_id == roadmap_id,
        CustomRoadmapNode.position > deleted_position
    ).all()

    for node in nodes_to_update:
        node.position -= 1

    db.session.commit()

    flash('Node deleted successfully!', 'success')
    return redirect(url_for('roadmap.edit_custom_roadmap', roadmap_id=roadmap_id))

@roadmap.route("/custom/<string:roadmap_id>/node/<string:node_id>/links", methods=['GET', 'POST'])
@login_required
def manage_node_links(roadmap_id, node_id):
    """Manage resource links for a node"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)
    node = CustomRoadmapNode.query.get_or_404(node_id)

    # Check if the node belongs to the roadmap
    if node.roadmap_id != roadmap_id:
        abort(404)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    form = ResourceLinkForm()

    if form.validate_on_submit():
        # Get existing links
        links = node.get_links()

        # Add new link
        links.append({
            'title': form.title.data,
            'url': form.url.data,
            'type': form.type.data
        })

        # Save links back to node
        node.links = json.dumps(links)
        db.session.commit()

        flash('Resource link added successfully!', 'success')
        return redirect(url_for('roadmap.manage_node_links', roadmap_id=roadmap_id, node_id=node_id))

    # Get existing links
    links = node.get_links()

    return render_template('roadmap/custom/manage_links.html',
                          title='Manage Resource Links',
                          form=form,
                          roadmap=custom_roadmap,
                          node=node,
                          links=links)

@roadmap.route("/custom/<string:roadmap_id>/node/<string:node_id>/links/delete/<int:link_index>", methods=['POST'])
@login_required
def delete_node_link(roadmap_id, node_id, link_index):
    """Delete a resource link from a node"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)
    node = CustomRoadmapNode.query.get_or_404(node_id)

    # Check if the node belongs to the roadmap
    if node.roadmap_id != roadmap_id:
        abort(404)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        abort(403)

    # Get existing links
    links = node.get_links()

    # Check if the link index is valid
    if link_index < 0 or link_index >= len(links):
        abort(404)

    # Remove the link
    links.pop(link_index)

    # Save links back to node
    node.links = json.dumps(links)
    db.session.commit()

    flash('Resource link deleted successfully!', 'success')
    return redirect(url_for('roadmap.manage_node_links', roadmap_id=roadmap_id, node_id=node_id))

@roadmap.route("/custom/<string:roadmap_id>/reorder", methods=['POST'])
@login_required
def reorder_nodes(roadmap_id):
    """Reorder nodes in a custom roadmap"""
    custom_roadmap = CustomRoadmap.query.get_or_404(roadmap_id)

    # Check if the user has permission to edit this roadmap
    if custom_roadmap.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403

    # Get the new order from the request
    try:
        new_order = request.json.get('nodes', [])

        # Update positions
        for position, node_id in enumerate(new_order):
            node = CustomRoadmapNode.query.get(node_id)
            if node and node.roadmap_id == roadmap_id:
                node.position = position

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
