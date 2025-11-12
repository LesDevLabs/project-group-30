"""
Comprehensive tests for CommandHandler class.
Tests all methods including success cases and error handling.
Run with: python test_command_handler.py
"""
from repositories.contact_repository import ContactRepository
from handlers.command_handler import CommandHandler
from models.contact import Record


def create_sample_contact():
    """Create a sample contact with all fields"""
    contact = Record("John Doe")
    contact.add_phone("1234567890")
    contact.add_phone("0987654321")
    contact.add_email("john@example.com")
    contact.set_address("123 Main St")
    contact.set_birthday("01.01.1990")
    return contact


def run_test(test_name, test_func):
    """Run a test and report results"""
    try:
        test_func()
        print(f"✓ {test_name}")
        return True
    except AssertionError as e:
        print(f"✗ {test_name}")
        print(f"  AssertionError: {e}")
        return False
    except Exception as e:
        print(f"✗ {test_name}")
        print(f"  Exception: {type(e).__name__}: {e}")
        return False


# ========== add_contact tests ==========

def test_add_contact_new_contact_name_only():
    """Test adding a new contact with only name"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.add_contact("Alice")
    assert result == "Contact added."
    contact = handler.repository.find_contact("Alice")
    assert contact is not None
    assert contact.name.value == "Alice"


def test_add_contact_new_contact_with_all_fields():
    """Test adding a new contact with all fields"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.add_contact(
        "Bob",
        phone="5551234567",
        email="bob@example.com",
        address="456 Oak Ave",
        birthday="15.05.1985"
    )
    assert result == "Contact added."
    contact = handler.repository.find_contact("Bob")
    assert contact.name.value == "Bob"
    assert len(contact.phones) == 1
    assert contact.phones[0].value == "5551234567"
    assert len(contact.emails) == 1
    assert contact.emails[0].value == "bob@example.com"
    assert contact.address.value == "456 Oak Ave"
    assert contact.birthday is not None


def test_add_contact_update_existing_contact():
    """Test updating an existing contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    sample_contact = create_sample_contact()
    handler.repository.add_contact(sample_contact)
    result = handler.add_contact(
        "John Doe",
        phone="9999999999",
        email="newemail@example.com"
    )
    assert result == "Contact updated."
    contact = handler.repository.find_contact("John Doe")
    assert len(contact.phones) == 3  # 2 original + 1 new
    assert len(contact.emails) == 2  # 1 original + 1 new


def test_add_contact_partial_fields():
    """Test adding contact with some optional fields"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.add_contact(
        "Charlie",
        phone="1112223333",
        email="charlie@example.com"
    )
    assert result == "Contact added."
    contact = handler.repository.find_contact("Charlie")
    assert len(contact.phones) == 1
    assert len(contact.emails) == 1
    assert contact.address is None
    assert contact.birthday is None


# ========== show_contact tests ==========

def test_show_contact_existing():
    """Test showing an existing contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    sample_contact = create_sample_contact()
    handler.repository.add_contact(sample_contact)
    result = handler.show_contact("John Doe")
    assert "Contact name: John Doe" in result
    assert "1234567890" in result
    assert "john@example.com" in result


def test_show_contact_not_found():
    """Test showing a non-existent contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.show_contact("NonExistent")
    assert "Error:" in result
    assert "not found" in result


# ========== show_all_contacts tests ==========

def test_show_all_contacts_empty():
    """Test showing all contacts when repository is empty"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.show_all_contacts()
    assert result == "No contacts stored."


def test_show_all_contacts_with_multiple():
    """Test showing all contacts with multiple contacts"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Alice", phone="1111111111")
    handler.add_contact("Bob", phone="2222222222")
    handler.add_contact("Charlie", phone="3333333333")
    result = handler.show_all_contacts()
    assert "Alice" in result
    assert "Bob" in result
    assert "Charlie" in result
    assert "1111111111" in result
    assert "2222222222" in result
    assert "3333333333" in result


# ========== change tests ==========

def test_change_phone_existing():
    """Test changing an existing phone number"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("David", phone="1111111111")
    result = handler.change("David", "1111111111", "9999999999")
    assert "changed from" in result
    assert "1111111111" in result
    assert "9999999999" in result
    contact = handler.repository.find_contact("David")
    assert "9999999999" in [p.value for p in contact.phones]


def test_change_phone_contact_not_found():
    """Test changing phone for non-existent contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.change("NonExistent", "1111111111", "9999999999")
    assert "Error:" in result
    assert "not found" in result


def test_change_phone_phone_not_found():
    """Test changing a phone number that doesn't exist"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Eve", phone="1111111111")
    result = handler.change("Eve", "9999999999", "8888888888")
    assert "Error:" in result
    assert "not found" in result


def test_change_phone_multiple_phones():
    """Test changing one phone when contact has multiple phones"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Frank", phone="1111111111")
    handler.add_contact("Frank", phone="2222222222")
    result = handler.change("Frank", "1111111111", "3333333333")
    assert "changed from" in result
    contact = handler.repository.find_contact("Frank")
    phone_values = [p.value for p in contact.phones]
    assert "3333333333" in phone_values
    assert "2222222222" in phone_values
    assert "1111111111" not in phone_values


# ========== edit_name tests ==========

def test_edit_name_success():
    """Test renaming a contact successfully"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    sample_contact = create_sample_contact()
    handler.repository.add_contact(sample_contact)
    result = handler.edit_name("John Doe", "Jane Doe")
    assert "changed from" in result
    assert "John Doe" in result
    assert "Jane Doe" in result
    # Old name should not exist
    assert handler.repository.find_contact("John Doe") is None
    # New name should exist
    contact = handler.repository.find_contact("Jane Doe")
    assert contact is not None
    assert contact.name.value == "Jane Doe"
    # Other fields should be preserved
    assert len(contact.phones) == 2


def test_edit_name_contact_not_found():
    """Test renaming a non-existent contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.edit_name("NonExistent", "NewName")
    assert "Error:" in result
    assert "not found" in result


def test_edit_name_target_exists():
    """Test renaming to a name that already exists"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Alice")
    handler.add_contact("Bob")
    result = handler.edit_name("Alice", "Bob")
    assert "Error:" in result
    assert "already exists" in result
    # Original contacts should still exist
    assert handler.repository.find_contact("Alice") is not None
    assert handler.repository.find_contact("Bob") is not None


# ========== delete_contact tests ==========

def test_delete_contact_existing():
    """Test deleting an existing contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    sample_contact = create_sample_contact()
    handler.repository.add_contact(sample_contact)
    result = handler.delete_contact("John Doe")
    assert "deleted successfully" in result
    assert handler.repository.find_contact("John Doe") is None


def test_delete_contact_not_found():
    """Test deleting a non-existent contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.delete_contact("NonExistent")
    assert "Error:" in result
    assert "not found" in result


def test_delete_contact_multiple_contacts():
    """Test deleting one contact when multiple exist"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Alice")
    handler.add_contact("Bob")
    handler.add_contact("Charlie")
    result = handler.delete_contact("Bob")
    assert "deleted successfully" in result
    assert handler.repository.find_contact("Alice") is not None
    assert handler.repository.find_contact("Bob") is None
    assert handler.repository.find_contact("Charlie") is not None


# ========== delete_phone tests ==========

def test_delete_phone_success():
    """Test deleting a phone number successfully"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("George", phone="1111111111")
    handler.add_contact("George", phone="2222222222")
    result = handler.delete_phone("George", "1111111111")
    assert "removed from contact" in result
    contact = handler.repository.find_contact("George")
    phone_values = [p.value for p in contact.phones]
    assert "1111111111" not in phone_values
    assert "2222222222" in phone_values


def test_delete_phone_contact_not_found():
    """Test deleting phone from non-existent contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.delete_phone("NonExistent", "1111111111")
    assert "Error:" in result
    assert "not found" in result


def test_delete_phone_phone_not_found():
    """Test deleting a phone number that doesn't exist"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Henry", phone="1111111111")
    result = handler.delete_phone("Henry", "9999999999")
    assert "Error:" in result
    assert "not found" in result


def test_delete_phone_last_phone():
    """Test deleting the last phone number from a contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Iris", phone="1111111111")
    result = handler.delete_phone("Iris", "1111111111")
    assert "removed from contact" in result
    contact = handler.repository.find_contact("Iris")
    assert len(contact.phones) == 0


# ========== Integration tests ==========

def test_full_workflow():
    """Test a complete workflow of operations"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    # Add contact
    result = handler.add_contact("Test User", phone="1234567890",
                                 email="test@example.com")
    assert result == "Contact added."

    # Show contact
    result = handler.show_contact("Test User")
    assert "Test User" in result

    # Add another phone
    handler.add_contact("Test User", phone="0987654321")

    # Change phone
    result = handler.change("Test User", "1234567890", "5555555555")
    assert "changed from" in result

    # Show all
    result = handler.show_all_contacts()
    assert "Test User" in result

    # Delete phone
    result = handler.delete_phone("Test User", "0987654321")
    assert "removed" in result

    # Rename
    result = handler.edit_name("Test User", "Renamed User")
    assert "changed from" in result

    # Delete contact
    result = handler.delete_contact("Renamed User")
    assert "deleted successfully" in result

    # Verify deleted
    result = handler.show_all_contacts()
    assert result == "No contacts stored."


def test_commands_dictionary():
    """Test that all commands are registered in the commands dictionary"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    assert "add" in handler.commands
    assert "show" in handler.commands
    assert "all" in handler.commands
    assert "change" in handler.commands
    assert "rename" in handler.commands
    assert "delete" in handler.commands
    assert "delete-phone" in handler.commands
    assert len(handler.commands) == 7


# ========== Edge cases ==========

def test_add_contact_empty_string_name():
    """Test adding contact with empty string name"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.add_contact("")
    assert result == "Contact added."
    contact = handler.repository.find_contact("")
    assert contact is not None


def test_add_contact_special_characters():
    """Test adding contact with special characters"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    result = handler.add_contact("O'Brien", phone="1234567890")
    assert result == "Contact added."
    contact = handler.repository.find_contact("O'Brien")
    assert contact is not None


def test_show_all_contacts_single_contact():
    """Test showing all contacts with single contact"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Single", phone="1111111111")
    result = handler.show_all_contacts()
    assert "Single" in result
    assert "1111111111" in result


def test_change_phone_same_value():
    """Test changing phone to the same value"""
    repository = ContactRepository()
    handler = CommandHandler(repository)
    handler.add_contact("Same", phone="1111111111")
    result = handler.change("Same", "1111111111", "1111111111")
    assert "changed from" in result
    contact = handler.repository.find_contact("Same")
    assert "1111111111" in [p.value for p in contact.phones]


# ========== Test Runner ==========

def main():
    """Run all tests"""
    tests = [
        # add_contact tests
        ("add_contact_new_contact_name_only",
         test_add_contact_new_contact_name_only),
        ("add_contact_new_contact_with_all_fields",
         test_add_contact_new_contact_with_all_fields),
        ("add_contact_update_existing_contact",
         test_add_contact_update_existing_contact),
        ("add_contact_partial_fields", test_add_contact_partial_fields),
        # show_contact tests
        ("show_contact_existing", test_show_contact_existing),
        ("show_contact_not_found", test_show_contact_not_found),
        # show_all_contacts tests
        ("show_all_contacts_empty", test_show_all_contacts_empty),
        ("show_all_contacts_with_multiple",
         test_show_all_contacts_with_multiple),
        # change tests
        ("change_phone_existing", test_change_phone_existing),
        ("change_phone_contact_not_found",
         test_change_phone_contact_not_found),
        ("change_phone_phone_not_found",
         test_change_phone_phone_not_found),
        ("change_phone_multiple_phones", test_change_phone_multiple_phones),
        # edit_name tests
        ("edit_name_success", test_edit_name_success),
        ("edit_name_contact_not_found", test_edit_name_contact_not_found),
        ("edit_name_target_exists", test_edit_name_target_exists),
        # delete_contact tests
        ("delete_contact_existing", test_delete_contact_existing),
        ("delete_contact_not_found", test_delete_contact_not_found),
        ("delete_contact_multiple_contacts",
         test_delete_contact_multiple_contacts),
        # delete_phone tests
        ("delete_phone_success", test_delete_phone_success),
        ("delete_phone_contact_not_found",
         test_delete_phone_contact_not_found),
        ("delete_phone_phone_not_found",
         test_delete_phone_phone_not_found),
        ("delete_phone_last_phone", test_delete_phone_last_phone),
        # Integration tests
        ("full_workflow", test_full_workflow),
        ("commands_dictionary", test_commands_dictionary),
        # Edge cases
        ("add_contact_empty_string_name",
         test_add_contact_empty_string_name),
        ("add_contact_special_characters",
         test_add_contact_special_characters),
        ("show_all_contacts_single_contact",
         test_show_all_contacts_single_contact),
        ("change_phone_same_value", test_change_phone_same_value),
    ]

    print("Running CommandHandler tests...\n")
    passed = 0
    failed = 0

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")
    print(f"Total tests: {len(tests)}")
    print(f"{'='*50}")

    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
