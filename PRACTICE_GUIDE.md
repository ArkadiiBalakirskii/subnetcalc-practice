# Практика: Git Flow + GitHub + AI (Copilot) на маленьком проекте

**Проект:** `subnetcalc` — CLI-калькулятор подсетей AWS на Python (только стандартная библиотека).
**Время:** 6–8 часов, можно растянуть на неделю.

> ✅ **Аккаунт AWS не нужен.** Программа ничего не создаёт в облаке и никуда не подключается: она только *считает* адреса локально с помощью стандартной библиотеки Python (`ipaddress`). «AWS» здесь — лишь тема задачи (правило «5 зарезервированных адресов в подсети»). Нужны только **GitHub-аккаунт, Python, git и VS Code с Copilot**.
**Цель:** пройти полный цикл Git Flow (issue → feature → PR → CI → release → hotfix) и на каждом шаге использовать AI-инструменты GitHub.

> ⚠️ Делайте это в **личном** GitHub-аккаунте, не в `nice-illuminate`. Не добавляйте сюда код, данные или секреты NiCE. Если пользуетесь корпоративной лицензией Copilot, соблюдайте политику компании.

---

## Что внутри проекта

```
gh-ai-practice/
├── src/subnetcalc/
│   ├── core.py          ← расчёты (здесь спрятан баг и есть TODO)
│   └── __main__.py      ← CLI: info, split
├── tests/               ← pytest
├── .github/
│   ├── copilot-instructions.md          ← правила для Copilot (Git Flow, коммиты, стиль)
│   ├── instructions/tests.instructions.md  ← правила только для tests/**
│   ├── prompts/pr-description.prompt.md    ← команда /pr-description
│   ├── prompts/release-notes.prompt.md     ← команда /release-notes
│   ├── workflows/ci.yml                    ← CI: ruff + pytest (GitHub Actions)
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/task.md
└── .vscode/settings.json   ← инструкции для генерации commit message и описания PR
```

**Модель веток:** `main` (только релизы с тегами) ← `release/*`, `hotfix/*`; `develop` (интеграция) ← `feature/*`.
**Формат коммитов:** `<type>(GH-<issue>): <message>`, например `fix(GH-1): subtract 5 reserved AWS IPs`. Это тот же принцип, что и `feat(CSA-12345): ...` в NiCE.

---

## Задание 0. Подготовка (30 мин)

> **Если в папке нет `.github` и `.vscode`, а есть `_github` и `_vscode`**, переименуйте их (служебные папки нельзя было записать удалённо):
> ```bash
> mv _github .github && mv _vscode .vscode
> ```
> Либо распакуйте архив `gh-ai-practice.zip`, там они уже с правильными именами.

1. Установите **git**, **Python 3.10+**, **VS Code** с расширением **GitHub Copilot** (Chat входит в него). Войдите в GitHub в VS Code.
2. Убедитесь, что у вас есть Copilot (бесплатный Copilot Free тоже подходит для большинства заданий; задание 5B требует плана с Copilot coding agent).
3. Создайте на GitHub **пустой публичный** репозиторий `subnetcalc-practice` (без README).
4. Залейте проект:

```bash
cd gh-ai-practice
git init -b main
git add .
git commit -m "chore(GH-0): initial project"
git remote add origin git@github.com:<you>/subnetcalc-practice.git
git push -u origin main

git checkout -b develop
git push -u origin develop
```

5. На GitHub: **Settings → General → Default branch = `develop`**.
6. **Settings → Rules → Rulesets → New branch ruleset** для `main` и `develop`:
   - Require a pull request before merging (1 approval можно не включать — вы один);
   - Require status checks to pass → `test` (из CI);
   - Block force pushes.
7. Проверьте, что во вкладке **Actions** CI прошёл зелёным.

**Проверка себя:** что значит `-u` в `git push -u origin develop`?

---

## Задание 1. Разобраться в коде с помощью Copilot Chat (20 мин)

В VS Code откройте Copilot Chat и спросите:

- `@workspace Объясни структуру проекта и как запустить тесты`
- выделите функцию `split` в `core.py` → `/explain`
- `Почему AWS резервирует 5 адресов в подсети? Совпадает ли это с кодом?` ← подсказка к заданию 3

Запустите локально:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m subnetcalc info 10.10.0.0/24
```

Запишите, сколько «AWS usable» показала программа для /24.

---

## Задание 2. Issues (15 мин)

Создайте на GitHub три issue по шаблону **Task** (номера получатся #1, #2, #3):

| # | Заголовок | Суть |
|---|---|---|
| 1 | Wrong number of AWS usable IPs | `/24` должно давать 251, программа даёт другое |
| 2 | Implement `overlaps()` | Найти пересекающиеся CIDR-блоки (функция-заглушка в `core.py`) |
| 3 | Add `overlaps` CLI command | `python -m subnetcalc overlaps 10.0.0.0/16 10.0.1.0/24 ...` |

**AI:** попросите Copilot Chat на github.com (иконка Copilot) помочь сформулировать acceptance criteria для issue #2.

---

## Задание 3. Баг-фикс по полному циклу (1 час) — главное упражнение

```bash
git checkout develop && git pull
git checkout -b feature/GH-1-fix-aws-usable-ips
```

1. **Тест сначала.** Откройте `tests/test_core.py`, напишите комментарий `# test that a /24 has 251 AWS usable IPs` и дайте Copilot дописать тест (inline-подсказка, `Tab`). Или в чате: `/tests` для `aws_usable_ips`.
2. Запустите `pytest -q` — тест должен **упасть**. Это и есть доказательство бага.
3. **Исправление.** Выделите функцию → в чате `/fix` или своими словами. Проверьте, что Copilot использовал константу `AWS_RESERVED_IPS`, а не «магическое число». Заодно уберите комментарий `NOTE: practice bug...`.
4. `pytest -q` и `ruff check .` — зелёные.
5. **Commit message через AI:** вкладка Source Control → иконка ✨ в поле сообщения. Благодаря `.vscode/settings.json` и `copilot-instructions.md` должно получиться что-то вроде `fix(GH-1): use 5 reserved IPs for AWS usable count`. Отредактируйте, если нужно.
6. `git push -u origin feature/GH-1-fix-aws-usable-ips`
7. **PR в `develop`:**
   - описание: в чате VS Code запустите `/pr-description` или нажмите кнопку Copilot в форме PR на GitHub;
   - добавьте `Closes #1`;
   - **Reviewers → Copilot** (Copilot code review), если доступно в вашем плане.
8. Прочитайте замечания Copilot-ревьюера: какие полезные, какие нет? Ответьте на них или исправьте.
9. Дождитесь зелёного CI → **Squash and merge** → удалите ветку.

**Проверка себя:** почему тест пишут до исправления? Что сделал ruleset, если бы CI был красным?

---

## Задание 4. Функция `overlaps()` с Agent mode (45 мин)

Ветка `feature/GH-2-implement-overlaps`.

В Copilot Chat переключитесь в **Agent mode** и дайте задачу:

> Implement `overlaps()` in `src/subnetcalc/core.py` according to issue #2. Return sorted pairs of overlapping CIDRs. Add pytest tests for: no overlaps, one overlap, identical blocks, invalid CIDR. Run the tests.

- Посмотрите, какие файлы агент меняет и какие команды запускает. **Подтверждайте каждый шаг осознанно.**
- Прочитайте diff целиком. Спросите себя: обработан ли случай одинаковых блоков? нет ли сложности O(n²) там, где это важно? (для этого проекта O(n²) нормально)
- Коммит → PR → Copilot review → CI → merge, как в задании 3.

---

## Задание 5. CLI-команда `overlaps` — два способа (45 мин)

**5A. Сами + inline-подсказки.** Ветка `feature/GH-3-overlaps-command`. Добавьте сабкоманду в `__main__.py`, начав печатать `ov = sub.add_parser("overlaps"` — дальше пусть подсказывает Copilot. Тест для CLI тоже начните с имени функции и дайте его дописать.

**5B. (Если доступно) Copilot coding agent.** Вместо 5A откройте issue #3 на GitHub и **назначьте его на Copilot** (Assignees → Copilot). Агент сам создаст ветку и PR.
- Проверьте: ветка от `develop`? имя ветки и формат коммитов соответствуют `copilot-instructions.md`? Если нет — оставьте комментарий в PR с просьбой исправить (агент отреагирует).
- Ревью и merge делаете вы.

**Вывод для себя:** сравните, где AI был полезнее — подсказки, Agent mode или coding agent.

---

## Задание 6. Красный CI и разбор ошибки (20 мин)

1. В новой ветке `feature/GH-4-ci-practice` добавьте в `core.py` неиспользуемый импорт `import os` и сломайте один тест.
2. Откройте PR → CI упадёт.
3. На странице упавшего job нажмите **Explain error** (Copilot) или скопируйте лог в Copilot Chat: «Почему упал CI и как исправить?»
4. Исправьте, дождитесь зелёного. PR можно закрыть без merge.

> В NiCE ту же роль играют Jenkins + `bedrockAnalyzer` и Jenkins MCP-сервер. Принцип одинаковый: AI объясняет лог, решение принимаете вы.

---

## Задание 7. Release (40 мин)

```bash
git checkout develop && git pull
git checkout -b release/0.2.0
```

1. Поднимите версию до `0.2.0` в `pyproject.toml` и `src/subnetcalc/__init__.py` (спросите Copilot: «где ещё указана версия?»).
2. Создайте `CHANGELOG.md` с помощью `/release-notes` в чате.
3. Коммит `chore(GH-5): release 0.2.0` → PR **в `main`** → merge (здесь лучше **Create a merge commit**, а не squash).
4. Тег и релиз:

```bash
git checkout main && git pull
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0
```

5. GitHub → **Releases → Draft a new release** → тег `v0.2.0` → **Generate release notes** (или вставьте текст из CHANGELOG).
6. **Верните изменения в `develop`:** PR `main → develop` (или `release/0.2.0 → develop`) и merge.

**Проверка себя:** почему release мержится и в `main`, и в `develop`?

---

## Задание 8. Hotfix (30 мин)

Найдите «баг в проде»: `python -m subnetcalc split 10.0.0.0/24 --prefix 40` — посмотрите, что происходит. Сообщение об ошибке должно быть понятным.

```bash
git checkout main && git pull
git checkout -b hotfix/0.2.1
```

1. Спросите Copilot: «Как валидировать prefix в `split` (0–32) с понятным сообщением?» Добавьте тест.
2. Версия `0.2.1`, коммит `fix(GH-6): validate prefix range in split`.
3. PR в `main` → merge → тег `v0.2.1` → GitHub Release.
4. PR `main → develop` → merge.

---

## Задание 9. Конфликт слияния (20 мин)

1. От `develop` создайте две ветки: `feature/GH-7-a` и `feature/GH-7-b`.
2. В обеих по-разному измените одну и ту же строку в `README.md` (описание проекта).
3. Смержите первую в `develop`, затем откройте PR второй — будет конфликт.
4. Локально: `git checkout feature/GH-7-b && git merge develop` → в VS Code используйте **Merge Editor** и спросите Copilot Chat: «Объясни конфликт и предложи итоговый текст».
5. Решите конфликт **сами**, закоммитьте, допушьте, смержите.

---

## Итоговый чек-лист

- [ ] Репозиторий с `main` + `develop`, rulesets и зелёным CI
- [ ] 3+ feature-PR в `develop` с `Closes #n` и форматом `type(GH-n)`
- [ ] Использованы: Chat `/explain`, `/tests`, `/fix`, inline-подсказки, Agent mode
- [ ] Commit message и описание PR сгенерированы Copilot (и отредактированы вами)
- [ ] Хотя бы один PR прошёл Copilot code review
- [ ] Разобран красный CI с помощью AI
- [ ] Релиз `v0.2.0` и hotfix `v0.2.1` с тегами и GitHub Releases
- [ ] Решён merge-конфликт
- [ ] (Опционально) PR от Copilot coding agent

## Перенос на работу в NiCE

| Здесь | В NiCE Illuminate |
|---|---|
| `GH-<issue>` | `CSA-<jira>` |
| GitHub Actions `ci.yml` | Jenkins: шаблоны `ILLUM-jenkins-pipeline-templates` + Shared Library |
| ruff + pytest | Sonar, Veracode, BlackDuck, codeScanGate |
| `release/*`, `hotfix/*` вручную | `gitfllow_finalize.groovy`, `monthly-release-deployment-tool` |
| `.github/copilot-instructions.md` | Уже есть в 32 репозиториях (например, `csa-rule-engine-ms`) |
| Explain error в Actions | Jenkins MCP (`csa-devops-mcp-servers`), `bedrockAnalyzer` |

Подробнее — в `COPILOT_GIT_FLOW_GUIDE_RU.md`.
