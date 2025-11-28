import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Warehouse, Item

app = Flask(__name__)

# Secret key configuration - use environment variable in production
# In development mode, a default key is used for convenience
_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key:
    if os.environ.get('FLASK_ENV') == 'production':
        raise RuntimeError("SECRET_KEY environment variable must be set in production")
    _secret_key = 'dev-secret-key-do-not-use-in-production'
app.secret_key = _secret_key

# Database setup - use lazy initialization
_engine = None
_Session = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        db_url = os.environ.get('DATABASE_URL', 'sqlite:///warehouse.db')
        _engine = create_engine(db_url)
        Base.metadata.create_all(_engine)
    return _engine


def get_session_maker():
    """Get or create the session maker."""
    global _Session
    if _Session is None:
        _Session = sessionmaker(bind=get_engine())
    return _Session


def get_db_session():
    """Get a database session."""
    return get_session_maker()()


def reset_db():
    """Reset database connection (useful for testing)."""
    global _engine, _Session
    _engine = None
    _Session = None


@app.route('/')
def index():
    """List all warehouses."""
    session = get_db_session()
    try:
        warehouses = session.query(Warehouse).all()
        return render_template('index.html', warehouses=warehouses)
    finally:
        session.close()


@app.route('/warehouse/new', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        capacity = request.form.get('capacity', '0')

        if not name:
            flash('Warehouse name is required', 'error')
            return render_template('warehouse_form.html', warehouse=None)

        try:
            capacity = float(capacity)
        except ValueError:
            capacity = 0.0

        session = get_db_session()
        try:
            warehouse = Warehouse(name=name, capacity=capacity)
            session.add(warehouse)
            session.commit()
            flash(f'Warehouse "{name}" created successfully', 'success')
            return redirect(url_for('index'))
        finally:
            session.close()

    return render_template('warehouse_form.html', warehouse=None)


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View a single warehouse and its items."""
    session = get_db_session()
    try:
        warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
        if not warehouse:
            flash('Warehouse not found', 'error')
            return redirect(url_for('index'))
        return render_template('warehouse_view.html', warehouse=warehouse)
    finally:
        session.close()


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit a warehouse."""
    session = get_db_session()
    try:
        warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
        if not warehouse:
            flash('Warehouse not found', 'error')
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            capacity = request.form.get('capacity', '0')

            if not name:
                flash('Warehouse name is required', 'error')
                return render_template('warehouse_form.html', warehouse=warehouse)

            try:
                capacity = float(capacity)
            except ValueError:
                capacity = warehouse.capacity

            warehouse.name = name
            warehouse.capacity = capacity
            session.commit()
            flash(f'Warehouse "{name}" updated successfully', 'success')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

        return render_template('warehouse_form.html', warehouse=warehouse)
    finally:
        session.close()


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    session = get_db_session()
    try:
        warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
        if not warehouse:
            flash('Warehouse not found', 'error')
            return redirect(url_for('index'))

        name = warehouse.name
        session.delete(warehouse)
        session.commit()
        flash(f'Warehouse "{name}" deleted successfully', 'success')
        return redirect(url_for('index'))
    finally:
        session.close()


@app.route('/warehouse/<int:warehouse_id>/item/add', methods=['GET', 'POST'])
def add_item(warehouse_id):
    """Add an item to a warehouse."""
    session = get_db_session()
    try:
        warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
        if not warehouse:
            flash('Warehouse not found', 'error')
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            quantity = request.form.get('quantity', '0')

            if not name:
                flash('Item name is required', 'error')
                return render_template('item_form.html', warehouse=warehouse, item=None)

            try:
                quantity = float(quantity)
            except ValueError:
                quantity = 0.0

            item = Item(name=name, quantity=quantity, warehouse_id=warehouse_id)
            session.add(item)
            session.commit()
            flash(f'Item "{name}" added successfully', 'success')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

        return render_template('item_form.html', warehouse=warehouse, item=None)
    finally:
        session.close()


@app.route('/warehouse/<int:warehouse_id>/item/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(warehouse_id, item_id):
    """Edit an item in a warehouse."""
    session = get_db_session()
    try:
        warehouse = session.query(Warehouse).filter_by(id=warehouse_id).first()
        if not warehouse:
            flash('Warehouse not found', 'error')
            return redirect(url_for('index'))

        item = session.query(Item).filter_by(id=item_id, warehouse_id=warehouse_id).first()
        if not item:
            flash('Item not found', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            quantity = request.form.get('quantity', '0')

            if not name:
                flash('Item name is required', 'error')
                return render_template('item_form.html', warehouse=warehouse, item=item)

            try:
                quantity = float(quantity)
            except ValueError:
                quantity = item.quantity

            item.name = name
            item.quantity = quantity
            session.commit()
            flash(f'Item "{name}" updated successfully', 'success')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

        return render_template('item_form.html', warehouse=warehouse, item=item)
    finally:
        session.close()


@app.route('/warehouse/<int:warehouse_id>/item/<int:item_id>/delete', methods=['POST'])
def delete_item(warehouse_id, item_id):
    """Delete an item from a warehouse."""
    session = get_db_session()
    try:
        item = session.query(Item).filter_by(id=item_id, warehouse_id=warehouse_id).first()
        if not item:
            flash('Item not found', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

        name = item.name
        session.delete(item)
        session.commit()
        flash(f'Item "{name}" deleted successfully', 'success')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
    finally:
        session.close()


if __name__ == '__main__':
    # Only enable debug mode if explicitly set via environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)
