def test(t, _):
    with t("Reduces something"):
         t@{
             "it": "works",
             "i": (lambda a, b: a + b, 0, [1, 2, 3, 4]),
             "e": 10
         }

