from types import SimpleNamespace

import app.ask as ask_module


def test_ask_prints_token_counts_and_returns_response_text(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(
            prompt_token_count=12,
            candidates_token_count=34,
        ),
    )

    class FakeModels:
        def generate_content(self, **kwargs):
            return response

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    perf_counter_values = iter([10.0, 11.23])
    monkeypatch.setattr(ask_module.time, "perf_counter", lambda: next(perf_counter_values))

    result = ask_module.ask("質問")

    assert result == "回答"
    assert capsys.readouterr().out.strip() == (
        "[トークン] 入力: 12, 出力: 34, 応答時間: 1.23秒"
    )