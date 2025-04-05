# Webex Alert Bot
![Docker Build](https://github.com/mallen012/webex-alert-bot/actions/workflows/docker-deploy.yml/badge.svg)


A Dockerized Webex bot with Web UI and support for real-time alerts and rich commands.

---

## ✅ Features

- REST endpoint: `/alert`
- WebSocket support: `ws://host:5650/alert`
- Web UI: send alerts and update config via browser
- Webex command support:
  - `/alert your message`
  - `/dadjoke`
  - `/weather 90210`
  - `/movie 90210`
  - `/tv`

---

## ⚙️ Setup

### 1. Configure `.env`

Duplicate `.env.example` and fill in:

```
WEBEX_TOKEN=your_bot_token
WEBEX_ROOM_ID=your_room_id
OPENWEATHER_API_KEY=...
MOVIE_API_KEY=...
TV_API_KEY=...
```

---

## 🐳 Local Docker Run

```bash
docker build -t webex-alert-bot .
docker run -d -p 5650:5650 --env-file .env --name webex-alert-bot webex-alert-bot
```

Access Web UI: `http://localhost:5650`

---

## 🧪 WebSocket Test

Connect to: `ws://localhost:5650/alert`

---

## ☁️ GitHub + Docker Hub Setup

### 1. Push to GitHub

```bash
git init
git remote add origin https://github.com/mallen012/webex-alert-bot.git
git add .
git commit -m "Deploy full-featured bot"
git push -u origin master
```

### 2. Add Secrets to GitHub Repo

Go to `Settings > Secrets > Actions`, add:

| Name             | Value             |
|------------------|-------------------|
| `DOCKER_USERNAME`| your Docker Hub ID |
| `DOCKER_PASSWORD`| your password or token |

Your image will auto-build & push to:
```
docker.io/mallen012/webex-alert-bot:latest
```

---

## 📦 Unraid Install (Script)

Run from terminal:

```bash
bash install-webex-bot-unraid.sh
```

---

## 🌐 Help Page via GitHub Pages

GitHub Pages is ready via `/docs/index.md`:

- Go to GitHub → Repo → Settings → Pages
- Set source = `main`, folder = `/docs`

Visit:
```
https://mallen012.github.io/webex-alert-bot/
```

---

## License

MIT © mallen012
