from deepgram import DeepgramClient
from config import settings


def transcribe_deepgram(audio_bytes: bytes, mime_type: str) -> str:
    try:
        deepgram = DeepgramClient(api_key=settings.DEEPGRAM_API_KEY)
        response = deepgram.listen.v1.media.transcribe_file(
            request=audio_bytes,
            model="nova-3",
            smart_format=True,
            language="ru-RU",
        )

        return response.results.channels[0].alternatives[0].transcript

    except Exception as e:
        raise RuntimeError(f"Deepgram client error: {e}") from e
    except Exception as e:
        print(f"Exception: {e}")
