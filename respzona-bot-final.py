async def play_track(query, track_id, context) -> None:
    if track_id not in TRACKS:
        await query.answer("❌ Трек не найден", show_alert=True)
        return

    track = TRACKS[track_id]

    if track['file_id'] is None:
        await query.answer(
            "⚠️ Трек еще не загружен в бота\n\n"
            "1️⃣ Отправь аудиофайл боту\n"
            "2️⃣ Скопируй File ID из ответа\n"
            "3️⃣ Вставь в код TRACKS",
            show_alert=True
        )
    else:
        try:
            # ✅ ОТПРАВЛЯЕМ АУДИО НАПРЯМУЮ
            await context.bot.send_audio(
                chat_id=query.message.chat_id,
                audio=track['file_id'],
                title=track['name'],
                performer='RESPZONA',
                caption=f"🎵 **{track['name']}**\n\n📅 Релиз: {track['date']}\n🎸 Жанр: {track['genre']}"
            )
            await query.answer(f"✅ Отправляю трек: {track['name']}")
            logger.info(f"✅ Трек {track_id} отправлен пользователю {query.message.chat_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки трека: {e}")
            await query.answer(
                f"❌ Ошибка: {str(e)}\n\n"
                "Попробуй позже или напиши в поддержку @respzonachat",
                show_alert=True
            )
