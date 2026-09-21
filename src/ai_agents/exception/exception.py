# """Custom exceptions for the AI pipeline.

# This module provides `BasePipelineException`, a lightweight, production-ready
# exception suitable for AI/LLM pipelines. It captures file/line context from
# tracebacks, preserves wrapped exceptions, stores an optional context dict,
# and exposes formatted traceback strings for logging.
# """
# from __future__ import annotations

# import traceback
# from typing import Any, Dict, Optional


# class BasePipelineException(Exception):
# 	"""Base exception for the AI pipeline.

# 	Features:
# 	- Captures filename and lineno where the original exception occurred.
# 	- Preserves the original (wrapped) exception instance.
# 	- Extracts the full traceback string for logging.
# 	- Accepts an optional `context` dict for structured metadata.
# 	- Provides compact, logger-friendly `__str__` and `__repr__`.
# 	"""

# 	def __init__(
# 		self,
# 		message: str,
# 		*,
# 		cause: Optional[BaseException] = None,
# 		context: Optional[Dict[str, Any]] = None,
# 	) -> None:
# 		super().__init__(message)
# 		self.message = message
# 		self.cause = cause
# 		self.context = context or {}

# 		# Attempt to extract originating filename/lineno from cause traceback,
# 		# falling back to the current frame if no cause provided.
# 		tb = None
# 		if cause is not None:
# 			tb = cause.__traceback__
# 		else:
# 			# Create a traceback from the current exception stack
# 			tb = None

# 		if tb is not None:
# 			# Walk to the last frame of the traceback (origin of exception)
# 			last_tb = tb
# 			while last_tb.tb_next is not None:
# 				last_tb = last_tb.tb_next
# 			frame = last_tb.tb_frame
# 			self.filename = frame.f_code.co_filename
# 			self.lineno = last_tb.tb_lineno
# 			self.traceback_str = "".join(traceback.format_exception(type(cause), cause, tb))
# 		else:
# 			# No cause provided — capture a short traceback from here
# 			stack = traceback.extract_stack()[:-1]
# 			if stack:
# 				origin = stack[-1]
# 				self.filename = origin.filename
# 				self.lineno = origin.lineno
# 			else:
# 				self.filename = "<unknown>"
# 				self.lineno = 0
# 			self.traceback_str = "".join(traceback.format_stack())

# 	def to_dict(self) -> Dict[str, Any]:
# 		"""Return a serializable dict useful for structured logging."""

# 		return {
# 			"message": self.message,
# 			"filename": self.filename,
# 			"lineno": self.lineno,
# 			"context": self.context,
# 			"cause": repr(self.cause) if self.cause is not None else None,
# 			"traceback": self.traceback_str,
# 		}

# 	def __str__(self) -> str:
# 		parts = [f"{self.__class__.__name__}: {self.message}"]
# 		parts.append(f"at {self.filename}:{self.lineno}")
# 		if self.context:
# 			parts.append(f"context={self.context}")
# 		if self.cause:
# 			parts.append(f"cause={self.cause!r}")
# 		return " | ".join(parts)

# 	def __repr__(self) -> str:
# 		return f"{self.__class__.__name__}({self.message!r}, cause={self.cause!r}, context={self.context!r})"




import sys
import traceback
from typing import Optional, cast

class ResearchAnalystException(Exception):
    def __init__(self, error_message, error_details: Optional[object] = None):
        
        # Normalize message
        if isinstance(error_message, BaseException):
            norm_msg = str(error_message)
        else:
            norm_msg = str(error_message)

        # Resolve exc_info (supports: sys module, Exception object, or current context)
        exc_type = exc_value = exc_tb = None
        if error_details is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        else:
            if hasattr(error_details, "exc_info"):  # e.g., sys
                exc_info_obj = cast(sys, error_details)
                exc_type, exc_value, exc_tb = exc_info_obj.exc_info()
            elif isinstance(error_details, BaseException):
                exc_type, exc_value, exc_tb = type(error_details), error_details, error_details.__traceback__
            else:
                exc_type, exc_value, exc_tb = sys.exc_info()

        # Walk to the last frame to report the most relevant location
        last_tb = exc_tb
        while last_tb and last_tb.tb_next:
            last_tb = last_tb.tb_next

        self.file_name = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
        self.lineno = last_tb.tb_lineno if last_tb else -1
        self.error_message = norm_msg

        # Full pretty traceback (if available)
        if exc_type and exc_tb:
            self.traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback_str = ""

        super().__init__(self.__str__())

    def __str__(self):
        # Compact, logger-friendly message (no leading spaces)
        base = f"Error in [{self.file_name}] at line [{self.lineno}] | Message: {self.error_message}"
        if self.traceback_str:
            return f"{base}\nTraceback:\n{self.traceback_str}"
        return base

    def __repr__(self):
        return f"ResearchAnalystException(file={self.file_name!r}, line={self.lineno}, message={self.error_message!r})"


if __name__ == "__main__":
    # Demo-1: generic exception -> wrap
    try:
        a = 1 / 0
    except Exception as e:
        raise ResearchAnalystException("Division failed", e) from e

    # Demo-2: still supports sys (old pattern)
    # try:
    #     a = int("abc")
    # except Exception as e:
    #     raise ResearchAnalystException(e, sys)
    
    
    # BaseException
    # ├── Exception
    # │     ├── ValueError
    # │     ├── TypeError
    # │     ├── KeyError
    # │     └── ...
    # ├── SystemExit
    # ├── KeyboardInterrupt

# validation error tha?
# config missing tha?
# LLM API down tha?
# embedding fail hua?
# vector DB fail hua?

# 👉 Matlab: unexpected / unhandled errors ko wrap karke clean error banana.


# Create a Python base custom exception class for a production AI/LLM pipeline that:
# Captures file name and line number from traceback
# Supports wrapping original exceptions
# Extracts full traceback string
# Accepts optional context dictionary (like user_id, model_name, db_name)
# Formats error message in a compact, logger-friendly format
# Includes str and repr methods