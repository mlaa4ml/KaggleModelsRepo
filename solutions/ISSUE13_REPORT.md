# Отчёт по issue #13

Агент: `anthropic/claude-opus-5@default`
Ветка: `anthropic-claude-opus-5-default-issue-13` (от `main`, коммит `a237310`)
Дата раунда: раунд 2 из 3.

---

## 1. Проверка памяти между раундами и шагами (обязательный пункт)

**Вывод: память между раундами работает, но частично — в виде текстового
резюме, а не полного контекста.**

Что реально переносится:

| Что | Переносится? | Как это выглядит |
|---|---|---|
| Текст issue и комментариев | да | пришло в резюме первым пунктом |
| Список сделанных вызовов инструментов | да | «Вызовы с прошлого резюме: get_issue, list_files, read_file × 5, list_issues, create_issue_branch» |
| **Полное** содержимое прочитанных файлов | **нет** | в резюме только первые ~200 символов каждого файла, «хвост» обрезан |
| Факт создания ветки | да | «Ветка `...-issue-13` создана от main (a237310)» |
| **Активная (выбранная) рабочая ветка** | **нет** | см. ошибку №1 ниже |
| Бюджет вызовов | обнуляется | 10 вызовов в каждом раунде заново |

Между шагами внутри одного раунда память полная: результаты предыдущих
вызовов видны дословно.

## 2. Ошибки и ограничения, обнаруженные по ходу (как просили в issue)

1. **Сброс выбранной ветки между раундами.** В раунде 1 был вызван
   `create_issue_branch(13)`, инструмент подтвердил: «Текущая рабочая ветка:
   `anthropic-claude-opus-5-default-issue-13`». В раунде 2 первый же
   `write_file` записал файл **не туда** — в ветку
   `anthropic-claude-opus-5-default` (коммит `911c83b`). То есть создание
   ветки запомнилось, а её *выбор* — нет.
   *Обход:* в начале каждого раунда повторно вызывать
   `create_issue_branch(N)` (он идемпотентен и просто переключает ветку),
   и только потом писать файлы. После повторного вызова запись прошла
   корректно (коммит `f0a3ead`).
   *Побочный эффект:* в ветке `anthropic-claude-opus-5-default` остался
   лишний коммит `911c83b` с этим же файлом — на `main` он не влияет.
2. **`list_files`/`search_code`/`read_file` без флага читают `main`, а не
   рабочую ветку.** Чтобы увидеть собственные правки, нужен
   `read_file(..., from_my_branch=True)`. Легко ошибиться и решить, что
   файл не записался.
3. **Обрезка длинных ответов** (`MAX_TOOL_OUTPUT = 12000` в ноутбуке): ноутбуки
   по ~50 КБ целиком не читаются, приходится читать по диапазонам строк.
4. **Нет создания issue.** См. раздел 4 — соответствующего инструмента в
   наборе нет, это ограничение окружения, а не отказ.
5. **Нет выполнения кода.** Проверить функцию запуском нельзя, поэтому тесты
   встроены прямо в модуль (`run_self_test()`), чтобы человек мог прогнать их
   одной командой.

## 3. Инвентаризация репозитория (вопрос 1 из комментария)

На ветке `main`: **папок — 0, файлов — 13** (все файлы лежат в корне,
подкаталогов нет). В моей ветке добавляется каталог `solutions/`, то есть
станет 1 папка и 15 файлов.

| # | Файл | Размер |
|---|---|---|
| 1 | `CAPABILITIES_anthropic-claude-opus-5-default.md` | 10174 B |
| 2 | `CAPABILITIES_google-gemini-3-5-flash-lite.md` | 2536 B |
| 3 | `CAPABILITIES_google-gemma-4-26b-a4b.md` | 1205 B |
| 4 | `CAPABILITIES_openai-gpt-5-4-nano-2026-03-17.md` | 7718 B |
| 5 | `CHANGES_anthropic-claude-opus-5-default.md` | 4122 B |
| 6 | `DIAGNOSTIC_TEST.md` | 4 B |
| 7 | `README.md` | 43 B |
| 8 | `benchmark-task-agentic-github-updated.ipynb` | 50151 B |
| 9 | `benchmark_task_github_skill.ipynb` | 49168 B |
| 10 | `benchmark_task_github_skill_issue_workflow.ipynb` | 614 B |
| 11 | `benchmark_task_github_skill_v2.ipynb` | 33202 B |
| 12 | `benchmark_task_github_skill_v2.md` | 539 B |
| 13 | `gemini_solution_issue9.py` | 757 B |

Краткое описание трёх файлов:

* **`benchmark-task-agentic-github-updated.ipynb`** — тот самый обновлённый
  блокнот из заголовка issue. Внутри: заголовочная markdown-ячейка «Agentic
  GitHub Benchmark v2 — issue-driven (`kbench`)», ячейка конфигурации
  (`GITHUB_OWNER = "mlaa4ml"`, `GITHUB_REPO = "KaggleModelsRepo"`,
  `GITHUB_BASE_BRANCH = "main"`, токен из `kaggle_secrets.UserSecretsClient`),
  транспортный слой `_gh_request` с ретраями на 5xx и вторичный rate limit,
  пагинация `_gh_paginate`, обрезка вывода `_clip`, далее набор инструментов
  агента (`list_files`, `search_code`, `read_file`, `patch_file`,
  `delete_file`, `list_issues`, `get_issue`, `create_issue_branch`,
  `comment_issue`, `report_work`, `diff_vs_base`) и задача
  `github_issue_resolution`. Есть жёсткий guard: запись разрешена только в
  ветки с префиксом slug модели. Требуется fine-grained PAT с правами
  Contents RW, Issues RW, Pull requests RW, Metadata R.
* **`gemini_solution_issue9.py`** — решение прошлой задачи #9 от другого
  агента (Gemini 3.5 Flash Lite). Это не чистый Python, а markdown-текст с
  вложенным блоком кода: функция `gemini_fibonacci(n: int) -> list[int]`.
  Файл с расширением `.py` не импортируется как модуль — тоже своего рода
  найденная ошибка предыдущего раунда.
* **`README.md`** — минимальный, 43 байта: заголовок `# KaggleModelsRepo` и
  строка «test some Kaggle models».

## 4. Issues в репозитории (вопрос 2 из комментария)

Всего issues: **3** (открытых — 1, закрытых — 2).

| № | Состояние | Заголовок | Комментариев |
|---|---|---|---|
| 13 | open | Новая версия кода блокнота в файле `benchmark-task-agentic-github-updated.ipynb` | 1 |
| 12 | closed | Повторный тест работы блокнота/ноутбука | 2 |
| 9 | closed | Проверка новых функций блокнота | 2 |

**Могу ли я создать новый issue?** Нет. В моём наборе инструментов есть
`list_issues`, `get_issue`, `comment_issue`, `report_work` — то есть чтение
issues и комментирование, но инструмента `create_issue` нет. Даже если у
токена стоит право `Issues: RW`, вызвать `POST /repos/{owner}/{repo}/issues`
мне нечем. Чтобы это заработало, в блокноте
`benchmark-task-agentic-github-updated.ipynb` нужно добавить инструмент
примерно такого вида и зарегистрировать его в списке тулов агента:

```python
def create_issue(title: str, body: str = "", labels: list[str] | None = None):
    payload = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    resp = _gh_request("POST", f"{REPO_PATH}/issues", json=payload)
    if resp.status_code != 201:
        return _err("create_issue", resp)
    data = resp.json()
    return f"Создан issue #{data['number']}: {data['html_url']}"
```

## 5. Основное задание: код функции

Добавлен файл **`solutions/issue13_text_stats.py`** — статистика по тексту:

* `text_stats(text, top=3)` — возвращает словарь: `chars`, `chars_no_ws`,
  `words`, `unique_words`, `lines`, `top_words`;
* `top_words(text, limit=3)` — самые частые слова, детерминированный порядок
  (по убыванию частоты, затем по алфавиту);
* `run_self_test()` — встроенный набор проверок без зависимостей.

Учтены: кириллица и латиница, слова через дефис и апостроф (`well-known`),
пропуск чисел, пустая строка, валидация типов (`TypeError` на `None`/не-строку,
`ValueError` на отрицательный `limit`).

Запуск:

```bash
python solutions/issue13_text_stats.py
python solutions/issue13_text_stats.py "свой текст для анализа"
```

Ожидаемый хвост вывода: `SELF-TEST OK: все проверки пройдены`.
Код прогнать в песочнице я не могу (инструмента исполнения нет), поэтому
проверки встроены в модуль и выполняются одной командой на стороне человека.
