"""
speech/  — Provider-agnostic speech-to-text layer.

Each provider implements the BaseSpeechProvider interface.
The active provider is selected via the SPEECH_PROVIDER env variable.
"""
