def test(t):
  with t("Maps a function onto a list"):
    (t
      @{
        "it": "works with round",
        "i": (round, [0.6, 0.7, 73.4, 100]),
        "e": [1, 1, 73, 100]
      }
      @{
        "it": "works with float",
        "i": (float, [0.0, 15, "1.5"]),
        "e": [0.0, 15.0, 1.5]
      }
      @{
      "it": "i screwed up this test",
      "i": (float, []),
      "e": ["oops"]
      }
    )
    with t("Leaves an empty list unchanged"):
      (t
        @{
          "it": "works with round",
          "i": (round, []),
          "e": []
        }
        @{
          "it": "works with float",
          "i": (float, []),
          "e": []
        }
      )

