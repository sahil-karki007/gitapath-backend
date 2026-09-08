import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geeta.settings')
django.setup()

from api.models import Chapter, Verse

chapters_data = [
    {"number": 1, "name": "Arjuna Vishada Yoga", "sanskrit_name": "अर्जुन विषाद योग", "description": "Arjun ka dard aur confusion on the battlefield", "total_verses": 47},
    {"number": 2, "name": "Sankhya Yoga", "sanskrit_name": "साँख्य योग", "description": "Aatma amar hai, duty karo", "total_verses": 72},
    {"number": 3, "name": "Karma Yoga", "sanskrit_name": "कर्म योग", "description": "Bina fal soche kaam karo", "total_verses": 43},
    {"number": 4, "name": "Jnana Karma Sanyasa Yoga", "sanskrit_name": "ज्ञान कर्म संन्यास योग", "description": "Gyaan aur action ka balance", "total_verses": 42},
    {"number": 5, "name": "Karma Sanyasa Yoga", "sanskrit_name": "कर्म संन्यास योग", "description": "Kaam karo ya chhodo?", "total_verses": 29},
    {"number": 6, "name": "Dhyana Yoga", "sanskrit_name": "ध्यान योग", "description": "Meditation kaise karte hain", "total_verses": 47},
    {"number": 7, "name": "Jnana Vijnana Yoga", "sanskrit_name": "ज्ञान विज्ञान योग", "description": "Bhagwan ka asli roop", "total_verses": 30},
    {"number": 8, "name": "Aksara Brahma Yoga", "sanskrit_name": "अक्षर ब्रह्म योग", "description": "Marne ke waqt kya socho", "total_verses": 28},
    {"number": 9, "name": "Raja Vidya Yoga", "sanskrit_name": "राज विद्या योग", "description": "Sabse bada gyaan — bhakti", "total_verses": 34},
    {"number": 10, "name": "Vibhuti Yoga", "sanskrit_name": "विभूति योग", "description": "Krishna ka vaibhav", "total_verses": 42},
    {"number": 11, "name": "Vishwarupa Darshana Yoga", "sanskrit_name": "विश्वरूप दर्शन योग", "description": "Cosmic form dekha Arjun ne", "total_verses": 55},
    {"number": 12, "name": "Bhakti Yoga", "sanskrit_name": "भक्ति योग", "description": "Pyaar se bhajao", "total_verses": 20},
    {"number": 13, "name": "Kshetra Kshetrajna Vibhaga Yoga", "sanskrit_name": "क्षेत्र क्षेत्रज्ञ विभाग योग", "description": "Body aur Soul alag hain", "total_verses": 34},
    {"number": 14, "name": "Gunatraya Vibhaga Yoga", "sanskrit_name": "गुणत्रय विभाग योग", "description": "Teen gunas — Sattva Rajas Tamas", "total_verses": 27},
    {"number": 15, "name": "Purushottama Yoga", "sanskrit_name": "पुरुषोत्तम योग", "description": "Sabse upar — Bhagwan", "total_verses": 20},
    {"number": 16, "name": "Daivasura Sampad Vibhaga Yoga", "sanskrit_name": "दैवासुर सम्पद् विभाग योग", "description": "Devta wale ya Asur wale qualities", "total_verses": 24},
    {"number": 17, "name": "Shraddhatraya Vibhaga Yoga", "sanskrit_name": "श्रद्धात्रय विभाग योग", "description": "Teen tarah ki shraddha", "total_verses": 28},
    {"number": 18, "name": "Moksha Sanyasa Yoga", "sanskrit_name": "मोक्ष संन्यास योग", "description": "Last lesson — sab Bhagwan ko de do", "total_verses": 78},
]

def seed():
    print("Seeding chapters...")
    for ch in chapters_data:
        chapter, created = Chapter.objects.update_or_create(
            number=ch['number'],
            defaults=ch
        )
        print(f"  {'✅' if created else '🔄'} Chapter {ch['number']} - {ch['name']}")

    print("\nSeeding verses from API...")
    for chapter_num in range(1, 19):
        try:
            chapter = Chapter.objects.get(number=chapter_num)
            for verse_num in range(1, 80):
                try:
                    v_res = requests.get(
                        f"https://vedicscriptures.github.io/slok/{chapter_num}/{verse_num}/",
                        timeout=10
                    )
                    if v_res.status_code != 200:
                        break
                    v_data = v_res.json()
                    sanskrit = v_data.get('slok', '')
                    if not sanskrit:
                        break
                    hindi = v_data.get('pur', {}).get('purport', '') or v_data.get('tej', {}).get('ht', '') or ''
                    english = v_data.get('siva', {}).get('et', '') or v_data.get('prabhu', {}).get('et', '') or ''
                    verse, created = Verse.objects.get_or_create(
                        chapter=chapter,
                        verse_number=verse_num,
                        defaults={
                            'sanskrit': sanskrit,
                            'hindi': hindi,
                            'english': english,
                            'hinglish': english,
                        }
                    )
                    print(f"  {'✅' if created else '⏭️'} Ch{chapter_num} V{verse_num}")
                except Exception as e:
                    print(f"  ❌ Ch{chapter_num} V{verse_num}: {e}")
                    break
        except Exception as e:
            print(f"❌ Chapter {chapter_num}: {e}")

    print("\n🎉 Seed complete!")

if __name__ == '__main__':
    seed()