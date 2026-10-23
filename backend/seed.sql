-- VoiceLens Multilingual Demo Seed Data
-- Can be imported directly into PostgreSQL:
-- docker exec -i voicelens_postgres psql -U postgres -d speech_transcription < backend/seed.sql

INSERT INTO transcriptions (id, title, transcript, language, duration_seconds, provider, created_at, updated_at)
VALUES
(
    '11111111-1111-4111-8111-111111111101',
    'Sprint Planning — VoiceLens Core Architecture',
    'Welcome everyone to our sprint planning session. Today we are prioritizing the real-time audio chunk streaming pipeline, reducing WebSocket latency to under two hundred milliseconds, and fine-tuning multilingual speech recognition for edge devices.',
    'en',
    38.4,
    'faster_whisper',
    NOW() - INTERVAL '45 minutes',
    NOW() - INTERVAL '45 minutes'
),
(
    '11111111-1111-4111-8111-111111111102',
    'Hinglish Tech Discussion — Microservices & Deployments',
    'Aap frontend deploy karne se pehle please backend API endpoints check kar lena. Docker compose up chalane ke baad database migrations verify karna mat bhoolna, taaki live production mein koi downtime na ho aur services smoothly sync rahein.',
    'hi',
    24.5,
    'faster_whisper',
    NOW() - INTERVAL '2 hours 15 minutes',
    NOW() - INTERVAL '2 hours 15 minutes'
),
(
    '11111111-1111-4111-8111-111111111103',
    'ग्राहक सेवा समीक्षा — Customer Feedback Review',
    'नमस्ते, आज की बैठक में हम नए यूज़र इंटरफ़ेस और बहुभाषी स्पीच ट्रांसक्रिप्शन के प्रदर्शन पर चर्चा करेंगे। सभी ग्राहकों की प्रतिक्रिया सकारात्मक रही है और लेटेंसी काफी कम हो गई है।',
    'hi',
    32.0,
    'faster_whisper',
    NOW() - INTERVAL '5 hours',
    NOW() - INTERVAL '5 hours'
),
(
    '11111111-1111-4111-8111-111111111104',
    'Demostración de Producto — Inteligencia Artificial de Voz',
    'Hola a todos. Hoy presentamos el sistema de reconocimiento de voz multilingüe en tiempo real. Esta solución permite transcribir conferencias y reuniones internacionales de forma instantánea con alta precisión y baja latencia.',
    'es',
    29.8,
    'faster_whisper',
    NOW() - INTERVAL '11 hours',
    NOW() - INTERVAL '11 hours'
),
(
    '11111111-1111-4111-8111-111111111105',
    'Point Stratégique — Expansion Internationale',
    'Bonjour à tous. Lors de cette réunion, nous faisons le point sur le déploiement de notre infrastructure cloud. La transcription automatisée offre un gain de productivité majeur pour l''ensemble des équipes réparties en Europe.',
    'fr',
    41.2,
    'faster_whisper',
    NOW() - INTERVAL '1 day 2 hours',
    NOW() - INTERVAL '1 day 2 hours'
),
(
    '11111111-1111-4111-8111-111111111106',
    'Technologie-Architektur — Hochverfügbare Systeme',
    'Guten Tag zusammen. Wir haben die Latenzzeiten der Transkriptions-Pipeline analysiert und festgestellt, dass die Optimierung des Modells auf Int-8 Genauigkeit die Verarbeitungszeit um vierzig Prozent ohne Genauigkeitsverlust reduziert.',
    'de',
    35.7,
    'faster_whisper',
    NOW() - INTERVAL '1 day 8 hours',
    NOW() - INTERVAL '1 day 8 hours'
),
(
    '11111111-1111-4111-8111-111111111107',
    'プロダクト開発会議 — 音声認識モデルの改善',
    '皆様、お疲れ様です。本日の定例ミーティングでは、次世代の多言語音声認識エンジンの精度検証結果についてご報告します。特にノイズキャンセリング機能とリアルタイム推論速度の強化が期待されています。',
    'ja',
    28.3,
    'faster_whisper',
    NOW() - INTERVAL '2 days 1 hour',
    NOW() - INTERVAL '2 days 1 hour'
),
(
    '11111111-1111-4111-8111-111111111108',
    'குரல் அறிதல் திட்ட மதிப்பாய்வு — Voice Project Review',
    'வணக்கம், எங்களின் பலமொழி குரல்-எழுத்து மாற்றி திட்டம் வெற்றிகரமாக செயல்படுத்தப்பட்டுள்ளது. இந்த புதிய தொழில்நுட்பம் மூலம் பயனர்கள் தங்கள் தாய்மொழியில் எளிதாக பேசலாம் மற்றும் துல்லியமான உரையை உடனடியாக பெறலாம்.',
    'ta',
    26.5,
    'faster_whisper',
    NOW() - INTERVAL '2 days 7 hours',
    NOW() - INTERVAL '2 days 7 hours'
),
(
    '11111111-1111-4111-8111-111111111109',
    'المؤتمر الطبي — تحويل الصوت إلى نصوص في الرعاية الصحية',
    'أهلاً بكم في هذا العرض التقديمي. تتيح تقنيات الذكاء الاصطناعي الحديثة للأطباء توثيق السجلات الطبية بالصوت مباشرة وبدقة متناهية، مما يختصر الوقت ويحسن جودة رعاية المرضى في كافة المستشفيات.',
    'ar',
    34.1,
    'faster_whisper',
    NOW() - INTERVAL '3 days 3 hours',
    NOW() - INTERVAL '3 days 3 hours'
),
(
    '11111111-1111-4111-8111-111111111110',
    '人工智能语音算法研究 — 多语言混合识别',
    '大家下午好。今天我们主要讨论多语言混合语音识别模型的优化方案。通过引入最新的量化推断技术，模型的实时推理速度和显存占用都得到了显著提升，同时保持了高准确率。',
    'zh',
    31.6,
    'faster_whisper',
    NOW() - INTERVAL '3 days 10 hours',
    NOW() - INTERVAL '3 days 10 hours'
),
(
    '11111111-1111-4111-8111-111111111111',
    'Clinical Note — Patient Consultation & Follow-up',
    'Patient presents with mild respiratory congestion and seasonal allergies. Vital signs are stable with blood pressure 120 over 80. Recommended hydration, standard antihistamines for five days, and a follow-up consultation next Tuesday if symptoms persist.',
    'en',
    45.0,
    'faster_whisper',
    NOW() - INTERVAL '4 days 4 hours',
    NOW() - INTERVAL '4 days 4 hours'
),
(
    '11111111-1111-4111-8111-111111111112',
    'Apresentação de Inovação — Transcrição Contínua',
    'Olá pessoal, bem-vindos à apresentação do VoiceLens. Com o processamento local e seguro, oferecemos transcrição de voz para texto em tempo real sem expor dados confidenciais a provedores externos.',
    'pt',
    22.4,
    'faster_whisper',
    NOW() - INTERVAL '5 days 2 hours',
    NOW() - INTERVAL '5 days 2 hours'
),
(
    '11111111-1111-4111-8111-111111111113',
    'Voice Note — Grocery & Weekly Errands',
    'Pick up fresh fruit, almond milk, and ground coffee from the organic market. Remember to back up the project database and review pending pull requests before Sunday evening.',
    'en',
    14.8,
    'mock',
    NOW() - INTERVAL '6 days 1 hour',
    NOW() - INTERVAL '6 days 1 hour'
),
(
    '11111111-1111-4111-8111-111111111114',
    'Executive Summary — Quarterly Product Metrics',
    'During the third quarter, user engagement increased by thirty-five percent following the introduction of multilingual voice search. Active transcription sessions reached over one million minutes with an overall word error rate below four percent across primary languages.',
    'en',
    52.3,
    'faster_whisper',
    NOW() - INTERVAL '7 days 5 hours',
    NOW() - INTERVAL '7 days 5 hours'
)
ON CONFLICT (id) DO NOTHING;
