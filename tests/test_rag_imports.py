import importlib
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class RagImportTests(unittest.TestCase):
    def test_import_rag_modules_without_openai_key(self):
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("OPENAI_EMBEDDING_MODEL", None)

        for module_name in [
            "app.rag.llm",
            "app.rag.embeddings.embeddingProvider",
            "app.rag.config.loadSecrets",
        ]:
            sys.modules.pop(module_name, None)

        llm_module = importlib.import_module("app.rag.llm")
        self.assertTrue(hasattr(llm_module, "generate_answer"))

        embedding_module = importlib.import_module(
            "app.rag.embeddings.embeddingProvider"
        )
        self.assertTrue(hasattr(embedding_module, "get_embedding_model"))


if __name__ == "__main__":
    unittest.main()
