"""Core MCP Streaming Schema Validator implementation."""
from typing import Dict, Any, Optional


class ValidationResult:
    def __init__(self, is_valid: bool, error: Optional[str] = None):
        self.is_valid = is_valid
        self.error = error


class MCPStreamingSchemaValidator:
    def validate_message(self, msg: Dict[str, Any]) -> ValidationResult:
        # 1. JSON-RPC 2.0 version check
        if msg.get("jsonrpc") != "2.0":
            return ValidationResult(False, "Missing or invalid 'jsonrpc' field (must be '2.0')")

        # 2. Check if request, response, or notification
        has_method = "method" in msg
        has_result = "result" in msg
        has_error = "error" in msg
        has_id = "id" in msg

        if has_method:
            # Request or Notification
            if not isinstance(msg["method"], str) or not msg["method"].strip():
                return ValidationResult(False, "Field 'method' must be a non-empty string")
            if "params" in msg and not isinstance(msg["params"], (dict, list)):
                return ValidationResult(False, "Field 'params' must be an object or array")
            return ValidationResult(True)

        elif has_result or has_error:
            # Response
            if not has_id:
                return ValidationResult(False, "Response must include an 'id' field matching request")
            if has_result and has_error:
                return ValidationResult(False, "Response cannot contain both 'result' and 'error'")
            if has_error and not isinstance(msg["error"], dict):
                return ValidationResult(False, "Field 'error' must be an object")
            return ValidationResult(True)

        return ValidationResult(False, "Message is neither a valid JSON-RPC request nor response")
