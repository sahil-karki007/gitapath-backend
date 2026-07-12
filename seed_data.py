import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geeta.settings')
django.setup()

from api.models import Chapter, Verse

def seed():
    print("📖 Fetching all chapters from Gita API...")

    for chapter_num in range(1, 19):
        print(f"\n📚 Chapter {chapter_num} fetch ho raha hai...")

        # Fetch chapter info
        ch_res = requests.get(f"https://bhagavad-gita3.p.rapidapi.com/v2/chapters/{chapter_num}/",
            headers={
                "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
                "X-RapidAPI-Host": "bhagavad-gita3.p.rapidapi.com"
            }
        )

        # Fetch verses from free API
        verses_res = requests.get(
            f"https://vedicscriptures.github.io/slok/{chapter_num}/1/",
        )

        try:
            chapter_obj, created = Chapter.objects.get_or_create(
                number=chapter_num,
                defaults={
                    'name': f"Chapter {chapter_num}",
                    'sanskrit_name': '',
                    'description': '',
                    'total_verses': 0,
                }
            )
            print(f"  {'✅ Created' if created else '⏭️  Exists'}: Chapter {chapter_num}")
        except Exception as e:
            print(f"  ❌ Chapter error: {e}")
            continue

        # Fetch all verses
        for verse_num in range(1, 80):
            try:
                v_res = requests.get(f"https://vedicscriptures.github.io/slok/{chapter_num}/{verse_num}/")
                if v_res.status_code != 200:
                    break

                v_data = v_res.json()

                sanskrit = v_data.get('slok', '')
                hindi = v_data.get('pur', {}).get('purport', '') or v_data.get('tej', {}).get('ht', '') or ''
                english = v_data.get('siva', {}).get('et', '') or v_data.get('prabhu', {}).get('et', '') or ''
                hinglish = english

                if not sanskrit:
                    break

                verse, created = Verse.objects.get_or_create(
                    chapter=chapter_obj,
                    verse_number=verse_num,
                    defaults={
                        'sanskrit': sanskrit,
                        'hindi': hindi,
                        'english': english,
                        'hinglish': hinglish,
                    }
                )
                print(f"  {'✅' if created else '⏭️ '} Verse {verse_num}")

            except Exception as e:
                print(f"  ❌ Verse {verse_num} error: {e}")
                break

    print("\n🎉 Poori Bhagavad Gita seed ho gayi!")

if __name__ == '__main__':
    seed()