from randomizer import (
    format_list,
    format_list_probabilities,
    get_from_list,
    deepcopy_list,
    RandomList,
    RandomGroup,
)

# ------------------------------------------------- #
#                     Helper Tests                  #
# ------------------------------------------------- #

def test_format_list():
    test_list = [
        "vanilla",
        "chocolate",
        {"item": "strawberry", "probability": 2}
    ]
    formatted_test_list = [
        {"item": "strawberry", "probability": 2},
        {"item": "vanilla", "probability": 1},
        {"item": "chocolate", "probability": 1}
    ]
    assert format_list(test_list) == formatted_test_list

def test_format_list_probabilities():
    test_list = [
        {"item": "strawberry", "probability": 2},
        {"item": "vanilla", "probability": 1},
        {"item": "chocolate", "probability": 1}
    ]
    formatted_test_list = [
        {"item": "strawberry", "probability": 2},
        {"item": "vanilla", "probability": 3},
        {"item": "chocolate", "probability": 4}
    ]
    assert format_list_probabilities(test_list) == formatted_test_list

def test_get_from_list():
    test_list = [
        {"item": "strawberry", "probability": 2},
        {"item": "vanilla", "probability": 3},
        {"item": "chocolate", "probability": 4}
    ]
    assert get_from_list(3, test_list) == {"item": "vanilla", "probability": 3}

def test_deepcopy_list():
    test_list = [
        {"item": "strawberry", "probability": 2},
        {"item": "vanilla", "probability": 3},
        {"item": "chocolate", "probability": 4}
    ]
    new_list = deepcopy_list(test_list)
    test_list[0] = {"item": "strawberry", "probability": 100}
    assert new_list[0]["probability"] != test_list[0]["probability"]

# ------------------------------------------------- #
#                   RandomList Tests                #
# ------------------------------------------------- #

input_list = [
    "vanilla",
    "chocolate",
    {"item": "strawberry", "probability": 2}
]

def test_list_construction():
    random_list = RandomList(input_list)
    offset_list = [
        {"item": "strawberry", "probability": 2},
        {"item": "vanilla", "probability": 3},
        {"item": "chocolate", "probability": 4}
    ]
    assert random_list._offset_contents == offset_list

def test_list_adjust_probability():
    random_list = RandomList(input_list)
    random_list._adjust_probability("strawberry", -1)
    random_list._adjust_probability("vanilla", -1)
    random_list._adjust_probability("chocolate", 3)
    adjusted_list = [
        {"item": "strawberry", "probability": 1},
        {"item": "chocolate", "probability": 5}
    ]
    assert random_list._offset_contents == adjusted_list

def test_list_get_random():
    random_list = RandomList(input_list)
    random_item = random_list.get_random()
    possible_items = ["strawberry", "vanilla", "chocolate"]
    assert (
        random_item in possible_items and
        len(random_list._contents) == 3
    )

def test_list_get_random_and_remove():
    random_list = RandomList(["strawberry", "vanilla", "chocolate"])
    random_item = random_list.get_random_and_remove()
    possible_items = ["strawberry", "vanilla", "chocolate"]
    assert (
        random_item in possible_items and
        len(random_list._contents) == 2
    )

def test_list_reset_contents():
    random_list = RandomList(input_list)
    random_list.get_random_and_remove()
    random_list.reset_contents()
    assert random_list._contents == format_list(input_list)

def test_list_items():
    meat_list = RandomList(["beef", "pork", "chicken"])
    assert meat_list.get_items() == ["beef", "pork", "chicken"]

def test_list_get_contents():
    contents = [
        {"item": "strawberry", "probability": 1},
        {"item": "vanilla", "probability": 1},
        {"item": "chocolate", "probability": 1}
    ]
    random_list = RandomList(contents)
    assert random_list.get_contents() == contents

def test_list_item_count():
    random_list = RandomList(input_list)
    assert random_list.item_count() == 3

# ------------------------------------------------- #
#                 RandomGroup Tests                 #
# ------------------------------------------------- #

def test_group_construction():
    meat_list = RandomList(["beef", "pork", "chicken"])
    veggie_list = RandomList(["carrot", "lettuce", "celery"])

    random_group = RandomGroup([meat_list, veggie_list])
    random_item = random_group.get_random()

    assert random_item in meat_list.get_items() or random_item in veggie_list.get_items()

def test_group_get_list_items():
    meat_list = RandomList(["beef", "pork", "chicken"])
    veggie_list = RandomList(["carrot", "lettuce", "celery"])

    random_group = RandomGroup([meat_list, veggie_list])
    lists = random_group.get_list_items()

    assert lists == [["beef", "pork", "chicken"], ["carrot", "lettuce", "celery"]]

def test_group_get_contents():
    meat_list = RandomList(["beef", "pork", "chicken"])
    veggie_list = RandomList([{
        "item": "carrot",
        "probability": 4
    }])

    random_group = RandomGroup([meat_list, veggie_list])
    contents = random_group.get_contents()

    assert contents == [
        {
            "item": [
                {"item": "beef", "probability": 1},
                {"item": "pork", "probability": 1},
                {"item": "chicken", "probability": 1}
            ],
            "probability": 1
        },
        {
            "item": [{"item": "carrot", "probability": 4}],
            "probability": 1
        }
    ]
