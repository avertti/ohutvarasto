import unittest
import os
import tempfile
from app import app, get_db_session, reset_db
from models import Base, Warehouse, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestWarehouseApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary database file for testing
        cls.db_fd, cls.db_path = tempfile.mkstemp()
        db_url = f'sqlite:///{cls.db_path}'
        os.environ['DATABASE_URL'] = db_url
        
        # Reset the app's database connection to use the test database
        reset_db()
        
        # Set up the engine and session for direct database access in tests
        cls.engine = create_engine(db_url)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Close and remove the temporary database file
        os.close(cls.db_fd)
        os.unlink(cls.db_path)
        # Reset the database connection
        reset_db()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Clear all data before each test
        session = self.Session()
        session.query(Item).delete()
        session.query(Warehouse).delete()
        session.commit()
        session.close()

    def test_index_empty(self):
        """Test that the index page loads successfully with no warehouses."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses', response.data)
        self.assertIn(b'No warehouses found', response.data)

    def test_create_warehouse_get(self):
        """Test that the create warehouse form loads successfully."""
        response = self.app.get('/warehouse/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New', response.data)
        self.assertIn(b'Warehouse Name', response.data)

    def test_create_warehouse_post(self):
        """Test creating a new warehouse."""
        response = self.app.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertIn(b'created successfully', response.data)

    def test_create_warehouse_empty_name(self):
        """Test creating a warehouse with an empty name."""
        response = self.app.post('/warehouse/new', data={
            'name': '',
            'capacity': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse name is required', response.data)

    def test_view_warehouse(self):
        """Test viewing a single warehouse."""
        # First create a warehouse
        session = self.Session()
        warehouse = Warehouse(name='View Test', capacity=50.0)
        session.add(warehouse)
        session.commit()
        warehouse_id = warehouse.id
        session.close()

        response = self.app.get(f'/warehouse/{warehouse_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'View Test', response.data)
        self.assertIn(b'50.0', response.data)

    def test_view_nonexistent_warehouse(self):
        """Test viewing a warehouse that doesn't exist."""
        response = self.app.get('/warehouse/9999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse not found', response.data)

    def test_edit_warehouse(self):
        """Test editing a warehouse."""
        # First create a warehouse
        session = self.Session()
        warehouse = Warehouse(name='Edit Test', capacity=30.0)
        session.add(warehouse)
        session.commit()
        warehouse_id = warehouse.id
        session.close()

        # Edit the warehouse
        response = self.app.post(f'/warehouse/{warehouse_id}/edit', data={
            'name': 'Updated Warehouse',
            'capacity': '200'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Warehouse', response.data)
        self.assertIn(b'updated successfully', response.data)

    def test_delete_warehouse(self):
        """Test deleting a warehouse."""
        # First create a warehouse
        session = self.Session()
        warehouse = Warehouse(name='Delete Test', capacity=20.0)
        session.add(warehouse)
        session.commit()
        warehouse_id = warehouse.id
        session.close()

        # Delete the warehouse
        response = self.app.post(f'/warehouse/{warehouse_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)

    def test_add_item(self):
        """Test adding an item to a warehouse."""
        # First create a warehouse
        session = self.Session()
        warehouse = Warehouse(name='Item Test', capacity=100.0)
        session.add(warehouse)
        session.commit()
        warehouse_id = warehouse.id
        session.close()

        # Add an item
        response = self.app.post(f'/warehouse/{warehouse_id}/item/add', data={
            'name': 'Test Item',
            'quantity': '5'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Item', response.data)
        self.assertIn(b'added successfully', response.data)

    def test_add_item_empty_name(self):
        """Test adding an item with an empty name."""
        # First create a warehouse
        session = self.Session()
        warehouse = Warehouse(name='Item Test 2', capacity=100.0)
        session.add(warehouse)
        session.commit()
        warehouse_id = warehouse.id
        session.close()

        response = self.app.post(f'/warehouse/{warehouse_id}/item/add', data={
            'name': '',
            'quantity': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Item name is required', response.data)

    def test_edit_item(self):
        """Test editing an item."""
        # First create a warehouse and an item
        session = self.Session()
        warehouse = Warehouse(name='Edit Item Test', capacity=100.0)
        session.add(warehouse)
        session.commit()
        item = Item(name='Original Item', quantity=10.0, warehouse_id=warehouse.id)
        session.add(item)
        session.commit()
        warehouse_id = warehouse.id
        item_id = item.id
        session.close()

        # Edit the item
        response = self.app.post(f'/warehouse/{warehouse_id}/item/{item_id}/edit', data={
            'name': 'Updated Item',
            'quantity': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Item', response.data)
        self.assertIn(b'updated successfully', response.data)

    def test_delete_item(self):
        """Test deleting an item."""
        # First create a warehouse and an item
        session = self.Session()
        warehouse = Warehouse(name='Delete Item Test', capacity=100.0)
        session.add(warehouse)
        session.commit()
        item = Item(name='Item to Delete', quantity=15.0, warehouse_id=warehouse.id)
        session.add(item)
        session.commit()
        warehouse_id = warehouse.id
        item_id = item.id
        session.close()

        # Delete the item
        response = self.app.post(f'/warehouse/{warehouse_id}/item/{item_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)

    def test_list_warehouses(self):
        """Test listing all warehouses."""
        # Create multiple warehouses
        session = self.Session()
        warehouse1 = Warehouse(name='Warehouse 1', capacity=50.0)
        warehouse2 = Warehouse(name='Warehouse 2', capacity=75.0)
        session.add_all([warehouse1, warehouse2])
        session.commit()
        session.close()

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse 1', response.data)
        self.assertIn(b'Warehouse 2', response.data)

    def test_invalid_capacity_uses_default(self):
        """Test that invalid capacity is handled properly."""
        response = self.app.post('/warehouse/new', data={
            'name': 'Invalid Capacity Test',
            'capacity': 'not-a-number'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid Capacity Test', response.data)


if __name__ == '__main__':
    unittest.main()
