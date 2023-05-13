from time import perf_counter
from parse_email import is_food_event, extract_fields

PRINT_EMAIL = True
TEST_CLS = False
TEST_EXTRACT = True

with open("dummy_email.txt") as f:
    dummy_email = f.read()

if PRINT_EMAIL:
    print(dummy_email, end='\n---\n\n')

if TEST_CLS:
    start = perf_counter()
    fef = is_food_event(dummy_email)
    print(f"is_food_event: {fef}, finished in {perf_counter() - start}s")

if TEST_EXTRACT:
    start = perf_counter()
    fields = extract_fields(dummy_email)
    print(f"extract_fields:\n\n{fields}\n\nfinished in {perf_counter() - start}s")
