"""
seed.py — Populate the database with realistic multilingual transcription records.

Usage:
  # Inside backend directory or via host:
  python seed.py

  # Via Docker:
  docker exec voicelens_backend python seed.py

  # Clear existing records and reseed:
  python seed.py --clear

  # Force seeding via REST API:
  python seed.py --api
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path so 'app' imports work
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

NOW = datetime.now(timezone.utc)

SEED_ITEMS = [
    {
        "id": "11111111-1111-4111-8111-111111111101",
        "title": "Sprint Planning — VoiceLens Core Architecture",
        "transcript": (
            "Welcome everyone to our sprint planning session. Today we are prioritizing "
            "the real-time audio chunk streaming pipeline, reducing WebSocket latency to under "
            "two hundred milliseconds, and fine-tuning multilingual speech recognition for edge devices."
        ),
        "language": "en",
        "duration_seconds": 38.4,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(minutes=45),
        "updated_at": NOW - timedelta(minutes=45),
    },
    {
        "id": "11111111-1111-4111-8111-111111111102",
        "title": "Hinglish Tech Discussion — Microservices & Deployments",
        "transcript": (
            "Aap frontend deploy karne se pehle please backend API endpoints check kar lena. "
            "Docker compose up chalane ke baad database migrations verify karna mat bhoolna, "
            "taaki live production mein koi downtime na ho aur services smoothly sync rahein."
        ),
        "language": "hi",
        "duration_seconds": 24.5,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(hours=2, minutes=15),
        "updated_at": NOW - timedelta(hours=2, minutes=15),
    },
    {
        "id": "11111111-1111-4111-8111-111111111103",
        "title": "ग्राहक सेवा समीक्षा — Customer Feedback Review",
        "transcript": (
            "नमस्ते, आज की बैठक में हम नए यूज़र इंटरफ़ेस और बहुभाषी स्पीच ट्रांसक्रिप्शन के "
            "प्रदर्शन पर चर्चा करेंगे। सभी ग्राहकों की प्रतिक्रिया सकारात्मक रही है और लेटेंसी काफी कम हो गई है।"
        ),
        "language": "hi",
        "duration_seconds": 32.0,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(hours=5),
        "updated_at": NOW - timedelta(hours=5),
    },
    {
        "id": "11111111-1111-4111-8111-111111111104",
        "title": "Demostración de Producto — Inteligencia Artificial de Voz",
        "transcript": (
            "Hola a todos. Hoy presentamos el sistema de reconocimiento de voz multilingüe "
            "en tiempo real. Esta solución permite transcribir conferencias y reuniones "
            "internacionales de forma instantánea con alta precisión y baja latencia."
        ),
        "language": "es",
        "duration_seconds": 29.8,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(hours=11),
        "updated_at": NOW - timedelta(hours=11),
    },
    {
        "id": "11111111-1111-4111-8111-111111111105",
        "title": "Point Stratégique — Expansion Internationale",
        "transcript": (
            "Bonjour à tous. Lors de cette réunion, nous faisons le point sur le déploiement "
            "de notre infrastructure cloud. La transcription automatisée offre un gain de "
            "productivité majeur pour l'ensemble des équipes réparties en Europe."
        ),
        "language": "fr",
        "duration_seconds": 41.2,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=1, hours=2),
        "updated_at": NOW - timedelta(days=1, hours=2),
    },
    {
        "id": "11111111-1111-4111-8111-111111111106",
        "title": "Technologie-Architektur — Hochverfügbare Systeme",
        "transcript": (
            "Guten Tag zusammen. Wir haben die Latenzzeiten der Transkriptions-Pipeline "
            "analysiert und festgestellt, dass die Optimierung des Modells auf Int-8 Genauigkeit "
            "die Verarbeitungszeit um vierzig Prozent ohne Genauigkeitsverlust reduziert."
        ),
        "language": "de",
        "duration_seconds": 35.7,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=1, hours=8),
        "updated_at": NOW - timedelta(days=1, hours=8),
    },
    {
        "id": "11111111-1111-4111-8111-111111111107",
        "title": "プロダクト開発会議 — 音声認識モデルの改善",
        "transcript": (
            "皆様、お疲れ様です。本日の定例ミーティングでは、次世代の多言語音声認識エンジンの"
            "精度検証結果についてご報告します。特にノイズキャンセリング機能とリアルタイム推論速度の"
            "強化が期待されています。"
        ),
        "language": "ja",
        "duration_seconds": 28.3,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=2, hours=1),
        "updated_at": NOW - timedelta(days=2, hours=1),
    },
    {
        "id": "11111111-1111-4111-8111-111111111108",
        "title": "குரல் அறிதல் திட்ட மதிப்பாய்வு — Voice Project Review",
        "transcript": (
            "வணக்கம், எங்களின் பலமொழி குரல்-எழுத்து மாற்றி திட்டம் வெற்றிகரமாக செயல்படுத்தப்பட்டுள்ளது. "
            "இந்த புதிய தொழில்நுட்பம் மூலம் பயனர்கள் தங்கள் தாய்மொழியில் எளிதாக பேசலாம் மற்றும் துல்லியமான "
            "உரையை உடனடியாக பெறலாம்."
        ),
        "language": "ta",
        "duration_seconds": 26.5,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=2, hours=7),
        "updated_at": NOW - timedelta(days=2, hours=7),
    },
    {
        "id": "11111111-1111-4111-8111-111111111109",
        "title": "المؤتمر الطبي — تحويل الصوت إلى نصوص في الرعاية الصحية",
        "transcript": (
            "أهلاً بكم في هذا العرض التقديمي. تتيح تقنيات الذكاء الاصطناعي الحديثة للأطباء توثيق السجلات الطبية "
            "بالصوت مباشرة وبدقة متناهية، مما يختصر الوقت ويحسن جودة رعاية المرضى في كافة المستشفيات."
        ),
        "language": "ar",
        "duration_seconds": 34.1,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=3, hours=3),
        "updated_at": NOW - timedelta(days=3, hours=3),
    },
    {
        "id": "11111111-1111-4111-8111-111111111110",
        "title": "人工智能语音算法研究 — 多语言混合识别",
        "transcript": (
            "大家下午好。今天我们主要讨论多语言混合语音识别模型的优化方案。通过引入最新的量化推断技术，"
            "模型的实时推理速度和显存占用都得到了显著提升，同时保持了高准确率。"
        ),
        "language": "zh",
        "duration_seconds": 31.6,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=3, hours=10),
        "updated_at": NOW - timedelta(days=3, hours=10),
    },
    {
        "id": "11111111-1111-4111-8111-111111111111",
        "title": "Clinical Note — Patient Consultation & Follow-up",
        "transcript": (
            "Patient presents with mild respiratory congestion and seasonal allergies. "
            "Vital signs are stable with blood pressure 120 over 80. Recommended hydration, "
            "standard antihistamines for five days, and a follow-up consultation next Tuesday if symptoms persist."
        ),
        "language": "en",
        "duration_seconds": 45.0,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=4, hours=4),
        "updated_at": NOW - timedelta(days=4, hours=4),
    },
    {
        "id": "11111111-1111-4111-8111-111111111112",
        "title": "Apresentação de Inovação — Transcrição Contínua",
        "transcript": (
            "Olá pessoal, bem-vindos à apresentação do VoiceLens. Com o processamento local e seguro, "
            "oferecemos transcrição de voz para texto em tempo real sem expor dados confidenciais a provedores externos."
        ),
        "language": "pt",
        "duration_seconds": 22.4,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=5, hours=2),
        "updated_at": NOW - timedelta(days=5, hours=2),
    },
    {
        "id": "11111111-1111-4111-8111-111111111113",
        "title": "Voice Note — Grocery & Weekly Errands",
        "transcript": (
            "Pick up fresh fruit, almond milk, and ground coffee from the organic market. "
            "Remember to back up the project database and review pending pull requests before Sunday evening."
        ),
        "language": "en",
        "duration_seconds": 14.8,
        "provider": "mock",
        "created_at": NOW - timedelta(days=6, hours=1),
        "updated_at": NOW - timedelta(days=6, hours=1),
    },
    {
        "id": "11111111-1111-4111-8111-111111111114",
        "title": "Executive Summary — Quarterly Product Metrics",
        "transcript": (
            "During the third quarter, user engagement increased by thirty-five percent following "
            "the introduction of multilingual voice search. Active transcription sessions reached over "
            "one million minutes with an overall word error rate below four percent across primary languages."
        ),
        "language": "en",
        "duration_seconds": 52.3,
        "provider": "faster_whisper",
        "created_at": NOW - timedelta(days=7, hours=5),
        "updated_at": NOW - timedelta(days=7, hours=5),
    },
]


def seed_via_db(clear: bool = False) -> bool:
    """Seed data directly using SQLAlchemy and the application database session."""
    try:
        from app.database import Base, SessionLocal, engine
        from app.models import Transcription

        # Ensure tables exist
        Base.metadata.create_all(bind=engine)

        with SessionLocal() as db:
            if clear:
                deleted = db.query(Transcription).delete()
                db.commit()
                print(f"🗑️  Cleared {deleted} existing transcription record(s).")

            count = 0
            for item in SEED_ITEMS:
                # Check if item ID or identical title already exists
                existing = db.get(Transcription, item["id"])
                if existing:
                    print(f"  ⏭️  Skipping existing record: {item['title'][:40]}...")
                    continue

                rec = Transcription(
                    id=item["id"],
                    title=item["title"],
                    transcript=item["transcript"],
                    language=item["language"],
                    duration_seconds=item["duration_seconds"],
                    provider=item["provider"],
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                )
                db.add(rec)
                count += 1

            db.commit()
            total_in_db = db.query(Transcription).count()
            print(f"✅ Successfully seeded {count} new record(s) via Database.")
            print(f"📊 Total transcriptions now in DB: {total_in_db}")
            return True

    except Exception as e:
        print(f"⚠️  Direct database seeding failed or unavailable: {e}")
        return False


def seed_via_api(api_url: str = "http://localhost:8000/api/transcriptions") -> bool:
    """Seed data by sending POST requests to the backend REST API."""
    print(f"🌐 Attempting to seed via REST API: {api_url} ...")
    success_count = 0

    for item in SEED_ITEMS:
        payload = {
            "title": item["title"],
            "transcript": item["transcript"],
            "language": item["language"],
            "duration_seconds": item["duration_seconds"],
            "provider": item["provider"],
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            api_url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status in (200, 201):
                    success_count += 1
                    print(f"  ✓ Added: {item['title'][:40]}...")
                else:
                    print(f"  ✗ Status {response.status} for: {item['title'][:40]}")
        except urllib.error.HTTPError as err:
            print(f"  ✗ HTTP {err.code}: {err.reason} for {item['title'][:40]}")
        except Exception as err:
            print(f"  ✗ Connection error: {err}")
            return False

    print(f"✅ Successfully created {success_count}/{len(SEED_ITEMS)} record(s) via REST API.")
    return success_count > 0


def main():
    parser = argparse.ArgumentParser(description="Seed VoiceLens database with multilingual demo data.")
    parser.add_argument("--clear", action="store_true", help="Delete existing transcriptions before seeding")
    parser.add_argument("--api", action="store_true", help="Force seeding through REST API")
    parser.add_argument("--api-url", default="http://localhost:8000/api/transcriptions", help="Custom API endpoint")
    args = parser.parse_args()

    print("══════════════════════════════════════════════════════════════")
    print("🎙️   VoiceLens — Database Seeding Script")
    print(f"📦 Total seed records defined: {len(SEED_ITEMS)}")
    print("══════════════════════════════════════════════════════════════")

    if args.api:
        ok = seed_via_api(args.api_url)
        if not ok:
            sys.exit(1)
        return

    # Try DB directly first
    ok = seed_via_db(clear=args.clear)
    if not ok:
        print("🔄 Falling back to REST API seeding...")
        ok = seed_via_api(args.api_url)
        if not ok:
            print("❌ Both direct DB and REST API seeding failed.")
            sys.exit(1)

    print("\n🎉 Seeding completed successfully!")


if __name__ == "__main__":
    main()
