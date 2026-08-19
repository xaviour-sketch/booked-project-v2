"""Import real books (with cover images) from the Open Library API into
the Booked database.

Open Library's Subjects API is public and requires no API key:
  https://openlibrary.org/subjects/{subject}.json?limit=N

Run with:
    python -m app.seed_open_library

This is additive: it will not duplicate a book that already exists
(matched by title + author), so it's safe to re-run.
"""
import random
import time
import requests

from app import create_app
from app.extensions import db
from app.models import Book

# Open Library subject slugs -> the genre label we store on our Book model
SUBJECTS = {
    "fiction": "Fiction",
    "fantasy": "Fantasy",
    "science_fiction": "Science Fiction",
    "mystery": "Mystery",
    "romance": "Romance",
    "nonfiction": "Non-Fiction",
    "biography": "Biography",
    "self_help": "Self-Help",
    "history": "History",
    "thriller": "Thriller",
}

BOOKS_PER_SUBJECT = 35  # 10 subjects x 35 = ~350 books before de-duplication
REQUEST_DELAY_SECONDS = 0.3  # be polite to the free public API


def fetch_subject_works(subject_slug, limit):
    url = f"https://openlibrary.org/subjects/{subject_slug}.json"
    resp = requests.get(url, params={"limit": limit}, timeout=15)
    resp.raise_for_status()
    return resp.json().get("works", [])


def cover_url_for(cover_id):
    if not cover_id:
        return ""
    return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"


def build_book_dict(work, genre_label):
    title = (work.get("title") or "").strip()
    authors = work.get("authors") or []
    author_name = authors[0]["name"] if authors else "Unknown Author"
    cover_id = work.get("cover_id")

    if not title or not cover_id:
        return None  # skip anything without a real cover

    price = round(random.uniform(9.99, 29.99), 2)
    total_copies = random.randint(1, 5)
    is_in_store = random.random() < 0.85     # most books available to buy
    is_in_library = random.random() < 0.6     # some also lendable

    return dict(
        title=title,
        author=author_name,
        genre=genre_label,
        description=f"{title} by {author_name}.",
        cover_url=cover_url_for(cover_id),
        price=price,
        is_in_store=is_in_store,
        is_in_library=is_in_library,
        total_copies=total_copies if is_in_library else 0,
        available_copies=total_copies if is_in_library else 0,
    )


def run():
    app = create_app()
    with app.app_context():
        db.create_all()

        existing = {
            (b.title.strip().lower(), b.author.strip().lower())
            for b in Book.query.all()
        }

        added = 0
        skipped = 0

        for subject_slug, genre_label in SUBJECTS.items():
            print(f"Fetching subject: {subject_slug} ...")
            try:
                works = fetch_subject_works(subject_slug, BOOKS_PER_SUBJECT)
            except requests.RequestException as exc:
                print(f"  Could not fetch {subject_slug}: {exc}")
                continue

            for work in works:
                book_dict = build_book_dict(work, genre_label)
                if not book_dict:
                    skipped += 1
                    continue

                key = (book_dict["title"].strip().lower(), book_dict["author"].strip().lower())
                if key in existing:
                    skipped += 1
                    continue

                db.session.add(Book(**book_dict))
                existing.add(key)
                added += 1

            db.session.commit()
            time.sleep(REQUEST_DELAY_SECONDS)

        print(f"Done. Added {added} new books, skipped {skipped} (duplicates or missing cover).")
        print(f"Total books in database: {Book.query.count()}")


if __name__ == "__main__":
    run()