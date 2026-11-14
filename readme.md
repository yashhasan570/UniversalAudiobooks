# Universal Audiobooks

A free, self-hosted audiobook and podcast server: stream your library to every device, track progress, and manage collections from a clean web interface, with mobile apps available.

## Contact

Questions or feedback? Reach us on Telegram: [@johnconstantine570](https://t.me/johnconstantine570)

## Running

Docker is the easiest way:

```
docker run -d -p 13378:80 -v /path/to/audiobooks:/audiobooks -v /path/to/config:/config universal-audiobooks
```

Or build from source:

```
npm install && npm run dev
```

## Sync

`.github/workflows/sync.yml` pulls upstream changes daily, re-applies the Universal Audiobooks branding via `scripts/migrate.py`, and pushes.
