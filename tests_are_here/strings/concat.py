def test(t, m):
    t@{
        "matcher": "plain",
        "it": "matcher.plain works",
        "i": m["concat"](m["HELLO"], m["WORLD"]),
        "e": "HELLOWORLD"
    }@{
        "matcher": "compare",
        "it": "matcher.compare works",
        "e": m["concat"]
    }
