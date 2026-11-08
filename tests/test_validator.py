"""Unit tests for mcp-streaming-schema-validator."""
import unittest
from mcp_streaming_schema_validator.validator import MCPStreamingSchemaValidator


class TestMCPStreamingSchemaValidator(unittest.TestCase):
    def test_valid_request(self):
        v = MCPStreamingSchemaValidator()
        res = v.validate_message({"jsonrpc": "2.0", "id": "req-1", "method": "tools/list"})
        self.assertTrue(res.is_valid)

    def test_invalid_jsonrpc_version(self):
        v = MCPStreamingSchemaValidator()
        res = v.validate_message({"jsonrpc": "2.1", "id": 1, "method": "test"})
        self.assertFalse(res.is_valid)
        self.assertIn("jsonrpc", res.error)

    def test_valid_response(self):
        v = MCPStreamingSchemaValidator()
        res = v.validate_message({"jsonrpc": "2.0", "id": "req-1", "result": {"status": "ok"}})
        self.assertTrue(res.is_valid)
