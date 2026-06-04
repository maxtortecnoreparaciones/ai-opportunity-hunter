from backend.ai.scoring_engine import ScoredOffer
from backend.config import settings


class TelegramNotifier:
    def __init__(self, bot_token: str | None = None, chat_id: str | None = None):
        self.bot_token = bot_token or settings.telegram_bot_token
        self.chat_id = chat_id or settings.telegram_chat_id
        self._bot = None

    @property
    def bot(self):
        if self._bot is None:
            try:
                from telegram import Bot
                self._bot = Bot(token=self.bot_token)
            except ImportError:
                raise ImportError("python-telegram-bot no instalado. pip install python-telegram-bot")
        return self._bot

    async def send_opportunity(self, scored: ScoredOffer) -> bool:
        if not self.bot_token or not self.chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID requeridos")

        msg = self._format_message(scored)
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=msg, parse_mode="HTML")
            return True
        except Exception as e:
            print(f"[Telegram] Error enviando notificación: {e}")
            return False

    async def send_daily_summary(self, scored_offers: list[ScoredOffer]) -> bool:
        if not scored_offers:
            return False

        lines = ["<b>Resumen diario de oportunidades</b>\n"]
        for s in scored_offers[:5]:
            lines.append(
                f"• {s.offer.empresa} — {s.offer.cargo}\n"
                f"  Score: {s.score_final}/10 | {s.clasificacion}"
            )

        try:
            await self.bot.send_message(chat_id=self.chat_id, text="\n".join(lines), parse_mode="HTML")
            return True
        except Exception as e:
            print(f"[Telegram] Error enviando resumen: {e}")
            return False

    def _format_message(self, scored: ScoredOffer) -> str:
        o = scored.offer
        return (
            f"🚀 <b>Nueva oportunidad encontrada</b>\n\n"
            f"<b>Empresa:</b> {o.empresa}\n"
            f"<b>Cargo:</b> {o.cargo}\n"
            f"<b>Ubicación:</b> {o.ubicacion}\n"
            f"<b>Score:</b> {scored.score_final}/10 — {scored.clasificacion}\n"
            f"<b>Link:</b> {o.link}\n\n"
            f"<b>Fortalezas:</b> {', '.join(scored.analysis.fortalezas)}\n"
            f"<b>Debilidades:</b> {', '.join(scored.analysis.debilidades)}"
        )
