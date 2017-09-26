## [Finglish To Farsi Bot](https://t.me/finToFabot)

### A [Telegram](https://telegram.org/) bot to transliterate finglish to farsi

Based on [TransliterateBot](https://github.com/Separius/TransliterateBot) and [PersianLiteration](https://github.com/masihyeganeh/PersianLiteration) API and [telebot](https://github.com/eternnoir/pyTelegramBotAPI) Wrapper for telegram bot API with python

Use this bot in your groups to transliterate finglish messages to farsi

## TO DO

- [x] fix فا use
- [x] get userIds in start for broadcasting new updates.
- [x] make a better help command
- [x] a program for broadcasting a message to given chatIds
- [x] add wrong word report feature(glassy button on every answer)
- [x] add wrong word report for groups too
- [x] add word database and collect user words
- [x] add bug report feature
- [ ] send reports to myself to check if they are correct and then use corrected collection
- [ ] do not transliterate abbreviations, like CTO
- [ ] defallahi method
- [ ] handle irregular syntaxes
- [ ] handle shortening words, and not using vowels, like slm!
- [ ] transliterate messages after edit
### Long Term Goals
- [ ] automate transliteration instead of replying fa to a message.
- [ ] learn words from farsi messages in groups
### Probably Going to Ignore
- [ ] change method from polling to webhook
- [ ] add farsi to finglish using [this](https://github.com/aminmarashi/onezero-f2f) to try to give a recommandation for irregular syntaxes 