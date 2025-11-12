from utils import normalize_phone, validate_email, validate_phone_number

assert validate_email("test@example.com") is True
assert validate_email("user.name@domain.org") is True
assert validate_email("x@y.io") is True

try:
    validate_email("noatsign.com")
    assert False, "Expected ValueError for missing '@'"
except ValueError:
    pass

try:
    validate_email("bad@@mail.com")
    assert False, "Expected ValueError for double '@'"
except ValueError:
    pass

try:
    validate_email("user@domain")
    assert False, "Expected ValueError for missing domain suffix"
except ValueError:
    pass

try:
    validate_email("")
    assert False, "Expected ValueError for empty string"
except ValueError:
    pass

try:
    validate_email(None)
    assert False, "Expected ValueError for None"
except ValueError:
    pass


assert normalize_phone("380501234567") == "380501234567"
assert normalize_phone("380501234567") == "380501234567"
assert normalize_phone("050 123 45 67") == "380501234567"
assert normalize_phone("375291234567") == "375291234567"

try:
    assert validate_phone_number("380501234567") is True
except AssertionError as e:
    pass
assert validate_phone_number("380501234567") is True
assert validate_phone_number("050 123 45 67") is True

try:
    validate_phone_number("38050123456")
    assert False, "Expected ValueError for short phone number"
except ValueError:
    pass

try:
    validate_phone_number("38050A34567")
    assert False, "Expected ValueError for letters in phone number"
except ValueError:
    pass

try:
    validate_phone_number("invalid number")
    assert False, "Expected ValueError for invalid phone input"
except ValueError:
    pass

print("✅ All assert tests passed successfully!")
