"""AI service behind the "Enhance Issue Description" feature.

Only the mock provider is implemented. A real provider (Gemini/OpenAI) would be
another branch in `enhance_description` reading its key from settings.AI_API_KEY.
"""

from app.schemas.issue import EnhanceResponse


class AIService:
    def enhance_description(self, title: str, description: str) -> EnhanceResponse:
        # Only the mock provider is wired up today; a real one (Gemini/OpenAI)
        # would branch on settings.AI_PROVIDER here.
        return self._enhance_mock(title, description)

    def _enhance_mock(self, title: str, description: str) -> EnhanceResponse:
        enhanced = (
            f"**Summary**\n{title.strip()}\n\n"
            f"**Details**\n{description.strip()}\n\n"
            "**Steps to Reproduce**\n1. \n2. \n3. \n\n"
            "**Expected Behavior**\n\n"
            "**Actual Behavior**\n"
        )
        return EnhanceResponse(enhanced_description=enhanced, provider="mock")
